import os
import json
import random
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

DATASETS_DIR = Path(__file__).resolve().parent / "ml" / "datasets"
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

MERCHANT_CATEGORY_MAP = {
    "Grocery": ["Walmart Supercenter", "Whole Foods Market", "Trader Joe's", "Costco Wholesale", "Kroger", "Safeway"],
    "Food": ["Starbucks", "McDonald's", "Chipotle Mexican Grill", "Subway", "Domino's Pizza", "Tokyo Sushi Lounge", "Uber Eats", "DoorDash"],
    "Rent": ["Skyline Property Management", "Metropolitan Apartments", "Residential Lease Corp"],
    "Utilities": ["Pacific Gas & Electric", "City Water & Sewer Dept", "Verizon Wireless", "AT&T Internet", "Comcast Broadband"],
    "Transport": ["Uber Commute", "Lyft Ride", "Metro Subway Transit", "Central Garage Parking", "EZPass Highway Toll"],
    "Fuel": ["Shell Gas Station", "Chevron Oil", "ExxonMobil", "BP Fuel Mart"],
    "Shopping": ["Amazon.com", "Target Stores", "Nike Athletic Store", "Apple Store", "Best Buy Electronics", "Zara Fashion"],
    "Entertainment": ["Netflix Subscription", "Spotify Premium", "AMC Theatres", "PlayStation Network", "Steam Games Store"],
    "Healthcare": ["CVS Pharmacy", "Walgreens Health", "Bright Dental Clinic", "City Medical Center"],
    "Education": ["State University Tuition", "Coursera Certificate", "Udemy Academy", "Barnes & Noble Books"],
    "Travel": ["Delta Air Lines", "United Airlines", "Marriott Hotel", "Airbnb Vacation Rental"],
    "Salary": ["Enterprise Direct Deposit", "Corporate Payroll LLC"],
    "Freelancing": ["Upwork Client Escrow", "Fiverr International", "Consulting Direct Transfer"],
    "Investment": ["Vanguard Index Fund", "Fidelity Investments", "Robinhood Financial", "Charles Schwab"],
    "Other": ["ATM Cash Withdrawal", "Bank Maintenance Service Fee"]
}

AMOUNT_RANGES = {
    "Grocery": (25.0, 180.0),
    "Food": (8.0, 65.0),
    "Rent": (1200.0, 2200.0),
    "Utilities": (45.0, 190.0),
    "Transport": (12.0, 45.0),
    "Fuel": (35.0, 75.0),
    "Shopping": (15.0, 320.0),
    "Entertainment": (12.0, 80.0),
    "Healthcare": (20.0, 250.0),
    "Education": (40.0, 500.0),
    "Travel": (150.0, 850.0),
    "Salary": (3000.0, 4500.0),
    "Freelancing": (400.0, 1500.0),
    "Investment": (200.0, 1000.0),
    "Other": (10.0, 100.0)
}

