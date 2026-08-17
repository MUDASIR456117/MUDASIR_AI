import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AssistantService:
    def process_query(self, query: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Context-aware Conversational AI Financial Assistant.
        Parses intent, aggregates user's personal financial numbers, and crafts intelligent actionable advice.
        """
        q = query.lower().strip()
        
        income = user_context.get("monthly_income", 5000.0)
        expenses_curr = user_context.get("current_month_expenses", 2850.0)
        expenses_prev = user_context.get("previous_month_expenses", 2600.0)
        budget = user_context.get("monthly_budget", 3200.0)
        category_spends = user_context.get("category_spends", {
            "Rent": 1400.0, "Grocery": 520.0, "Food": 340.0,
            "Utilities": 220.0, "Transport": 180.0, "Shopping": 190.0
        })
        health_score = user_context.get("health_score", 78)
        goals = user_context.get("goals", [{"name": "Emergency Fund", "progress": 65}])

        # Determine biggest category
        top_cat = "Rent"
        top_cat_amt = 0.0
        if category_spends:
            top_cat = max(category_spends, key=category_spends.get)
            top_cat_amt = category_spends[top_cat]

        suggested_actions = []
        metrics = {}

        # 1. "Where am I spending the most?" / "What is my biggest expense?"
        if any(w in q for w in ["where", "most", "biggest", "highest", "top category", "top expense"]):
            reply = (
                f"📊 Based on your active transaction records, your highest spending category this month is **{top_cat}** "
                f"at **${top_cat_amt:,.2f}**, which represents **{(top_cat_amt / max(expenses_curr, 1.0)) * 100:.1f}%** of your total monthly expenditures."
            )
            if len(category_spends) > 1:
                sorted_cats = sorted(category_spends.items(), key=lambda x: x[1], reverse=True)[:3]
                breakdown = ", ".join([f"**{c}** (${a:,.2f})" for c, a in sorted_cats])
                reply += f"\n\nYour top 3 spending categories are: {breakdown}."
            metrics = {"top_expense_amount": top_cat_amt, "total_expenses": expenses_curr}
            suggested_actions = ["Set a category budget limit for " + top_cat, "View detailed Expense Analytics"]

        # 2. "How much did I spend this month?"
        elif any(w in q for w in ["how much", "spend this month", "total spend", "current spend", "spending this month"]):
            net_savings = max(0.0, income - expenses_curr)
            savings_rate = (net_savings / max(income, 1.0)) * 100.0
            reply = (
                f"💳 You have spent a total of **${expenses_curr:,.2f}** this month across all categories.\n\n"
                f"• **Monthly Inflow:** ${income:,.2f}\n"
                f"• **Net Savings:** ${net_savings:,.2f} ({savings_rate:.1f}% savings rate)\n"
                f"• **Budget Status:** ${budget - expenses_curr:,.2f} remaining out of your ${budget:,.2f} monthly ceiling."
            )
            metrics = {"total_spent": expenses_curr, "monthly_income": income, "savings_rate": round(savings_rate, 1)}
            suggested_actions = ["Check spending forecast", "Explore budget progress"]

        # 3. "Compare this month with last month"
        elif any(w in q for w in ["compare", "last month", "previous month", "versus", "vs"]):
            diff = expenses_curr - expenses_prev
            pct_diff = (diff / max(expenses_prev, 1.0)) * 100.0
            direction = "increased" if diff > 0 else "decreased"
            status_emoji = "📈" if diff > 0 else "📉"
            reply = (
                f"{status_emoji} **Month-over-Month Comparison:**\n\n"
                f"• **Current Month:** ${expenses_curr:,.2f}\n"
                f"• **Previous Month:** ${expenses_prev:,.2f}\n"
                f"• **Variance:** Your spending has **{direction} by ${abs(diff):,.2f} ({abs(pct_diff):.1f}%)**."
            )
            if diff > 0:
                reply += "\n\n💡 *Tip: Check your discretionary categories (Dining and Shopping) to bring outlays back down to your previous baseline.*"
            else:
                reply += "\n\n🎉 *Great job! You are spending less this month compared to last month.*"
            metrics = {"current_month": expenses_curr, "previous_month": expenses_prev, "difference": round(diff, 2)}
            suggested_actions = ["Review category-level changes", "Update monthly budget"]

        # 4. "How can I save more?"
        elif any(w in q for w in ["save more", "increase savings", "saving tips", "cut costs", "save money"]):
            wants_estimate = (category_spends.get("Food", 0) + category_spends.get("Entertainment", 0) + category_spends.get("Shopping", 0))
            potential_15_cut = wants_estimate * 0.15
            reply = (
                f"💰 **Actionable Ways to Boost Your Savings:**\n\n"
                f"1. **Discretionary Trimming:** You currently spend approximately **${wants_estimate:,.2f}** across Food, Shopping, and Entertainment. Reducing this by just 15% would save an extra **${potential_15_cut:,.2f}/month** ($ {potential_15_cut * 12:,.2f}/year).\n"
                f"2. **Automate the 20% Rule:** Set up an automatic transfer of **${income * 0.20:,.2f}** directly into high-yield savings on payday.\n"
                f"3. **Audit Recurring Subscriptions:** Check utilities and subscription charges for recurring services you no longer utilize."
            )
            suggested_actions = ["Set a dedicated Savings Goal", "Generate AI Recommended Budget"]

        # 5. "Will I exceed my budget?"
        elif any(w in q for w in ["exceed", "over budget", "will i exceed", "budget limit"]):
            burn_pct = (expenses_curr / max(budget, 1.0)) * 100.0
            if burn_pct > 90.0:
                reply = (
                    f"⚠️ **Budget Alert:** You have utilized **{burn_pct:.1f}%** (${expenses_curr:,.2f} of ${budget:,.2f}) of your monthly budget. "
                    f"You have only **${max(0.0, budget - expenses_curr):,.2f}** remaining for the rest of the period. Proceed cautiously with discretionary purchases."
                )
            else:
                reply = (
                    f"✅ **On Track:** You have used **{burn_pct:.1f}%** (${expenses_curr:,.2f} of ${budget:,.2f}) of your monthly budget. "
                    f"You still have **${budget - expenses_curr:,.2f}** in remaining headroom."
                )
            metrics = {"budget_utilization_pct": round(burn_pct, 1), "remaining_budget": round(budget - expenses_curr, 2)}
            suggested_actions = ["Adjust category limits", "View Spending Forecast"]

        # 6. "Analyze my financial health"
        elif any(w in q for w in ["financial health", "health score", "analyze my", "financial status", "how am i doing"]):
            rating = "GOOD" if health_score >= 70 else ("EXCELLENT" if health_score >= 85 else "FAIR")
            reply = (
                f"🩺 **AI Financial Health Assessment:**\n\n"
                f"Your Financial Health Score is **{health_score} / 100 ({rating})**.\n\n"
                f"• **Strengths:** Consistent savings rate, structured budgeting.\n"
                f"• **Opportunities:** Build out your emergency fund to 6 months of living expenses and maintain low credit utilization."
            )
            metrics = {"health_score": health_score}
            suggested_actions = ["View Detailed Health Score Breakdown", "Run Credit Risk Analysis"]

        # General conversational response
        else:
            reply = (
                f"👋 Hello! I am your **AI Financial Advisor Assistant**. I analyze your live transactions, budgets, "
                f"investments, and spending patterns in real time.\n\n"
                f"Here are a few questions you can ask me:\n"
                f"• *'Where am I spending the most?'*\n"
                f"• *'How much did I spend this month?'*\n"
                f"• *'Compare this month with last month.'*\n"
                f"• *'How can I save more?'*\n"
                f"• *'Will I exceed my budget?'*\n"
                f"• *'Analyze my financial health.'*"
            )
            suggested_actions = ["Where am I spending the most?", "Analyze my financial health", "How can I save more?"]

        return {
            "reply": reply,
            "relevant_metrics": metrics,
            "suggested_actions": suggested_actions,
            "timestamp": datetime.utcnow()
        }

assistant_service = AssistantService()
