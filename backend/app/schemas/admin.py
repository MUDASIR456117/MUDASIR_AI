from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ModelStatus(BaseModel):
    name: str
    version: str
    status: str  # "LOADED", "TRAINING", "ERROR", "UNINITIALIZED"
    type: str  # "ML", "DL", "CV", "NLP"
    accuracy_or_metric: Optional[str] = "N/A"
    last_trained: Optional[str] = "Pre-packaged"

class SystemHealthResponse(BaseModel):
    status: str = "healthy"
    database: str = "connected"
    models: str = "loaded"
    environment: str = "production-ready"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AdminStatsResponse(BaseModel):
    total_users: int
    active_users_last_30d: int
    total_transactions_count: int
    total_transaction_volume: float
    total_fraud_alerts: int
    high_risk_anomalies_count: int
    models: List[ModelStatus]
    api_uptime_pct: float = 99.98
    recent_audit_logs: List[Dict[str, Any]] = Field(default_factory=list)
