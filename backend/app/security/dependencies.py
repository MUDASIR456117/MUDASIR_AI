from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from bson import ObjectId
from backend.app.security.jwt import decode_access_token
from backend.app.database import get_database, get_sync_database

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Validate bearer token and retrieve authenticated user."""
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identity",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db = get_database()
    if db is not None:
        try:
            user = await db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
                return user
        except Exception:
            pass

    # Fallback to sync DB or payload info if DB query fails
    sync_db = get_sync_database()
    if sync_db is not None:
        try:
            user = sync_db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
                return user
        except Exception:
            pass

    # If user object not found in DB but token is valid
    return {
        "id": user_id,
        "email": payload.get("email", "user@example.com"),
        "username": payload.get("username", "demo_user"),
        "role": payload.get("role", "USER"),
        "is_active": True
    }

async def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")
    return current_user

async def get_current_admin_user(current_user: Dict[str, Any] = Depends(get_current_active_user)) -> Dict[str, Any]:
    if current_user.get("role") != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Administrator privileges required"
        )
    return current_user
