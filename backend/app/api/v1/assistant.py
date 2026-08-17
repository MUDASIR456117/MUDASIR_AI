from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime
from backend.app.schemas.assistant import ChatRequest, ChatResponse, FinancialHealthResponse
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.assistant_service import assistant_service
from backend.app.services.health_score_service import health_score_service
from backend.app.repositories.transaction_repository import transaction_repo
from backend.app.database import get_sync_database

router = APIRouter(prefix="/assistant", tags=["AI Financial Assistant"])

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    chat_req: ChatRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    user_id = current_user["id"]
    agg = await transaction_repo.get_dashboard_aggregations(user_id)
    monthly_income = agg["total_income"] if agg["total_income"] > 0 else float(current_user.get("monthly_income", 5000.0))
    monthly_expenses = agg["total_expenses"]

    user_context = {
        "monthly_income": monthly_income,
        "current_month_expenses": monthly_expenses,
        "previous_month_expenses": monthly_expenses * 0.94,
        "monthly_budget": float(current_user.get("monthly_budget", 3500.0)),
        "category_spends": agg.get("category_spending", {}),
        "health_score": 78,
        "username": current_user.get("username", "User")
    }

    response = assistant_service.process_query(chat_req.message, user_context)

    # Save to chat history
    sync_db = get_sync_database()
    if sync_db is not None:
        try:
            sync_db.chat_history.insert_one({
                "user_id": user_id,
                "user_message": chat_req.message,
                "assistant_reply": response["reply"],
                "timestamp": datetime.utcnow()
            })
        except Exception:
            pass

    return response

@router.get("/health-score", response_model=FinancialHealthResponse)
async def get_financial_health_score(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    user_id = current_user["id"]
    agg = await transaction_repo.get_dashboard_aggregations(user_id)
    monthly_income = agg["total_income"] if agg["total_income"] > 0 else float(current_user.get("monthly_income", 5000.0))
    monthly_expenses = agg["total_expenses"] if agg["total_expenses"] > 0 else 3100.0

    return health_score_service.calculate_health_score({
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "emergency_savings": monthly_income * 2.5,
        "monthly_debt": 350.0,
        "budget_limit": float(current_user.get("monthly_budget", 3500.0)),
        "spending_volatility_pct": 12.0
    })
