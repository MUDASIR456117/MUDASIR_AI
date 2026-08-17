from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class ForecastDataPoint(BaseModel):
    date: str
    predicted_amount: float
    lower_bound: float
    upper_bound: float

class ForecastResponse(BaseModel):
    model_used: str  # "LSTM Deep Learning" or "Gradient Boosting ML"
    has_sufficient_data: bool
    status_message: str
    next_week_predicted: Optional[float] = 0.0
    next_month_predicted: Optional[float] = 0.0
    annual_projected: Optional[float] = 0.0
    category_forecasts: Dict[str, float] = Field(default_factory=dict)
    historical_trend: List[Dict[str, float]] = Field(default_factory=list)
    future_forecast_series: List[ForecastDataPoint] = Field(default_factory=list)
    metrics: Dict[str, float] = Field(default_factory=dict)  # MAE, RMSE, R2
    generated_at: datetime = Field(default_factory=datetime.utcnow)
