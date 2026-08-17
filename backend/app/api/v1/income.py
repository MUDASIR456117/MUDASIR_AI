from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, List
from backend.app.security.dependencies import get_current_active_user
from backend.app.repositories.transaction_repository import transaction_repo

router = APIRouter(prefix="/income", tags=["Income"])

@router.get("/")
async def get_income_summary(
    limit: int = Query(50, ge=1),
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    user_id = current_user["id"]
    incomes = await transaction_repo.get_by_user(user_id=user_id, limit=limit, tx_type="INCOME")
    
    total = sum(float(i.get("amount", 0.0)) for i in incomes)
    by_source: Dict[str, float] = {}
    for i in incomes:
        src = i.get("category", "Salary")
        by_source[src] = by_source.get(src, 0.0) + float(i.get("amount", 0.0))

    return {
        "total_income": round(total, 2),
        "income_count": len(incomes),
        "breakdown_by_source": by_source,
        "records": incomes
    }
