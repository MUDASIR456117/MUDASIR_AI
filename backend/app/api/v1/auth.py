from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import datetime, timezone
from bson import ObjectId
import re
from pymongo.errors import DuplicateKeyError
from backend.app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from backend.app.security.password import verify_password, get_password_hash
from backend.app.security.jwt import create_access_token
from backend.app.security.dependencies import get_current_active_user
from backend.app.database import get_database, get_sync_database

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    sync_db = get_sync_database()
    clean_email = str(user_in.email).strip().lower()
    clean_username = str(user_in.username).strip()

    # Check if user already exists in MongoDB
    if sync_db is not None:
        existing = sync_db.users.find_one({
            "$or": [
                {"email": clean_email},
                {"username": clean_username}
            ]
        })
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email or username already exists."
            )

    hashed_pw = get_password_hash(user_in.password)
    user_doc = {
        "email": clean_email,
        "username": clean_username,
        "full_name": user_in.full_name.strip() if user_in.full_name else clean_username.capitalize(),
        "hashed_password": hashed_pw,
        "role": user_in.role if user_in.role in ["USER", "ADMIN"] else "USER",
        "is_active": True,
        "monthly_income": float(user_in.monthly_income or 5000.0),
        "risk_tolerance": user_in.risk_tolerance or "MODERATE",
        "created_at": datetime.now(timezone.utc)
    }

    user_id = str(ObjectId())
    if sync_db is not None:
        try:
            res = sync_db.users.insert_one(user_doc)
            user_id = str(res.inserted_id)
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An account with this email or username already exists."
            )
        except Exception as e:
            pass

    user_doc["id"] = user_id

    access_token = create_access_token(
        data={
            "sub": user_id,
            "email": user_doc["email"],
            "username": user_doc["username"],
            "role": user_doc["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_doc
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    sync_db = get_sync_database()
    clean_email = str(credentials.email).strip().lower()

    user = None
    if sync_db is not None:
        try:
            user = sync_db.users.find_one({"email": clean_email})
            if not user:
                user = sync_db.users.find_one({"email": {"$regex": f"^{re.escape(clean_email)}$", "$options": "i"}})
        except Exception:
            user = None

    if not user or not verify_password(credentials.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled. Please contact support."
        )

    user_id = str(user["_id"])
    user["id"] = user_id

    access_token = create_access_token(
        data={
            "sub": user_id,
            "email": user.get("email", clean_email),
            "username": user.get("username", clean_email.split("@")[0]),
            "role": user.get("role", "USER")
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    return current_user
