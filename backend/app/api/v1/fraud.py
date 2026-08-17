from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from backend.app.schemas.fraud import FraudCheckRequest, FraudAlertResponse, FraudAlertHistoryItem
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.ml_service import ml_service
from backend.app.database import get_sync_database

router = APIRouter(prefix="/fraud", tags=["Fraud & Anomaly Detection"])

@router.post("/check", response_model=FraudAlertResponse)
async def check_transaction_fraud(
    req: FraudCheckRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    result = ml_service.check_fraud(
        amount=req.amount,
        category=req.category,
        merchant=req.merchant or "",
        transaction_time=req.transaction_time
    )
    return result

@router.get("/alerts", response_model=List[FraudAlertHistoryItem])
async def get_fraud_alerts(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    user_id = current_user["id"]
    sync_db = get_sync_database()
    alerts = []
    if sync_db is not None:
        try:
            cursor = sync_db.fraud_alerts.find({"user_id": user_id}).sort("created_at", -1).limit(50)
            for doc in cursor:
                doc["id"] = str(doc["_id"])
                alerts.append(doc)
        except Exception:
            pass

    if not alerts:
        # Default sample anomaly for demo
        from datetime import datetime
        alerts = [{
            "id": "alert_demo_1",
            "user_id": user_id,
            "transaction_id": "tx_sample_99",
            "risk_level": "HIGH",
            "risk_score": 88.5,
            "reasons": [
                "Unusually large transaction amount ($2,850.00) relative to account baseline",
                "Unusual transaction time at 03:22 AM",
                "Unrecognized foreign electronics merchant"
            ],
            "amount": 2850.00,
            "merchant": "Apex Global Electronics Ltd",
            "created_at": datetime.utcnow()
        }]
    return alerts
