import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st
import pandas as pd
from frontend.services.api_client import api_client
from frontend.components.kpi_card import render_kpi_card, render_ai_insight
from frontend.components.charts import (
    create_income_vs_expense_chart,
    create_category_donut_chart,
    create_forecast_ribbon_chart
)

token = st.session_state.get("token", "")
metrics = api_client.get_dashboard_metrics(token)
kpis = metrics.get("kpis", {})

# Header Section
st.markdown('<div class="brand-header">💎 Executive Financial Dashboard</div>', unsafe_allow_html=True)
st.markdown(f"<p style='color: #94A3B8;'>Real-time AI-powered financial monitoring for <b>{st.session_state.get('user', {}).get('full_name', 'Alex Mercer')}</b>.</p>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. KPI CARDS GRID (Rows of 5)
# -------------------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    render_kpi_card(
        title="Total Balance",
        value=f"${kpis.get('total_balance', 3650.0):,.2f}",
        badge_text="Live Liquid",
        badge_type="info",
        variant="blue"
    )
with c2:
    render_kpi_card(
        title="Monthly Income",
        value=f"${kpis.get('total_income', 6500.0):,.2f}",
        badge_text="+4.8% MoM",
        badge_type="success",
        variant="emerald"
    )
with c3:
    render_kpi_card(
        title="Monthly Expenses",
        value=f"${kpis.get('total_expenses', 2850.0):,.2f}",
        badge_text="Tracked",
        badge_type="warning",
        variant="rose"
    )
with c4:
    render_kpi_card(
        title="Net Savings",
        value=f"${kpis.get('total_savings', 3650.0):,.2f}",
        badge_text=f"{kpis.get('savings_rate_pct', 56.2)}% Rate",
        badge_type="success",
        variant="emerald"
    )
with c5:
    render_kpi_card(
        title="Monthly Budget",
        value=f"${kpis.get('monthly_budget', 3500.0):,.2f}",
        badge_text=f"{kpis.get('budget_used_pct', 81.4)}% Used",
        badge_type="info",
        variant="amber"
    )

# Second row of KPIs
c6, c7, c8, c9, c10 = st.columns(5)

with c6:
    render_kpi_card(
        title="Investment Portfolio",
        value=f"${kpis.get('investment_value', 18450.0):,.2f}",
        badge_text="+14.2% Return",
        badge_type="success",
        variant="purple"
    )
with c7:
    render_kpi_card(
        title="Credit Risk Tier",
        value="LOW RISK",
        badge_text="Score: 765",
        badge_type="success",
        variant="emerald"
    )
with c8:
    render_kpi_card(
        title="Fraud Anomalies",
        value=f"{kpis.get('fraud_alerts_count', 0)} Active",
        badge_text="Shielded",
        badge_type="info",
        variant="blue"
    )
with c9:
    render_kpi_card(
        title="Health Score",
        value=f"{kpis.get('financial_health_score', 82)} / 100",
        badge_text=kpis.get("health_rating", "EXCELLENT"),
        badge_type="success",
        variant="emerald"
    )
with c10:
    render_kpi_card(
        title="Emergency Runway",
        value="5.2 Months",
        badge_text="Healthy Target",
        badge_type="success",
        variant="blue"
    )

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. AI GENERATED DYNAMIC INSIGHTS
# -------------------------------------------------------------
st.subheader("🧠 Proactive AI Financial Intelligence")
insights = metrics.get("ai_insights", [])
icols = st.columns(len(insights) if insights else 1)
for idx, ins in enumerate(insights):
    with icols[idx]:
        render_ai_insight(ins, icon="⚡", tag=f"Signal {idx+1}")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. INTERACTIVE VISUALIZATIONS
# -------------------------------------------------------------
col_chart1, col_chart2 = st.columns([1.3, 0.9], gap="medium")

with col_chart1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    monthly_trend = metrics.get("monthly_trend", [])
    fig_flow = create_income_vs_expense_chart(monthly_trend)
    st.plotly_chart(fig_flow, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    cat_spending = metrics.get("category_spending", {})
    fig_donut = create_category_donut_chart(cat_spending)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. RECENT TRANSACTIONS TABLE
# -------------------------------------------------------------
st.subheader("💳 Recent Financial Activity")
recent_txs = metrics.get("recent_transactions", [])
if recent_txs:
    df_tx = pd.DataFrame(recent_txs)
    show_cols = [c for c in ["date", "merchant", "description", "category", "type", "amount", "status"] if c in df_tx.columns]
    st.dataframe(
        df_tx[show_cols],
        column_config={
            "amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
            "date": st.column_config.DateColumn("Date")
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No transaction records available. Add a transaction or scan a receipt to get started.")