def generate_synthetic_transactions(num_records: int = 1500) -> pd.DataFrame:
    print(f"Generating {num_records} realistic synthetic financial transaction records...")
    random.seed(42)
    np.random.seed(42)
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=365)
    
    records = []
    for i in range(num_records):
        random_days = random.randint(0, 365)
        tx_date = start_date + timedelta(days=random_days, hours=random.randint(7, 22), minutes=random.randint(0, 59))
        
        # Determine Type & Category
        r_type = random.choices(["EXPENSE", "INCOME", "INVESTMENT"], weights=[0.82, 0.12, 0.06])[0]
        if r_type == "INCOME":
            cat = random.choice(["Salary", "Freelancing"])
        elif r_type == "INVESTMENT":
            cat = "Investment"
        else:
            cat = random.choices(
                ["Food", "Grocery", "Rent", "Utilities", "Transport", "Fuel", "Shopping", "Entertainment", "Healthcare", "Education", "Travel", "Other"],
                weights=[0.18, 0.16, 0.06, 0.10, 0.10, 0.08, 0.12, 0.08, 0.04, 0.03, 0.03, 0.02]
            )[0]
        
        merchants = MERCHANT_CATEGORY_MAP.get(cat, ["General Retail"])
        merchant = random.choice(merchants)
        
        min_a, max_a = AMOUNT_RANGES.get(cat, (10.0, 100.0))
        amount = round(random.uniform(min_a, max_a), 2)
        
        # Inject 3% synthetic anomalies for fraud detection dataset
        is_fraud = 0
        if r_type == "EXPENSE" and random.random() < 0.03:
            is_fraud = 1
            amount = round(random.uniform(1500.0, 4800.0), 2)
            tx_date = tx_date.replace(hour=random.randint(1, 4)) # Late night timing anomaly
            merchant = "Apex International Luxury Foreign Mart"
        
        description = f"{cat} charge at {merchant}"
        
        records.append({
            "transaction_id": f"TX_{i+1:06d}",
            "date": tx_date.strftime("%Y-%m-%d %H:%M:%S"),
            "type": r_type,
            "category": cat,
            "merchant": merchant,
            "description": description,
            "amount": amount,
            "currency": "USD",
            "payment_method": random.choice(["Credit Card", "Debit Card", "Apple Pay", "Bank Transfer"]),
            "is_fraud": is_fraud
        })
        
    df = pd.DataFrame(records)
    csv_path = DATASETS_DIR / "financial_transactions_synthetic.csv"
    df.to_csv(csv_path, index=False)
    print(f"[✓] Saved synthetic transactions dataset to: {csv_path}")
    return df

def generate_credit_dataset(num_records: int = 3000) -> pd.DataFrame:
    print(f"Generating {num_records} credit risk assessment profiles...")
    np.random.seed(42)
    
    annual_income = np.random.lognormal(mean=10.9, sigma=0.55, size=num_records)
    emp_years = np.random.exponential(scale=4.5, size=num_records)
    existing_loans = np.random.poisson(lam=1.6, size=num_records)
    monthly_debt = (annual_income / 12) * np.random.uniform(0.08, 0.60, size=num_records)
    on_time_pct = np.clip(np.random.normal(loc=93.0, scale=10.0, size=num_records), 0, 100)
    utilization_pct = np.clip(np.random.beta(a=2, b=4, size=num_records) * 100, 0, 100)
    open_accts = np.random.poisson(lam=5, size=num_records) + 1
    previous_defaults = np.random.choice([0, 1, 2], p=[0.85, 0.11, 0.04], size=num_records)
    age = np.random.randint(20, 75, size=num_records)
    
    # Calculate default label
    dti_ratio = (monthly_debt * 12) / np.maximum(annual_income, 10000)
    risk_score_raw = (
        + (100 - on_time_pct) * 0.35
        + utilization_pct * 0.25
        + dti_ratio * 40.0
        + previous_defaults * 25.0
        - np.log1p(annual_income) * 2.0
    )
    risk_tier = np.where(risk_score_raw < 22, "LOW RISK", np.where(risk_score_raw < 42, "MEDIUM RISK", "HIGH RISK"))
    
    df = pd.DataFrame({
        "annual_income": np.round(annual_income, 2),
        "employment_duration_years": np.round(emp_years, 1),
        "existing_loans_count": existing_loans,
        "monthly_debt_payments": np.round(monthly_debt, 2),
        "payment_history_on_time_pct": np.round(on_time_pct, 1),
        "credit_utilization_ratio": np.round(utilization_pct, 1),
        "number_of_open_accounts": open_accts,
        "previous_defaults_count": previous_defaults,
        "age": age,
        "risk_tier": risk_tier
    })
    
    csv_path = DATASETS_DIR / "credit_risk_synthetic.csv"
    df.to_csv(csv_path, index=False)
    print(f"[✓] Saved credit risk synthetic dataset to: {csv_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_transactions(1500)
    generate_credit_dataset(3000)
    print("All synthetic datasets generated successfully.")
