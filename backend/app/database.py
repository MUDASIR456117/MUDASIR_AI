import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.database import Database as SyncDatabase
from backend.app.config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.async_client: AsyncIOMotorClient | None = None
        self.async_db: AsyncIOMotorDatabase | None = None
        self.sync_client: MongoClient | None = None
        self.sync_db: SyncDatabase | None = None
        self.is_connected: bool = False

    def connect(self):
        try:
            # Synchronous PyMongo client
            self.sync_client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            # Ping database to verify connection
            self.sync_client.admin.command('ping')
            self.sync_db = self.sync_client[settings.DATABASE_NAME]

            # Asynchronous Motor client
            self.async_client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            self.async_db = self.async_client[settings.DATABASE_NAME]
            self.is_connected = True
            logger.info("Successfully connected to MongoDB: %s", settings.DATABASE_NAME)
            self.create_indexes()
        except Exception as e:
            logger.warning("MongoDB connection failed or unavailable (%s). Falling back to mock-capable mode.", e)
            self.is_connected = False

    def create_indexes(self):
        """Create necessary indexes on collections."""
        if not self.is_connected or self.sync_db is None:
            return
        try:
            # Users: unique email & username
            self.sync_db.users.create_index([("email", ASCENDING)], unique=True)
            self.sync_db.users.create_index([("username", ASCENDING)], unique=True)

            # Transactions: user_id, date, category, status
            self.sync_db.transactions.create_index([("user_id", ASCENDING), ("date", DESCENDING)])
            self.sync_db.transactions.create_index([("category", ASCENDING)])
            self.sync_db.transactions.create_index([("type", ASCENDING)])
            self.sync_db.transactions.create_index([("created_at", DESCENDING)])
            self.sync_db.transactions.create_index([("description", TEXT), ("merchant", TEXT)])

            # Income & Expenses
            self.sync_db.income.create_index([("user_id", ASCENDING), ("date", DESCENDING)])
            self.sync_db.expenses.create_index([("user_id", ASCENDING), ("date", DESCENDING)])

            # Budgets & Goals
            self.sync_db.budgets.create_index([("user_id", ASCENDING), ("year", ASCENDING), ("month", ASCENDING)], unique=True)
            self.sync_db.financial_goals.create_index([("user_id", ASCENDING), ("status", ASCENDING)])

            # Receipts & Fraud alerts
            self.sync_db.receipts.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])
            self.sync_db.fraud_alerts.create_index([("user_id", ASCENDING), ("risk_level", ASCENDING)])

            # Credit & Investments
            self.sync_db.credit_profiles.create_index([("user_id", ASCENDING)], unique=True)
            self.sync_db.investments.create_index([("user_id", ASCENDING)])
            self.sync_db.portfolios.create_index([("user_id", ASCENDING)])

            # Audit logs & Chat
            self.sync_db.chat_history.create_index([("user_id", ASCENDING), ("timestamp", ASCENDING)])
            self.sync_db.audit_logs.create_index([("timestamp", DESCENDING)])
            self.sync_db.notifications.create_index([("user_id", ASCENDING), ("read", ASCENDING)])

            logger.info("MongoDB indexes verified successfully.")
        except Exception as e:
            logger.warning("Error creating MongoDB indexes: %s", e)

    def close(self):
        if self.async_client:
            self.async_client.close()
        if self.sync_client:
            self.sync_client.close()
        self.is_connected = False
        logger.info("MongoDB connection closed.")

db_manager = DatabaseManager()

def get_database() -> AsyncIOMotorDatabase:
    if db_manager.async_db is None:
        db_manager.connect()
    return db_manager.async_db

def get_sync_database() -> SyncDatabase:
    if db_manager.sync_db is None:
        db_manager.connect()
    return db_manager.sync_db
