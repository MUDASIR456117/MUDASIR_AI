import pytest
from datetime import datetime
from backend.app.services.ml_service import ml_service
from backend.app.services.health_score_service import health_score_service
from backend.app.services.investment_service import investment_service
from backend.app.services.receipt_service import receipt_service

def test_expense_categorizer():
    cat, conf = ml_service.predict_category("Uber ride to airport", "Uber", 35.0)
    assert cat in ["Transport", "Fuel"]
    assert conf >= 0.50

    cat_g, conf_g = ml_service.predict_category("Whole foods weekly groceries", "Whole Foods", 120.0)
    assert cat_g == "Grocery"
    assert conf_g >= 0.50

def test_fraud_anomaly_detection():
    # Normal spending
    normal_eval = ml_service.check_fraud(amount=45.0, category="Food", merchant="Starbucks")
    assert normal_eval["risk_level"] in ["LOW", "MEDIUM"]
    assert normal_eval["risk_score"] < 60.0

    # Extreme spending spike at 3 AM
    dt_anom = datetime.utcnow().replace(hour=3)
    spike_eval = ml_service.check_fraud(amount=3800.0, category="Shopping", merchant="Apex Foreign Mart", transaction_time=dt_anom)
    assert spike_eval["risk_level"] == "HIGH"
    assert spike_eval["is_anomaly"] is True
    assert len(spike_eval["reasons"]) > 0

def test_credit_risk_evaluation():
    profile = {
        "annual_income": 85000.0,
        "employment_duration_years": 5.0,
        "existing_loans_count": 1,
        "monthly_debt_payments": 400.0,
        "payment_history_on_time_pct": 99.0,
        "credit_utilization_ratio": 18.0,
        "number_of_open_accounts": 6,
        "previous_defaults_count": 0,
        "age": 32
    }
    eval_res = ml_service.evaluate_credit_risk(profile)
    assert eval_res["risk_category"] == "LOW RISK"
    assert eval_res["confidence_score"] >= 0.85
    assert len(eval_res["top_positive_factors"]) > 0
    assert "feature_importance" in eval_res

def test_health_score_service():
    f_data = {
        "monthly_income": 6000.0,
        "monthly_expenses": 2800.0,
        "emergency_savings": 15000.0,
        "monthly_debt": 300.0,
        "budget_limit": 3200.0,
        "spending_volatility_pct": 10.0
    }
    health = health_score_service.calculate_health_score(f_data)
    assert 0 <= health["overall_score"] <= 100
    assert health["category_rating"] in ["EXCELLENT", "GOOD", "FAIR", "POOR"]
    assert len(health["components"]) == 6

def test_investment_risk_profiling():
    prof = {
        "age": 28,
        "investment_horizon_years": 15,
        "risk_tolerance_level": "AGGRESSIVE",
        "emergency_fund_months": 5.0,
        "monthly_income": 6500.0
    }
    inv_res = investment_service.evaluate_risk_profile(prof)
    assert inv_res["classified_profile"] in ["CONSERVATIVE", "MODERATE", "AGGRESSIVE"]
    assert len(inv_res["asset_allocation"]) >= 4

def test_receipt_parsing():
    raw_sample = """
    WALMART SUPERCENTER
    Date: 2026-08-14
    ORGANIC MILK 1GAL   1  $4.89
    TOTAL: $4.89
    PAYMENT: VISA
    """
    parsed = receipt_service.parse_receipt_data(raw_sample)
    assert parsed["merchant"] != ""
    assert parsed["total"] > 0
