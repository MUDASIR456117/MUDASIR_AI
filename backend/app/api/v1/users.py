from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from bson import ObjectId
from backend.app.schemas.user import UserResponse, UserUpdate
from backend.app.security.dependencies import get_current_active_user
from backend.app.database import get_sync_database

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    user_id = current_user["id"]
    sync_db = get_sync_database()
    
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    if sync_db is not None and update_dict:
        try:
            sync_db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_dict})
            user = sync_db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
                return user
        except Exception:
            pass

    current_user.update(update_dict)
    return current_user
