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

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">🧠 AI Smart Budget Planner</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Adaptive mathematical budgeting balancing 50/30/20 principles with your live empirical spending history.</p>", unsafe_allow_html=True)

budget_status = api_client.get_budget_status(token)
total_spent = budget_status.get("total_spent", 2850.0)
monthly_budget = budget_status.get("monthly_budget", 3500.0)
remaining = budget_status.get("remaining_budget", 650.0)
pct_used = budget_status.get("percentage_used", 81.4)

# KPI Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Monthly Budget Limit", f"${monthly_budget:,.2f}", badge_text="Total Cap", variant="blue")
with c2:
    render_kpi_card("Current Total Spent", f"${total_spent:,.2f}", badge_text=f"{pct_used}% Burned", badge_type="warning" if pct_used > 80 else "success", variant="rose")
with c3:
    render_kpi_card("Remaining Safety Buffer", f"${remaining:,.2f}", badge_text="Headroom", badge_type="success" if remaining > 0 else "danger", variant="emerald")
with c4:
    render_kpi_card("Emergency Target (3 Mo)", "$15,000.00", badge_text="Optimal Buffer", variant="purple")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Overspending Warnings
warnings = budget_status.get("warnings", [])
for w in warnings:
    st.warning(f"⚠️ {w}")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.subheader("Category-Level Budget Limits & Progress")

cats = budget_status.get("categories", [])
for item in cats:
    cat_name = item.get("category", "Unknown")
    limit = item.get("budget_limit", 500.0)
    spent = item.get("actual_spent", 0.0)
    pct = min(1.0, spent / max(limit, 1.0))
    rem = max(0.0, limit - spent)
    
    col_label, col_prog, col_stats = st.columns([1, 2, 1])
    with col_label:
        st.markdown(f"**{cat_name}**")
    with col_prog:
        bar_color = "red" if spent > limit else "blue"
        st.progress(pct)
    with col_stats:
        status_text = f"🚨 Over by ${spent-limit:.2f}" if spent > limit else f"${rem:.2f} left"
        st.markdown(f"${spent:,.2f} / ${limit:,.2f} • *{status_text}*")

st.markdown('</div>', unsafe_allow_html=True)
