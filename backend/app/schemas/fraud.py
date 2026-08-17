from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FraudCheckRequest(BaseModel):
    amount: float
    category: str
    merchant: Optional[str] = ""
    payment_method: Optional[str] = "Credit Card"
    location: Optional[str] = "Online"
    transaction_time: Optional[datetime] = None

class FraudAlertResponse(BaseModel):
    transaction_id: Optional[str] = None
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    risk_score: float  # 0.0 - 100.0
    fraud_probability: float  # 0.0 - 1.0
    is_anomaly: bool
    reasons: List[str]
    recommended_action: str
    disclaimer: str = "Anomaly detection represents a statistical risk signal, not definitive proof of fraud."
    checked_at: datetime = Field(default_factory=datetime.utcnow)

class FraudAlertHistoryItem(BaseModel):
    id: str
    user_id: str
    transaction_id: Optional[str] = None
    risk_level: str
    risk_score: float
    reasons: List[str]
    amount: float
    merchant: str
    created_at: datetime
