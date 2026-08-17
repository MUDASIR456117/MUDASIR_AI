from typing import Dict, Any, List
from datetime import datetime

class BudgetService:
    def generate_smart_budget_recommendation(
        self,
        monthly_income: float,
        historical_category_spends: Dict[str, float] = None,
        savings_goal_monthly: float = 0.0
    ) -> Dict[str, Any]:
        """
        Generate intelligent dynamic budget recommendation.
        Combines 50/30/20 standard baseline with user's empirical category history.
        """
        income = max(monthly_income, 500.0)
        
        # 50/30/20 allocations
        needs_budget = round(income * 0.50, 2)
        wants_budget = round(income * 0.30, 2)
        savings_target = round(max(income * 0.20, savings_goal_monthly), 2)
        emergency_fund_target = round(income * 3.0, 2)

        # Baseline category allocations adjusted to income
        category_allocations = {
            "Rent": round(income * 0.30, 2),
            "Grocery": round(income * 0.12, 2),
            "Utilities": round(income * 0.08, 2),
            "Food": round(income * 0.08, 2),
            "Transport": round(income * 0.07, 2),
            "Fuel": round(income * 0.05, 2),
            "Shopping": round(income * 0.06, 2),
            "Entertainment": round(income * 0.04, 2),
            "Healthcare": round(income * 0.04, 2),
            "Education": round(income * 0.03, 2),
            "Travel": round(income * 0.03, 2),
            "Other": round(income * 0.02, 2)
        }

        # Check for overspending warnings if historical spending is supplied
        warnings = []
        if historical_category_spends:
            for cat, actual_spent in historical_category_spends.items():
                rec_limit = category_allocations.get(cat, income * 0.05)
                if actual_spent > rec_limit * 1.15:
                    pct_over = ((actual_spent - rec_limit) / rec_limit) * 100.0
                    warnings.append(
                        f"Overspending in '{cat}': currently ${actual_spent:,.2f} vs recommended limit of ${rec_limit:,.2f} (+{pct_over:.1f}%)."
                    )

        if not warnings:
            warnings.append("All category allocations are within target financial guardrails.")

        return {
            "monthly_income": income,
            "recommended_total_budget": round(needs_budget + wants_budget, 2),
            "needs_budget": needs_budget,
            "wants_budget": wants_budget,
            "savings_target": savings_target,
            "emergency_fund_target": emergency_fund_target,
            "category_allocations": category_allocations,
            "overspending_warnings": warnings
        }

budget_service = BudgetService()
