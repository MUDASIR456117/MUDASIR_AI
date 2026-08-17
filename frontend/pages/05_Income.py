import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st
import pandas as pd
import plotly.express as px
from frontend.services.api_client import api_client
from frontend.components.kpi_card import render_kpi_card

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">💰 Income & Inflow Tracking</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Analyze recurring salary streams, freelancing contracts, dividend yields, and business revenues.</p>", unsafe_allow_html=True)

metrics = api_client.get_dashboard_metrics(token)
total_income = metrics.get("kpis", {}).get("total_income", 6500.0)

c1, c2, c3 = st.columns(3)
with c1:
    render_kpi_card("Total Monthly Inflow", f"${total_income:,.2f}", badge_text="Verified Streams", variant="emerald")
with c2:
    render_kpi_card("Primary Salary Source", "$5,500.00 / mo", badge_text="84.6% of Inflow", variant="blue")
with c3:
    render_kpi_card("Secondary / Freelance", "$1,000.00 / mo", badge_text="15.4% of Inflow", variant="purple")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

col_chart, col_form = st.columns([1.2, 0.8], gap="medium")

with col_chart:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Inflow Breakdown by Revenue Source")
    
    income_data = pd.DataFrame([
        {"Source": "Primary Tech Salary", "Amount": 5500.0},
        {"Source": "Freelance Consulting", "Amount": 650.0},
        {"Source": "Stock Dividends", "Amount": 250.0},
        {"Source": "High-Yield Interest", "Amount": 100.0}
    ])
    
    fig = px.pie(
        income_data, names="Source", values="Amount", hole=0.5,
        color_discrete_sequence=['#10B981', '#3B82F6', '#8B5CF6', '#F59E0B']
    )
    fig.update_layout(
        paper_bgcolor="rgba(18, 24, 38, 0.4)",
        plot_bgcolor="rgba(18, 24, 38, 0.4)",
        font=dict(color="#F8FAFC")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_form:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Record Inflow Deposit")
    with st.form("income_entry_form", clear_on_submit=True):
        src_name = st.text_input("Income Source", placeholder="e.g. Consulting Invoice #104")
        inc_cat = st.selectbox("Type", ["Salary", "Freelancing", "Business", "Investment", "Other"], index=0)
        inc_amt = st.number_input("Amount ($)", min_value=1.0, value=1200.0, step=100.0)
        submitted = st.form_submit_button("Record Inflow Deposit", type="primary", use_container_width=True)
        if submitted:
            payload = {
                "description": src_name or f"{inc_cat} Income",
                "merchant": "Direct Deposit",
                "amount": inc_amt,
                "type": "INCOME",
                "category": inc_cat,
                "currency": "USD"
            }
            api_client.create_transaction(token, payload)
            st.success(f"Successfully recorded income deposit of ${inc_amt:,.2f}!")
    st.markdown('</div>', unsafe_allow_html=True)
