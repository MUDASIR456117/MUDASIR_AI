from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class BudgetBase(BaseModel):
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=2000, le=2100)
    total_budget: float = Field(..., gt=0)
    category_limits: Dict[str, float] = Field(default_factory=dict)

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    total_budget: Optional[float] = None
    category_limits: Optional[Dict[str, float]] = None

class BudgetResponse(BudgetBase):
    id: str
    user_id: str
    total_spent: float = 0.0
    category_spent: Dict[str, float] = Field(default_factory=dict)
    percentage_used: float = 0.0
    created_at: datetime

class BudgetRecommendation(BaseModel):
    monthly_income: float
    recommended_total_budget: float
    needs_budget: float
    wants_budget: float
    savings_target: float
    emergency_fund_target: float
    category_allocations: Dict[str, float]
    overspending_warnings: list[str] = Field(default_factory=list)
