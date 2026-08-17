from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    relevant_metrics: Optional[Dict[str, float]] = None
    suggested_actions: Optional[List[str]] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HealthScoreComponent(BaseModel):
    name: str
    score: float  # out of max_score
    max_score: float
    status: str  # "EXCELLENT", "GOOD", "NEEDS IMPROVEMENT", "CRITICAL"
    value_display: str
    benchmark: str

class FinancialHealthResponse(BaseModel):
    overall_score: int  # 0 to 100
    category_rating: str  # "EXCELLENT", "GOOD", "FAIR", "POOR"
    components: List[HealthScoreComponent]
    strengths: List[str]
    improvements: List[str]
    calculated_at: datetime = Field(default_factory=datetime.utcnow)
