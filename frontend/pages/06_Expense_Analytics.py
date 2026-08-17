import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from frontend.services.api_client import api_client
from frontend.components.kpi_card import render_kpi_card

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">📉 Expense Analytics & Deep Dive</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Granular category breakdowns, discretionary ratio tracking, and historical expenditure patterns.</p>", unsafe_allow_html=True)

metrics = api_client.get_dashboard_metrics(token)
cat_spending = metrics.get("category_spending", {})
total_exp = metrics.get("kpis", {}).get("total_expenses", 2850.0)

# Needs vs Wants calculation
needs_cats = ["Rent", "Grocery", "Utilities", "Healthcare", "Transport", "Fuel"]
needs_sum = sum(amt for cat, amt in cat_spending.items() if cat in needs_cats)
wants_sum = sum(amt for cat, amt in cat_spending.items() if cat not in needs_cats)
needs_pct = (needs_sum / max(total_exp, 1.0)) * 100.0
wants_pct = (wants_sum / max(total_exp, 1.0)) * 100.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Expenditures", f"${total_exp:,.2f}", badge_text="Current Month", variant="rose")
with c2:
    render_kpi_card("Essential Needs (50% Target)", f"${needs_sum:,.2f}", badge_text=f"{needs_pct:.1f}% of Total", badge_type="success" if needs_pct <= 55 else "warning", variant="blue")
with c3:
    render_kpi_card("Discretionary Wants (30% Target)", f"${wants_sum:,.2f}", badge_text=f"{wants_pct:.1f}% of Total", badge_type="success" if wants_pct <= 35 else "danger", variant="amber")
with c4:
    top_cat = max(cat_spending, key=cat_spending.get) if cat_spending else "Rent"
    render_kpi_card("Top Cost Driver", f"{top_cat}", badge_text=f"${cat_spending.get(top_cat, 0):,.2f}", variant="purple")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 0.8], gap="medium")

with col1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Category Expenditure Ranking (Pareto Distribution)")
    df_cat = pd.DataFrame(list(cat_spending.items()), columns=["Category", "Amount"]).sort_values("Amount", ascending=True)
    fig_bar = px.bar(
        df_cat, x="Amount", y="Category", orientation="h",
        color="Amount", color_continuous_scale="Blues",
        text_auto="$.2f"
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(18, 24, 38, 0.4)",
        plot_bgcolor="rgba(18, 24, 38, 0.4)",
        font=dict(color="#F8FAFC"),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickprefix="$")
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Needs vs Wants Proportion")
    fig_nw = go.Figure(data=[go.Pie(
        labels=["Essential Needs", "Discretionary Wants"],
        values=[needs_sum, wants_sum],
        hole=0.5,
        marker_colors=["#3B82F6", "#F59E0B"],
        textinfo="label+percent"
    )])
    fig_nw.update_layout(
        paper_bgcolor="rgba(18, 24, 38, 0.4)",
        plot_bgcolor="rgba(18, 24, 38, 0.4)",
        font=dict(color="#F8FAFC")
    )
    st.plotly_chart(fig_nw, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
