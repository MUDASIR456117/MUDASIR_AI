from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from datetime import datetime
from backend.app.schemas.budget import BudgetCreate, BudgetResponse, BudgetRecommendation
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.budget_service import budget_service
from backend.app.repositories.transaction_repository import transaction_repo
from backend.app.database import get_sync_database

router = APIRouter(prefix="/budget", tags=["AI Budget Planner"])

@router.get("/recommendation", response_model=BudgetRecommendation)
async def get_budget_recommendation(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    user_id = current_user["id"]
    agg = await transaction_repo.get_dashboard_aggregations(user_id)
    monthly_income = agg["total_income"] if agg["total_income"] > 0 else float(current_user.get("monthly_income", 5000.0))
    category_spends = agg.get("category_spending", {})
    return budget_service.generate_smart_budget_recommendation(
        monthly_income=monthly_income,
        historical_category_spends=category_spends
    )

@router.get("/status")
async def get_budget_status(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    user_id = current_user["id"]
    agg = await transaction_repo.get_dashboard_aggregations(user_id)
    monthly_income = agg["total_income"] if agg["total_income"] > 0 else float(current_user.get("monthly_income", 5000.0))
    total_spent = agg["total_expenses"]
    monthly_budget = float(current_user.get("monthly_budget", monthly_income * 0.70))

    cat_spending = agg.get("category_spending", {})
    rec = budget_service.generate_smart_budget_recommendation(monthly_income, cat_spending)

    categories_status = []
    for cat, limit in rec["category_allocations"].items():
        spent = cat_spending.get(cat, 0.0)
        pct = round((spent / max(limit, 1.0)) * 100.0, 1)
        categories_status.append({
            "category": cat,
            "budget_limit": limit,
            "actual_spent": spent,
            "remaining": round(max(0.0, limit - spent), 2),
            "percentage_used": pct,
            "is_over_budget": spent > limit
        })

    return {
        "monthly_budget": monthly_budget,
        "total_spent": total_spent,
        "remaining_budget": round(max(0.0, monthly_budget - total_spent), 2),
        "percentage_used": round((total_spent / max(monthly_budget, 1.0)) * 100.0, 1),
        "categories": categories_status,
        "warnings": rec["overspending_warnings"]
    }
