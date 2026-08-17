from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId
from backend.app.schemas.transaction import (
    TransactionCreate, TransactionUpdate, TransactionResponse, TransactionType
)
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.ml_service import ml_service
from backend.app.repositories.transaction_repository import transaction_repo
from backend.app.database import get_sync_database

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    tx_in: TransactionCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    user_id = current_user["id"]
    sync_db = get_sync_database()

    # 1. AI ML Auto-Categorization if category is "Other" or blank
    category = tx_in.category
    confidence = 1.0
    if not category or category == "Other":
        predicted_cat, conf = ml_service.predict_category(tx_in.description, tx_in.merchant or "", tx_in.amount)
        category = predicted_cat
        confidence = conf

    # 2. AI ML Real-time Fraud Anomaly Check
    fraud_eval = ml_service.check_fraud(
        amount=tx_in.amount,
        category=category,
        merchant=tx_in.merchant or "",
        transaction_time=tx_in.date
    )

    doc = {
        "user_id": user_id,
        "type": tx_in.type.value if hasattr(tx_in.type, "value") else str(tx_in.type),
        "category": category,
        "amount": round(tx_in.amount, 2),
        "currency": tx_in.currency,
        "description": tx_in.description,
        "merchant": tx_in.merchant or "",
        "date": tx_in.date or datetime.utcnow(),
        "payment_method": tx_in.payment_method or "Credit Card",
        "location": tx_in.location or "Online",
        "status": tx_in.status or "COMPLETED",
        "is_anomaly": fraud_eval["is_anomaly"],
        "anomaly_score": fraud_eval["risk_score"],
        "created_at": datetime.utcnow()
    }

    created = await transaction_repo.create(doc)

    # If flagged as high risk anomaly, register fraud alert in DB
    if fraud_eval["risk_level"] in ["MEDIUM", "HIGH"] and sync_db is not None:
        try:
            sync_db.fraud_alerts.insert_one({
                "user_id": user_id,
                "transaction_id": created["id"],
                "risk_level": fraud_eval["risk_level"],
                "risk_score": fraud_eval["risk_score"],
                "reasons": fraud_eval["reasons"],
                "amount": tx_in.amount,
                "merchant": tx_in.merchant or tx_in.description,
                "created_at": datetime.utcnow()
            })
        except Exception:
            pass

    return created

@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0),
    category: Optional[str] = None,
    tx_type: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    user_id = current_user["id"]
    return await transaction_repo.get_by_user(
        user_id=user_id, limit=limit, skip=skip, category=category, tx_type=tx_type
    )

@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    tx_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    user_id = current_user["id"]
    success = await transaction_repo.delete(tx_id, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found or unauthorized")
    return None
