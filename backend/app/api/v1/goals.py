from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from datetime import datetime
from bson import ObjectId
from backend.app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from backend.app.security.dependencies import get_current_active_user
from backend.app.database import get_sync_database

router = APIRouter(prefix="/goals", tags=["Financial Goals"])

@router.get("/", response_model=List[GoalResponse])
async def list_goals(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    user_id = current_user["id"]
    sync_db = get_sync_database()
    goals = []

    if sync_db is not None:
        try:
            cursor = sync_db.financial_goals.find({"user_id": user_id})
            for doc in cursor:
                doc["id"] = str(doc["_id"])
                target = float(doc.get("target_amount", 1000.0))
                current = float(doc.get("current_amount", 0.0))
                doc["progress_percentage"] = round((current / max(target, 1.0)) * 100.0, 1)
                doc["remaining_amount"] = round(max(0.0, target - current), 2)
                goals.append(doc)
        except Exception:
            pass

    if not goals:
        # Default starter financial goals
        goals = [
            {
                "id": "g1", "user_id": user_id, "name": "Emergency Fund (6 Months)",
                "target_amount": 18000.0, "current_amount": 12500.0, "target_date": datetime(2026, 12, 31),
                "monthly_contribution": 750.0, "category": "Emergency", "status": "IN_PROGRESS",
                "progress_percentage": 69.4, "remaining_amount": 5500.0, "on_track": True, "created_at": datetime.utcnow()
            },
            {
                "id": "g2", "user_id": user_id, "name": "Tech Gadget Upgrade (MacBook / GPU)",
                "target_amount": 3200.0, "current_amount": 2400.0, "target_date": datetime(2026, 10, 15),
                "monthly_contribution": 400.0, "category": "Gadgets", "status": "IN_PROGRESS",
                "progress_percentage": 75.0, "remaining_amount": 800.0, "on_track": True, "created_at": datetime.utcnow()
            },
            {
                "id": "g3", "user_id": user_id, "name": "Europe Vacation Trip",
                "target_amount": 5000.0, "current_amount": 1800.0, "target_date": datetime(2027, 6, 1),
                "monthly_contribution": 350.0, "category": "Travel", "status": "IN_PROGRESS",
                "progress_percentage": 36.0, "remaining_amount": 3200.0, "on_track": True, "created_at": datetime.utcnow()
            }
        ]

    return goals

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal_in: GoalCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    user_id = current_user["id"]
    sync_db = get_sync_database()
    doc = goal_in.model_dump()
    doc["user_id"] = user_id
    doc["created_at"] = datetime.utcnow()

    target = float(doc.get("target_amount", 1000.0))
    current = float(doc.get("current_amount", 0.0))
    doc["progress_percentage"] = round((current / max(target, 1.0)) * 100.0, 1)
    doc["remaining_amount"] = round(max(0.0, target - current), 2)
    doc["on_track"] = True

    if sync_db is not None:
        try:
            res = sync_db.financial_goals.insert_one(doc)
            doc["id"] = str(res.inserted_id)
            return doc
        except Exception:
            pass

    doc["id"] = "goal_" + ObjectId().__str__()
    return doc
