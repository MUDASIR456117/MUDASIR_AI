from fastapi import APIRouter, Depends
from typing import Dict, Any, List
import pandas as pd
from backend.app.schemas.forecast import ForecastResponse
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.ml_service import ml_service
from backend.app.repositories.transaction_repository import transaction_repo

router = APIRouter(prefix="/forecast", tags=["Financial Forecast & Deep Learning"])

@router.get("/", response_model=ForecastResponse)
async def get_spending_forecast(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    user_id = current_user["id"]
    txs = await transaction_repo.get_by_user(user_id=user_id, limit=300, tx_type="EXPENSE")

    # If user has sparse transactions, generate sample daily series for demonstration
    daily_history = []
    if len(txs) >= 7:
        df = pd.DataFrame(txs)
        df["date_str"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        grouped = df.groupby("date_str")["amount"].sum().reset_index()
        daily_history = grouped.to_dict(orient="records")
    else:
        # Provide base history
        from datetime import datetime, timedelta
        now = datetime.utcnow()
        for i in range(30, 0, -1):
            d = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_history.append({"date": d, "amount": 65.0 + (i % 7) * 12.0})

    forecast = ml_service.generate_spending_forecast(daily_history)
    return forecast
