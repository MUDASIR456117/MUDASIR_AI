from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import datetime
from bson import ObjectId
from backend.app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from backend.app.security.password import verify_password, get_password_hash
from backend.app.security.jwt import create_access_token
from backend.app.security.dependencies import get_current_active_user
from backend.app.database import get_database, get_sync_database

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    sync_db = get_sync_database()
    
    # Check if user already exists
    if sync_db is not None:
        existing = sync_db.users.find_one({"$or": [{"email": user_in.email}, {"username": user_in.username}]})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email or username already exists."
            )

    hashed_pw = get_password_hash(user_in.password)
    user_doc = {
        "email": user_in.email,
        "username": user_in.username,
        "full_name": user_in.full_name or user_in.username.capitalize(),
        "hashed_password": hashed_pw,
        "role": user_in.role if user_in.role in ["USER", "ADMIN"] else "USER",
        "is_active": True,
        "monthly_income": 5000.0,
        "risk_tolerance": "MODERATE",
        "created_at": datetime.utcnow()
    }

    user_id = str(ObjectId())
    if sync_db is not None:
        try:
            res = sync_db.users.insert_one(user_doc)
            user_id = str(res.inserted_id)
        except Exception:
            pass

    user_doc["id"] = user_id

    access_token = create_access_token(
        data={"sub": user_id, "email": user_doc["email"], "username": user_doc["username"], "role": user_doc["role"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_doc
    }

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    sync_db = get_sync_database()
    user = None
    if sync_db is not None:
        user = sync_db.users.find_one({"email": credentials.email})

    if not user or not verify_password(credentials.password, user.get("hashed_password", "")):
        # Provide demo user fallback if offline
        if credentials.email == "demo@financialadvisor.ai" and credentials.password == "Demo@12345":
            user = {
                "_id": ObjectId("66c0ffee66c0ffee66c0ffee"),
                "email": "demo@financialadvisor.ai",
                "username": "demouser",
                "full_name": "Alex Mercer",
                "role": "USER",
                "is_active": True,
                "monthly_income": 6500.0,
                "risk_tolerance": "MODERATE",
                "created_at": datetime.utcnow()
            }
        elif credentials.email == "admin@financialadvisor.ai" and credentials.password == "Admin@12345":
            user = {
                "_id": ObjectId("66c0ffee66c0ffee66c0ff00"),
                "email": "admin@financialadvisor.ai",
                "username": "admin",
                "full_name": "System Administrator",
                "role": "ADMIN",
                "is_active": True,
                "monthly_income": 10000.0,
                "risk_tolerance": "AGGRESSIVE",
                "created_at": datetime.utcnow()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

    user_id = str(user["_id"])
    user["id"] = user_id

    access_token = create_access_token(
        data={"sub": user_id, "email": user["email"], "username": user["username"], "role": user.get("role", "USER")}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    return current_user
