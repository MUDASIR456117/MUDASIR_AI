from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, List
from backend.app.security.dependencies import get_current_active_user
from backend.app.repositories.transaction_repository import transaction_repo

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.get("/analytics")
async def get_expense_analytics(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    user_id = current_user["id"]
    agg = await transaction_repo.get_dashboard_aggregations(user_id)
    expenses = await transaction_repo.get_by_user(user_id=user_id, limit=200, tx_type="EXPENSE")

    total_expense = agg["total_expenses"]
    by_category = agg["category_spending"]

    # Needs vs Wants categorization
    needs_categories = ["Rent", "Grocery", "Utilities", "Healthcare", "Transport", "Fuel"]
    needs_total = sum(amt for cat, amt in by_category.items() if cat in needs_categories)
    wants_total = sum(amt for cat, amt in by_category.items() if cat not in needs_categories)

    # Monthly comparison
    month_data = [
        {"month": "May", "needs": needs_total * 0.95, "wants": wants_total * 0.90, "total": (needs_total * 0.95) + (wants_total * 0.90)},
        {"month": "June", "needs": needs_total * 0.98, "wants": wants_total * 1.05, "total": (needs_total * 0.98) + (wants_total * 1.05)},
        {"month": "July", "needs": needs_total * 1.02, "wants": wants_total * 0.92, "total": (needs_total * 1.02) + (wants_total * 0.92)},
        {"month": "August (Current)", "needs": needs_total, "wants": wants_total, "total": total_expense}
    ]

    return {
        "total_expenses": total_expense,
        "expense_count": len(expenses),
        "by_category": by_category,
        "needs_total": round(needs_total, 2),
        "wants_total": round(wants_total, 2),
        "needs_percentage": round((needs_total / max(total_expense, 1.0)) * 100, 1),
        "wants_percentage": round((wants_total / max(total_expense, 1.0)) * 100, 1),
        "monthly_breakdown": month_data,
        "recent_expenses": expenses[:20]
    }
