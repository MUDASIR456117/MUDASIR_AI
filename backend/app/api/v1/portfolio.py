from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from bson import ObjectId
from backend.app.schemas.investment import PortfolioHolding, PortfolioSummaryResponse
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.investment_service import investment_service
from backend.app.database import get_sync_database

router = APIRouter(prefix="/portfolio", tags=["Portfolio Analysis"])

@router.get("/", response_model=PortfolioSummaryResponse)
async def get_portfolio(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    user_id = current_user["id"]
    sync_db = get_sync_database()
    holdings = []
    
    if sync_db is not None:
        try:
            cursor = sync_db.portfolios.find({"user_id": user_id})
            for doc in cursor:
                doc["id"] = str(doc["_id"])
                holdings.append(doc)
        except Exception:
            pass

    if not holdings:
        # Default sample portfolio for demonstration
        holdings = [
            {"id": "h1", "symbol": "VOO", "name": "Vanguard S&P 500 ETF", "asset_type": "ETF", "quantity": 15.0, "purchase_price": 420.0, "current_price": 490.50},
            {"id": "h2", "symbol": "MSFT", "name": "Microsoft Corporation", "asset_type": "Stock", "quantity": 10.0, "purchase_price": 380.0, "current_price": 425.00},
            {"id": "h3", "symbol": "BND", "name": "Vanguard Total Bond Market", "asset_type": "Bond", "quantity": 40.0, "purchase_price": 72.0, "current_price": 74.50},
            {"id": "h4", "symbol": "GLD", "name": "SPDR Gold Trust", "asset_type": "Gold", "quantity": 8.0, "purchase_price": 195.0, "current_price": 218.00}
        ]

    return investment_service.analyze_portfolio(holdings)

@router.post("/holdings", response_model=PortfolioHolding, status_code=status.HTTP_201_CREATED)
async def add_holding(
    holding_in: PortfolioHolding,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    user_id = current_user["id"]
    sync_db = get_sync_database()
    doc = holding_in.model_dump()
    doc["user_id"] = user_id

    if sync_db is not None:
        try:
            res = sync_db.portfolios.insert_one(doc)
            doc["id"] = str(res.inserted_id)
            return doc
        except Exception:
            pass

    doc["id"] = "h_" + ObjectId().__str__()
    return doc
