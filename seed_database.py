import os
import sys
from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import MongoClient
from backend.app.config import settings
from backend.app.security.password import get_password_hash

def seed_database():
    print(f"Connecting to MongoDB database '{settings.DATABASE_NAME}' at {settings.MONGODB_URI}...")
    try:
        client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2500)
        client.admin.command('ping')
        db = client[settings.DATABASE_NAME]
        print("Connected to MongoDB successfully.")
    except Exception as e:
        print(f"Notice: MongoDB not currently reachable on localhost:27017 ({e}).")
        print("This is normal if running in containerized or offline demonstration mode.")
        return

    print("Seeding demo users, transactions, portfolios, budgets, and goals...")

    # 1. Clear existing demo collections
    db.users.delete_many({"email": {"$in": ["demo@financialadvisor.ai", "admin@financialadvisor.ai"]}})
    
    # 2. Insert Users
    demo_user_id = ObjectId("66c0ffee66c0ffee66c0ffee")
    admin_user_id = ObjectId("66c0ffee66c0ffee66c0ff00")

    users_data = [
        {
            "_id": demo_user_id,
            "username": "demouser",
            "email": "demo@financialadvisor.ai",
            "full_name": "Alex Mercer",
            "hashed_password": get_password_hash("Demo@12345"),
            "role": "USER",
            "is_active": True,
            "monthly_income": 6500.0,
            "risk_tolerance": "MODERATE",
            "created_at": datetime.utcnow()
        },
        {
            "_id": admin_user_id,
            "username": "admin",
            "email": "admin@financialadvisor.ai",
            "full_name": "System Administrator",
            "hashed_password": get_password_hash("Admin@12345"),
            "role": "ADMIN",
            "is_active": True,
            "monthly_income": 10000.0,
            "risk_tolerance": "AGGRESSIVE",
            "created_at": datetime.utcnow()
        }
    ]
    db.users.insert_many(users_data)
    print(f"[✓] Seeded {len(users_data)} users.")

    # 3. Seed Transactions for Demo User
    db.transactions.delete_many({"user_id": str(demo_user_id)})
    
    tx_list = [
        {"desc": "Bi-weekly Payroll Salary", "merch": "Acme Tech Corp", "cat": "Salary", "type": "INCOME", "amt": 3250.0, "days_ago": 1},
        {"desc": "Organic supermarket shopping", "merch": "Whole Foods Market", "cat": "Grocery", "type": "EXPENSE", "amt": 142.50, "days_ago": 2},
        {"desc": "Monthly apartment rent lease", "merch": "Skyline Properties", "cat": "Rent", "type": "EXPENSE", "amt": 1400.0, "days_ago": 5},
        {"desc": "Espresso coffee and pastries", "merch": "Starbucks Coffee", "cat": "Food", "type": "EXPENSE", "amt": 18.75, "days_ago": 3},
        {"desc": "Unleaded fuel gasoline", "merch": "Shell Gas Station", "cat": "Fuel", "type": "EXPENSE", "amt": 55.00, "days_ago": 4},
        {"desc": "Electric & heating utility bill", "merch": "City Power & Gas", "cat": "Utilities", "type": "EXPENSE", "amt": 115.00, "days_ago": 7},
        {"desc": "Electronics accessories purchase", "merch": "Amazon", "cat": "Shopping", "type": "EXPENSE", "amt": 78.40, "days_ago": 6},
        {"desc": "Monthly streaming video subscription", "merch": "Netflix", "cat": "Entertainment", "type": "EXPENSE", "amt": 19.99, "days_ago": 9},
        {"desc": "Client software consulting bonus", "merch": "Apex Consulting", "cat": "Freelancing", "type": "INCOME", "amt": 850.0, "days_ago": 11},
        {"desc": "Pharmacy prescriptions", "merch": "CVS Pharmacy", "cat": "Healthcare", "type": "EXPENSE", "amt": 35.20, "days_ago": 12},
        {"desc": "Subway transit commuter card", "merch": "Metro Transit", "cat": "Transport", "type": "EXPENSE", "amt": 45.00, "days_ago": 14},
        {"desc": "Index fund automatic contribution", "merch": "Vanguard ETF", "cat": "Investment", "type": "INVESTMENT", "amt": 500.0, "days_ago": 15}
    ]

    tx_docs = []
    now = datetime.utcnow()
    for tx in tx_list:
        tx_date = now - timedelta(days=tx["days_ago"])
        tx_docs.append({
            "user_id": str(demo_user_id),
            "type": tx["type"],
            "category": tx["cat"],
            "amount": tx["amt"],
            "currency": "USD",
            "description": tx["desc"],
            "merchant": tx["merch"],
            "date": tx_date,
            "payment_method": "Credit Card" if tx["type"] == "EXPENSE" else "Direct Deposit",
            "location": "Online" if "Amazon" in tx["merch"] or "Netflix" in tx["merch"] else "In-Store",
            "status": "COMPLETED",
            "is_anomaly": False,
            "anomaly_score": 10.0,
            "created_at": tx_date
        })

    db.transactions.insert_many(tx_docs)
    print(f"[✓] Seeded {len(tx_docs)} transactions.")

    # 4. Seed Goals
    db.financial_goals.delete_many({"user_id": str(demo_user_id)})
    goals_data = [
        {"user_id": str(demo_user_id), "name": "Emergency Fund (6 Months)", "target_amount": 18000.0, "current_amount": 12500.0, "target_date": datetime(2026, 12, 31), "monthly_contribution": 750.0, "category": "Emergency", "status": "IN_PROGRESS", "created_at": now},
        {"user_id": str(demo_user_id), "name": "Tech Gadget Upgrade (MacBook / GPU)", "target_amount": 3200.0, "current_amount": 2400.0, "target_date": datetime(2026, 10, 15), "monthly_contribution": 400.0, "category": "Gadgets", "status": "IN_PROGRESS", "created_at": now},
        {"user_id": str(demo_user_id), "name": "Europe Vacation Trip", "target_amount": 5000.0, "current_amount": 1800.0, "target_date": datetime(2027, 6, 1), "monthly_contribution": 350.0, "category": "Travel", "status": "IN_PROGRESS", "created_at": now}
    ]
    db.financial_goals.insert_many(goals_data)
    print(f"[✓] Seeded {len(goals_data)} financial goals.")

    # 5. Seed Portfolio Holdings
    db.portfolios.delete_many({"user_id": str(demo_user_id)})
    holdings_data = [
        {"user_id": str(demo_user_id), "symbol": "VOO", "name": "Vanguard S&P 500 ETF", "asset_type": "ETF", "quantity": 15.0, "purchase_price": 420.0, "current_price": 490.50},
        {"user_id": str(demo_user_id), "symbol": "MSFT", "name": "Microsoft Corporation", "asset_type": "Stock", "quantity": 10.0, "purchase_price": 380.0, "current_price": 425.00},
        {"user_id": str(demo_user_id), "symbol": "BND", "name": "Vanguard Total Bond Market", "asset_type": "Bond", "quantity": 40.0, "purchase_price": 72.0, "current_price": 74.50},
        {"user_id": str(demo_user_id), "symbol": "GLD", "name": "SPDR Gold Trust", "asset_type": "Gold", "quantity": 8.0, "purchase_price": 195.0, "current_price": 218.00}
    ]
    db.portfolios.insert_many(holdings_data)
    print(f"[✓] Seeded {len(holdings_data)} investment portfolio holdings.")

    print("\n==========================================================")
    print("Database seeding completed successfully.")
    print("Demo User:  demo@financialadvisor.ai  | Password: Demo@12345")
    print("Admin User: admin@financialadvisor.ai | Password: Admin@12345")
    print("==========================================================")

if __name__ == "__main__":
    seed_database()
