from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class RiskProfileRequest(BaseModel):
    monthly_income: float = Field(..., gt=0)
    monthly_savings: float = Field(..., ge=0)
    age: int = Field(..., ge=18, le=100)
    primary_goal: str = "Wealth Accumulation"  # "Retirement", "Home Purchase", "Wealth Accumulation", "Preservation"
    investment_horizon_years: int = Field(..., ge=1, le=50)
    risk_tolerance_level: str = "MODERATE"  # "CONSERVATIVE", "MODERATE", "AGGRESSIVE"
    emergency_fund_months: float = Field(default=3.0, ge=0)

class AssetAllocationItem(BaseModel):
    asset_class: str
    allocation_pct: float
    recommended_amount: float
    description: str
    expected_volatility: str

class RiskProfileResponse(BaseModel):
    classified_profile: str  # "CONSERVATIVE", "MODERATE", "AGGRESSIVE"
    profile_score: float  # 0 - 100
    target_annual_return_range: str
    asset_allocation: List[AssetAllocationItem]
    insights: List[str]
    disclaimer: str = "This application provides educational and analytical information and is not a substitute for advice from a licensed financial professional. No guaranteed returns."

class PortfolioHolding(BaseModel):
    id: Optional[str] = None
    symbol: str
    name: str
    asset_type: str  # "Stock", "ETF", "Mutual Fund", "Bond", "Crypto", "Gold", "Cash"
    quantity: float = Field(..., gt=0)
    purchase_price: float = Field(..., gt=0)
    current_price: float = Field(..., gt=0)

class PortfolioSummaryResponse(BaseModel):
    total_invested: float
    current_value: float
    total_gain_loss: float
    total_gain_loss_pct: float
    holdings: List[PortfolioHolding]
    allocation_by_type: Dict[str, float]
    concentration_risk: str  # "Low", "Moderate", "High"
    risk_indicators: List[str]
