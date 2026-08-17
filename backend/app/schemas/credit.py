from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class CreditProfileCreate(BaseModel):
    annual_income: float = Field(..., gt=0)
    employment_duration_years: float = Field(..., ge=0)
    existing_loans_count: int = Field(default=0, ge=0)
    monthly_debt_payments: float = Field(default=0.0, ge=0)
    payment_history_on_time_pct: float = Field(default=100.0, ge=0, le=100)
    credit_utilization_ratio: float = Field(default=30.0, ge=0, le=100)
    number_of_open_accounts: int = Field(default=3, ge=1)
    previous_defaults_count: int = Field(default=0, ge=0)
    age: int = Field(..., ge=18, le=100)
    savings_balance: Optional[float] = 0.0

class CreditRiskResponse(BaseModel):
    risk_category: str  # "LOW RISK", "MEDIUM RISK", "HIGH RISK"
    estimated_credit_score_range: str  # e.g., "720 - 780 (Very Good)"
    default_probability: float  # 0.0 - 1.0
    confidence_score: float  # 0.0 - 1.0
    top_positive_factors: List[str]
    top_risk_factors: List[str]
    feature_importance: Dict[str, float]
    disclaimer: str = "This prediction is an educational and model-based estimate and does not represent an official credit score or loan approval guarantee."
    assessed_at: datetime = Field(default_factory=datetime.utcnow)
