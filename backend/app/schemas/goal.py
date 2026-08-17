from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class GoalBase(BaseModel):
    name: str
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(default=0.0, ge=0)
    target_date: datetime
    monthly_contribution: Optional[float] = 0.0
    category: Optional[str] = "Savings"
    status: Optional[str] = "IN_PROGRESS"  # IN_PROGRESS, COMPLETED, PAUSED

class GoalCreate(GoalBase):
    pass

class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    target_date: Optional[datetime] = None
    monthly_contribution: Optional[float] = None
    category: Optional[str] = None
    status: Optional[str] = None

class GoalResponse(GoalBase):
    id: str
    user_id: str
    progress_percentage: float = 0.0
    remaining_amount: float = 0.0
    projected_completion_date: Optional[datetime] = None
    on_track: bool = True
    created_at: datetime
