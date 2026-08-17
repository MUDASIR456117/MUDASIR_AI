import numpy as np
from typing import Dict, Any, List
from datetime import datetime

class HealthScoreService:
    def calculate_health_score(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate transparent 0-100 AI Financial Health Score based on 6 key dimensions:
        1. Savings Rate (25 pts)
        2. Expense-to-Income Ratio (20 pts)
        3. Emergency Fund Coverage (15 pts)
        4. Debt Burden / DTI (15 pts)
        5. Budget Adherence (15 pts)
        6. Spending Consistency & Volatility (10 pts)
        """
        income = max(float(financial_data.get("monthly_income", 5000.0)), 100.0)
        expenses = float(financial_data.get("monthly_expenses", 3200.0))
        emergency_savings = float(financial_data.get("emergency_savings", 12000.0))
        monthly_debt = float(financial_data.get("monthly_debt", 400.0))
        budget_limit = float(financial_data.get("budget_limit", 3500.0))
        volatility_pct = float(financial_data.get("spending_volatility_pct", 12.0))

        savings = max(0.0, income - expenses)
        savings_rate = (savings / income) * 100.0
        expense_ratio = (expenses / income) * 100.0
        emergency_months = emergency_savings / max(expenses, 500.0)
        dti_ratio = (monthly_debt / income) * 100.0
        budget_adherence = (expenses / max(budget_limit, 1.0)) * 100.0

        strengths = []
        improvements = []
        components = []

        # 1. Savings Rate (Max 25 pts)
        if savings_rate >= 20.0:
            score_sr = 25.0
            status_sr = "EXCELLENT"
            strengths.append(f"Strong savings rate of {savings_rate:.1f}% (Benchmark: 20%+).")
        elif savings_rate >= 10.0:
            score_sr = 18.0
            status_sr = "GOOD"
        elif savings_rate >= 5.0:
            score_sr = 10.0
            status_sr = "NEEDS IMPROVEMENT"
            improvements.append("Savings rate is under 10%. Aim to automate monthly transfers.")
        else:
            score_sr = 4.0
            status_sr = "CRITICAL"
            improvements.append("Minimal or negative savings rate detected this period.")

        components.append({
            "name": "Savings Rate",
            "score": score_sr,
            "max_score": 25.0,
            "status": status_sr,
            "value_display": f"{savings_rate:.1f}%",
            "benchmark": "20.0% of Net Income"
        })

        # 2. Expense-to-Income Ratio (Max 20 pts)
        if expense_ratio <= 60.0:
            score_er = 20.0
            status_er = "EXCELLENT"
            strengths.append("Controlled monthly expenses relative to total cash inflow.")
        elif expense_ratio <= 80.0:
            score_er = 15.0
            status_er = "GOOD"
        elif expense_ratio <= 95.0:
            score_er = 8.0
            status_er = "NEEDS IMPROVEMENT"
            improvements.append(f"High expense ratio ({expense_ratio:.1f}%). Little buffer for surprises.")
        else:
            score_er = 2.0
            status_er = "CRITICAL"
            improvements.append("Spending exceeds or nears 100% of income. High vulnerability.")

        components.append({
            "name": "Expense-to-Income Ratio",
            "score": score_er,
            "max_score": 20.0,
            "status": status_er,
            "value_display": f"{expense_ratio:.1f}%",
            "benchmark": "< 70.0% of Income"
        })

        # 3. Emergency Fund Coverage (Max 15 pts)
        if emergency_months >= 6.0:
            score_ef = 15.0
            status_ef = "EXCELLENT"
            strengths.append(f"Robust {emergency_months:.1f}-month emergency liquidity cushion.")
        elif emergency_months >= 3.0:
            score_ef = 12.0
            status_ef = "GOOD"
            strengths.append(f"Solid {emergency_months:.1f} months of expenses saved.")
        elif emergency_months >= 1.0:
            score_ef = 6.0
            status_ef = "NEEDS IMPROVEMENT"
            improvements.append(f"Emergency reserve is only {emergency_months:.1f} months. Target 3-6 months.")
        else:
            score_ef = 2.0
            status_ef = "CRITICAL"
            improvements.append("Emergency fund has less than 1 month of living expenses.")

        components.append({
            "name": "Emergency Fund Cushion",
            "score": score_ef,
            "max_score": 15.0,
            "status": status_ef,
            "value_display": f"{emergency_months:.1f} Months",
            "benchmark": "3 - 6 Months of Expenses"
        })

        # 4. Debt Burden / DTI (Max 15 pts)
        if dti_ratio <= 15.0:
            score_dti = 15.0
            status_dti = "EXCELLENT"
            strengths.append(f"Low debt obligations ({dti_ratio:.1f}% of income).")
        elif dti_ratio <= 30.0:
            score_dti = 11.0
            status_dti = "GOOD"
        elif dti_ratio <= 45.0:
            score_dti = 6.0
            status_dti = "NEEDS IMPROVEMENT"
            improvements.append(f"Moderate debt payments consuming {dti_ratio:.1f}% of income.")
        else:
            score_dti = 2.0
            status_dti = "CRITICAL"
            improvements.append(f"Heavy debt burden ({dti_ratio:.1f}%). Focus on high-interest paydown.")

        components.append({
            "name": "Debt-to-Income (DTI)",
            "score": score_dti,
            "max_score": 15.0,
            "status": status_dti,
            "value_display": f"{dti_ratio:.1f}%",
            "benchmark": "< 20.0% of Income"
        })

        # 5. Budget Adherence (Max 15 pts)
        if budget_adherence <= 90.0:
            score_ba = 15.0
            status_ba = "EXCELLENT"
            strengths.append(f"Strict budget discipline ({budget_adherence:.1f}% of cap used).")
        elif budget_adherence <= 100.0:
            score_ba = 12.0
            status_ba = "GOOD"
        elif budget_adherence <= 115.0:
            score_ba = 5.0
            status_ba = "NEEDS IMPROVEMENT"
            improvements.append(f"Over budget by {budget_adherence - 100.0:.1f}%. Review discretionary discretionary outlays.")
        else:
            score_ba = 1.0
            status_ba = "CRITICAL"
            improvements.append("Substantial budget overrun recorded.")

        components.append({
            "name": "Budget Adherence",
            "score": score_ba,
            "max_score": 15.0,
            "status": status_ba,
            "value_display": f"{budget_adherence:.1f}%",
            "benchmark": "< 100.0% of Target Budget"
        })

        # 6. Spending Consistency (Max 10 pts)
        if volatility_pct <= 15.0:
            score_sc = 10.0
            status_sc = "EXCELLENT"
        elif volatility_pct <= 30.0:
            score_sc = 7.0
            status_sc = "GOOD"
        else:
            score_sc = 3.0
            status_sc = "NEEDS IMPROVEMENT"
            improvements.append("High spending volatility across weeks creates cashflow unpredictability.")

        components.append({
            "name": "Spending Stability",
            "score": score_sc,
            "max_score": 10.0,
            "status": status_sc,
            "value_display": f"±{volatility_pct:.1f}%",
            "benchmark": "< 15.0% Volatility"
        })

        total_score = int(score_sr + score_er + score_ef + score_dti + score_ba + score_sc)
        total_score = int(np.clip(total_score, 0, 100))

        if total_score >= 85:
            rating = "EXCELLENT"
        elif total_score >= 70:
            rating = "GOOD"
        elif total_score >= 50:
            rating = "FAIR"
        else:
            rating = "POOR"

        return {
            "overall_score": total_score,
            "category_rating": rating,
            "components": components,
            "strengths": strengths if strengths else ["Active tracking established"],
            "improvements": improvements if improvements else ["Maintain current prudent financial habits"],
            "calculated_at": datetime.utcnow()
        }

health_score_service = HealthScoreService()
