from fastapi import APIRouter, Depends
from typing import Dict, Any
from backend.app.schemas.credit import CreditProfileCreate, CreditRiskResponse
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.ml_service import ml_service
from backend.app.database import get_sync_database

router = APIRouter(prefix="/credit", tags=["Credit Risk & Explainable AI"])

@router.post("/evaluate", response_model=CreditRiskResponse)
async def evaluate_credit_risk(
    profile: CreditProfileCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    result = ml_service.evaluate_credit_risk(profile.model_dump())
    
    sync_db = get_sync_database()
    if sync_db is not None:
        try:
            sync_db.credit_predictions.insert_one({
                "user_id": current_user["id"],
                "input_profile": profile.model_dump(),
                "prediction": result,
                "created_at": result["assessed_at"]
            })
        except Exception:
            pass

    return result

@router.get("/my-profile", response_model=CreditRiskResponse)
async def get_my_credit_assessment(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    # Evaluate with default user profile parameters
    default_profile = {
        "annual_income": float(current_user.get("monthly_income", 5000.0)) * 12.0,
        "employment_duration_years": 4.5,
        "existing_loans_count": 1,
        "monthly_debt_payments": 420.0,
        "payment_history_on_time_pct": 98.0,
        "credit_utilization_ratio": 22.0,
        "number_of_open_accounts": 5,
        "previous_defaults_count": 0,
        "age": 30
    }
    return ml_service.evaluate_credit_risk(default_profile)
