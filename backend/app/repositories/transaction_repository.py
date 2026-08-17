import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId
from backend.app.database import get_database, get_sync_database

logger = logging.getLogger(__name__)

class TransactionRepository:
    def __init__(self):
        pass

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        db = get_database()
        if db is not None:
            try:
                res = await db.transactions.insert_one(data)
                data["_id"] = res.inserted_id
                data["id"] = str(res.inserted_id)
                return data
            except Exception as e:
                logger.warning("Async Mongo insert failed: %s", e)

        sync_db = get_sync_database()
        if sync_db is not None:
            try:
                res = sync_db.transactions.insert_one(data)
                data["_id"] = res.inserted_id
                data["id"] = str(res.inserted_id)
                return data
            except Exception as e:
                logger.warning("Sync Mongo insert failed: %s", e)

        data["id"] = str(data.get("_id", "tx_" + datetime.utcnow().strftime("%Y%m%d%H%M%S")))
        return data

    async def get_by_user(self, user_id: str, limit: int = 100, skip: int = 0,
                          category: Optional[str] = None, tx_type: Optional[str] = None) -> List[Dict[str, Any]]:
        query: Dict[str, Any] = {"user_id": user_id}
        if category:
            query["category"] = category
        if tx_type:
            query["type"] = tx_type

        db = get_database()
        if db is not None:
            try:
                cursor = db.transactions.find(query).sort("date", -1).skip(skip).limit(limit)
                items = await cursor.to_list(length=limit)
                for item in items:
                    item["id"] = str(item["_id"])
                return items
            except Exception as e:
                logger.warning("Async Mongo query failed: %s", e)

        sync_db = get_sync_database()
        if sync_db is not None:
            try:
                cursor = sync_db.transactions.find(query).sort("date", -1).skip(skip).limit(limit)
                items = list(cursor)
                for item in items:
                    item["id"] = str(item["_id"])
                return items
            except Exception as e:
                logger.warning("Sync Mongo query failed: %s", e)

        return []

    async def delete(self, tx_id: str, user_id: str) -> bool:
        try:
            oid = ObjectId(tx_id)
        except Exception:
            return False

        db = get_database()
        if db is not None:
            try:
                res = await db.transactions.delete_one({"_id": oid, "user_id": user_id})
                return res.deleted_count > 0
            except Exception:
                pass

        sync_db = get_sync_database()
        if sync_db is not None:
            try:
                res = sync_db.transactions.delete_one({"_id": oid, "user_id": user_id})
                return res.deleted_count > 0
            except Exception:
                pass
        return False

    async def get_dashboard_aggregations(self, user_id: str) -> Dict[str, Any]:
        """Execute MongoDB aggregation pipeline for dashboard metrics."""
        sync_db = get_sync_database()
        total_income = 0.0
        total_expenses = 0.0
        category_spending: Dict[str, float] = {}
        recent_txs: List[Dict[str, Any]] = []

        if sync_db is not None:
            try:
                # 1. Total Income & Total Expenses Aggregation Pipeline
                pipeline_totals = [
                    {"$match": {"user_id": user_id}},
                    {"$group": {
                        "_id": "$type",
                        "total": {"$sum": "$amount"},
                        "count": {"$sum": 1}
                    }}
                ]
                results = list(sync_db.transactions.aggregate(pipeline_totals))
                for r in results:
                    if r["_id"] == "INCOME":
                        total_income = float(r["total"])
                    elif r["_id"] == "EXPENSE":
                        total_expenses = float(r["total"])

                # 2. Category Aggregation Pipeline for Expenses
                pipeline_cats = [
                    {"$match": {"user_id": user_id, "type": "EXPENSE"}},
                    {"$group": {
                        "_id": "$category",
                        "total": {"$sum": "$amount"}
                    }},
                    {"$sort": {"total": -1}}
                ]
                cat_results = list(sync_db.transactions.aggregate(pipeline_cats))
                for c in cat_results:
                    category_spending[c["_id"]] = float(c["total"])

                # 3. Recent 10 transactions
                cursor = sync_db.transactions.find({"user_id": user_id}).sort("date", -1).limit(10)
                for doc in cursor:
                    doc["id"] = str(doc["_id"])
                    recent_txs.append(doc)

            except Exception as e:
                logger.warning("MongoDB Aggregation Pipeline error: %s", e)

        net_savings = max(0.0, total_income - total_expenses)
        savings_rate = (net_savings / max(total_income, 1.0)) * 100.0

        return {
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "total_balance": round(total_income - total_expenses, 2),
            "total_savings": round(net_savings, 2),
            "savings_rate_pct": round(savings_rate, 1),
            "category_spending": category_spending,
            "recent_transactions": recent_txs
        }

transaction_repo = TransactionRepository()
