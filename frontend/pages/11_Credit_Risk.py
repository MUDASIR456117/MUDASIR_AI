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

st.markdown('<div class="brand-header">🎯 Credit Risk Analysis & Explainable AI (XAI)</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Evaluate credit health, default risk tier, and explore transparent feature attribution weights.</p>", unsafe_allow_html=True)

st.warning("⚠️ **Educational Disclaimer**: This assessment is an educational machine-learning estimate and is not an official FICO/credit score or a loan approval guarantee.")

col_form, col_res = st.columns([1, 1.2], gap="large")

with col_form:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Credit Profile Inputs")
    with st.form("credit_profile_form"):
        income = st.number_input("Annual Gross Income ($)", min_value=10000.0, value=78000.0, step=5000.0)
        emp_years = st.number_input("Employment Duration (Years)", min_value=0.0, value=4.5, step=0.5)
        monthly_debt = st.number_input("Monthly Debt Payments ($)", min_value=0.0, value=450.0, step=50.0)
        on_time_pct = st.slider("Payment History (% On-Time)", min_value=50.0, max_value=100.0, value=98.0, step=1.0)
        utilization = st.slider("Credit Utilization Ratio (%)", min_value=0.0, max_value=100.0, value=22.0, step=1.0)
        open_accts = st.number_input("Number of Active Credit Accounts", min_value=1, value=5, step=1)
        defaults = st.selectbox("Previous Defaults / Delinquencies", [0, 1, 2, 3], index=0)
        age = st.number_input("Age", min_value=18, max_value=90, value=30)
        
        calc_btn = st.form_submit_button("⚡ Evaluate Credit Risk & Run XAI Attribution", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_res:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Predictive Assessment & Explainability")
    
    # Run evaluation
    profile_payload = {
        "annual_income": income,
        "employment_duration_years": emp_years,
        "existing_loans_count": 1,
        "monthly_debt_payments": monthly_debt,
        "payment_history_on_time_pct": on_time_pct,
        "credit_utilization_ratio": utilization,
        "number_of_open_accounts": open_accts,
        "previous_defaults_count": defaults,
        "age": age
    }
    
    res = api_client.evaluate_credit(token, profile_payload)
    risk_cat = res.get("risk_category", "LOW RISK")
    score_range = res.get("estimated_credit_score_range", "740 - 780")
    def_prob = res.get("default_probability", 0.04)
    
    c_badge = "success" if risk_cat == "LOW RISK" else ("warning" if risk_cat == "MEDIUM RISK" else "danger")
    st.markdown(
        f"""
        <div style="padding: 16px 20px; border-radius: 12px; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.85rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Estimated Credit Standing</span>
                <span class="kpi-badge badge-{c_badge}">{risk_cat}</span>
            </div>
            <div style="font-size: 1.9rem; font-weight: 800; color: #FFFFFF; margin-top: 4px;">{score_range}</div>
            <div style="font-size: 0.82rem; color: #64748B;">Estimated Model Default Probability: <b>{def_prob * 100:.1f}%</b></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("##### 🟢 Primary Positive Factors (Strengths):")
    for pos in res.get("top_positive_factors", []):
        st.markdown(f"• <span style='color: #34D399;'>{pos}</span>", unsafe_allow_html=True)
        
    st.markdown("##### 🔴 Primary Risk Vectors (Areas to Watch):")
    for rk in res.get("top_risk_factors", []):
        st.markdown(f"• <span style='color: #F87171;'>{rk}</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### 📊 Explainable AI: Feature Importance Weights")
    feat_imp = res.get("feature_importance", {})
    if feat_imp:
        df_imp = pd.DataFrame(list(feat_imp.items()), columns=["Factor", "Weight"]).sort_values("Weight", ascending=True)
        fig_imp = px.bar(df_imp, x="Weight", y="Factor", orientation="h", color="Weight", color_continuous_scale="Tealgrn")
        fig_imp.update_layout(
            paper_bgcolor="rgba(18, 24, 38, 0.4)",
            plot_bgcolor="rgba(18, 24, 38, 0.4)",
            font=dict(color="#F8FAFC"),
            coloraxis_showscale=False,
            height=200,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_imp, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
