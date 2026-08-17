from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from backend.app.schemas.investment import (
    RiskProfileRequest, RiskProfileResponse, PortfolioHolding, PortfolioSummaryResponse
)
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.investment_service import investment_service
from backend.app.database import get_sync_database

router = APIRouter(prefix="/investments", tags=["Investment Advisor"])

@router.post("/risk-profile", response_model=RiskProfileResponse)
async def calculate_risk_profile(
    req: RiskProfileRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    return investment_service.evaluate_risk_profile(req.model_dump())

@router.get("/recommendations", response_model=RiskProfileResponse)
async def get_default_investment_recommendations(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    default_req = {
        "monthly_income": float(current_user.get("monthly_income", 5000.0)),
        "monthly_savings": float(current_user.get("monthly_income", 5000.0)) * 0.20,
        "age": 30,
        "primary_goal": "Wealth Accumulation",
        "investment_horizon_years": 10,
        "risk_tolerance_level": current_user.get("risk_tolerance", "MODERATE"),
        "emergency_fund_months": 4.0
    }
    return investment_service.evaluate_risk_profile(default_req)
