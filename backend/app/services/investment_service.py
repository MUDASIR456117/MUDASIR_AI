from typing import Dict, Any, List
import numpy as np

class InvestmentService:
    def evaluate_risk_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify user investment risk profile and generate tailored educational asset allocations.
        """
        age = profile_data.get("age", 30)
        horizon = profile_data.get("investment_horizon_years", 10)
        tolerance = profile_data.get("risk_tolerance_level", "MODERATE").upper()
        emergency_months = profile_data.get("emergency_fund_months", 3.0)
        monthly_income = profile_data.get("monthly_income", 5000.0)

        # Risk scoring algorithm (0 - 100)
        score = 50.0
        # Age factor: younger investors have more time to bear market volatility
        score += max(0, (65 - age) * 0.4)
        # Horizon factor
        score += min(horizon, 20) * 1.2
        # Emergency fund safety factor
        if emergency_months < 3.0:
            score -= 15.0
        elif emergency_months >= 6.0:
            score += 10.0
        # Tolerance adjustment
        if "CONSERVATIVE" in tolerance:
            score -= 20.0
        elif "AGGRESSIVE" in tolerance:
            score += 20.0

        score = float(np.clip(score, 10.0, 95.0))

        if score < 40.0:
            profile_class = "CONSERVATIVE"
            return_range = "4.0% - 6.5% Annual Est."
            allocations = [
                {"asset_class": "High-Yield Savings & Cash", "allocation_pct": 25.0, "recommended_amount": round(monthly_income * 0.25, 2), "description": "Liquid principal protection", "expected_volatility": "Very Low"},
                {"asset_class": "Government & Corporate Bonds", "allocation_pct": 40.0, "recommended_amount": round(monthly_income * 0.40, 2), "description": "Fixed income yield", "expected_volatility": "Low"},
                {"asset_class": "Broad Market Index ETFs (S&P 500 / Total Market)", "allocation_pct": 25.0, "recommended_amount": round(monthly_income * 0.25, 2), "description": "Moderate equity growth", "expected_volatility": "Moderate"},
                {"asset_class": "Physical Gold / Commodities", "allocation_pct": 10.0, "recommended_amount": round(monthly_income * 0.10, 2), "description": "Inflation hedge", "expected_volatility": "Moderate"}
            ]
            insights = [
                "Focus on capital preservation and downside stability.",
                "High allocation to fixed income dampens equity market drawdowns.",
                "Ensure emergency reserves remain liquid in high-yield cash equivalents."
            ]
        elif score < 70.0:
            profile_class = "MODERATE"
            return_range = "6.5% - 9.0% Annual Est."
            allocations = [
                {"asset_class": "High-Yield Savings & Cash", "allocation_pct": 10.0, "recommended_amount": round(monthly_income * 0.10, 2), "description": "Liquidity buffer", "expected_volatility": "Very Low"},
                {"asset_class": "Fixed Income & Intermediate Bonds", "allocation_pct": 20.0, "recommended_amount": round(monthly_income * 0.20, 2), "description": "Bond laddering stability", "expected_volatility": "Low"},
                {"asset_class": "Large-Cap & Total Stock Market ETFs", "allocation_pct": 45.0, "recommended_amount": round(monthly_income * 0.45, 2), "description": "Core long-term growth", "expected_volatility": "Moderate to High"},
                {"asset_class": "International & Emerging Markets", "allocation_pct": 15.0, "recommended_amount": round(monthly_income * 0.15, 2), "description": "Geographic diversification", "expected_volatility": "High"},
                {"asset_class": "Gold & Real Assets (REITs)", "allocation_pct": 10.0, "recommended_amount": round(monthly_income * 0.10, 2), "description": "Non-correlated real returns", "expected_volatility": "Moderate"}
            ]
            insights = [
                "Balanced growth strategy capturing upside while buffering recessions.",
                "Dollar-cost averaging into low-cost index funds is recommended.",
                "Rebalance portfolio semi-annually to maintain target percentages."
            ]
        else:
            profile_class = "AGGRESSIVE"
            return_range = "8.5% - 12.0% Annual Est."
            allocations = [
                {"asset_class": "Cash Equivalents", "allocation_pct": 5.0, "recommended_amount": round(monthly_income * 0.05, 2), "description": "Tactical liquidity", "expected_volatility": "Very Low"},
                {"asset_class": "Large-Cap Core Equities (VTI/VOO)", "allocation_pct": 40.0, "recommended_amount": round(monthly_income * 0.40, 2), "description": "Equities core engine", "expected_volatility": "Moderate to High"},
                {"asset_class": "High-Growth Tech & Small-Cap Stocks", "allocation_pct": 30.0, "recommended_amount": round(monthly_income * 0.30, 2), "description": "Maximum capital appreciation", "expected_volatility": "High"},
                {"asset_class": "International & Emerging Markets", "allocation_pct": 15.0, "recommended_amount": round(monthly_income * 0.15, 2), "description": "Global upside expansion", "expected_volatility": "High"},
                {"asset_class": "Alternative Assets (Gold/Crypto)", "allocation_pct": 10.0, "recommended_amount": round(monthly_income * 0.10, 2), "description": "High-beta alternative growth", "expected_volatility": "Very High"}
            ]
            insights = [
                "Optimized for maximum compounding over long horizons (>7 years).",
                "Requires emotional tolerance for 15-30% short-term market drawdowns.",
                "Strong emphasis on equity and disruptive innovation sectors."
            ]

        return {
            "classified_profile": profile_class,
            "profile_score": round(score, 1),
            "target_annual_return_range": return_range,
            "asset_allocation": allocations,
            "insights": insights,
            "disclaimer": "This application provides educational and analytical information and is not a substitute for advice from a licensed financial professional. No guaranteed returns."
        }

    def analyze_portfolio(self, holdings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute portfolio gain/loss, asset distribution, and concentration risk."""
        if not holdings:
            return {
                "total_invested": 0.0,
                "current_value": 0.0,
                "total_gain_loss": 0.0,
                "total_gain_loss_pct": 0.0,
                "holdings": [],
                "allocation_by_type": {},
                "concentration_risk": "Low",
                "risk_indicators": ["No investment holdings recorded yet."]
            }

        total_invested = 0.0
        current_value = 0.0
        type_values: Dict[str, float] = {}

        processed_holdings = []
        for h in holdings:
            qty = float(h.get("quantity", 0.0))
            buy_p = float(h.get("purchase_price", 0.0))
            cur_p = float(h.get("current_price", 0.0))
            cost = qty * buy_p
            val = qty * cur_p
            total_invested += cost
            current_value += val

            atype = h.get("asset_type", "Stock")
            type_values[atype] = type_values.get(atype, 0.0) + val

            gain = val - cost
            gain_pct = (gain / max(cost, 1.0)) * 100.0
            
            item = dict(h)
            item["invested_total"] = round(cost, 2)
            item["current_total"] = round(val, 2)
            item["gain_loss"] = round(gain, 2)
            item["gain_loss_pct"] = round(gain_pct, 2)
            processed_holdings.append(item)

        gain_loss = current_value - total_invested
        gain_loss_pct = (gain_loss / max(total_invested, 1.0)) * 100.0

        # Allocation percentages
        allocations = {}
        for atype, amt in type_values.items():
            allocations[atype] = round((amt / max(current_value, 1.0)) * 100.0, 1)

        # Concentration risk check
        risk_indicators = []
        concentration_risk = "Low"
        for atype, pct in allocations.items():
            if pct >= 50.0:
                concentration_risk = "High"
                risk_indicators.append(f"Heavy concentration: {pct}% of portfolio is in '{atype}'.")
            elif pct >= 35.0 and concentration_risk != "High":
                concentration_risk = "Moderate"
                risk_indicators.append(f"Moderate concentration in '{atype}' ({pct}%).")

        if not risk_indicators:
            risk_indicators.append("Well-diversified asset class allocation across holdings.")

        return {
            "total_invested": round(total_invested, 2),
            "current_value": round(current_value, 2),
            "total_gain_loss": round(gain_loss, 2),
            "total_gain_loss_pct": round(gain_loss_pct, 2),
            "holdings": processed_holdings,
            "allocation_by_type": allocations,
            "concentration_risk": concentration_risk,
            "risk_indicators": risk_indicators
        }

investment_service = InvestmentService()
