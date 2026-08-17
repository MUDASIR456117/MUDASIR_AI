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
from frontend.components.charts import create_portfolio_distribution_chart

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">💎 Investment Advisor & Portfolio Analysis</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Risk tolerance classification, educational asset allocation models, and live portfolio concentration analysis.</p>", unsafe_allow_html=True)

st.warning("⚠️ **Regulatory Notice**: This application provides educational and analytical information and is not a substitute for advice from a licensed financial professional. No guaranteed returns.")

tab_port, tab_advisor = st.tabs(["💼 Live Portfolio Holdings", "🧠 Risk Profiler & Asset Allocation"])

with tab_port:
    portfolio = api_client.get_portfolio(token)
    
    total_inv = portfolio.get("total_invested", 16180.0)
    cur_val = portfolio.get("current_value", 18450.0)
    gain_loss = portfolio.get("total_gain_loss", 2270.0)
    gain_pct = portfolio.get("total_gain_loss_pct", 14.03)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Total Capital Invested", f"${total_inv:,.2f}", variant="blue")
    with c2:
        render_kpi_card("Current Market Value", f"${cur_val:,.2f}", variant="emerald")
    with c3:
        render_kpi_card("Unrealized Gain / Loss", f"+${gain_loss:,.2f}", badge_text=f"+{gain_pct:.2f}% Return", badge_type="success", variant="emerald")
    with c4:
        render_kpi_card("Concentration Risk", portfolio.get("concentration_risk", "Low"), badge_text="Diversified", variant="purple")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    col_table, col_pie = st.columns([1.3, 0.9], gap="medium")
    with col_table:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("Asset Holdings Breakdown")
        holdings = portfolio.get("holdings", [])
        if holdings:
            df_h = pd.DataFrame(holdings)
            st.dataframe(
                df_h[["symbol", "name", "asset_type", "quantity", "purchase_price", "current_price", "gain_loss", "gain_loss_pct"]],
                column_config={
                    "purchase_price": st.column_config.NumberColumn("Cost ($)", format="$%.2f"),
                    "current_price": st.column_config.NumberColumn("Current ($)", format="$%.2f"),
                    "gain_loss": st.column_config.NumberColumn("Gain/Loss ($)", format="$%.2f"),
                    "gain_loss_pct": st.column_config.NumberColumn("Return (%)", format="%.2f%%")
                },
                use_container_width=True,
                hide_index=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pie:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        alloc = portfolio.get("allocation_by_type", {"ETF": 45.0, "Stock": 25.0, "Bond": 18.0, "Gold": 12.0})
        fig_pie = create_portfolio_distribution_chart(alloc)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab_advisor:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Personalized Risk Profile & Recommended Asset Allocation")
    
    col_in, col_out = st.columns([1, 1.2], gap="large")
    with col_in:
        with st.form("risk_profiler_form"):
            user_age = st.number_input("Current Age", min_value=18, max_value=85, value=30)
            user_horizon = st.slider("Investment Horizon (Years)", min_value=1, max_value=40, value=10)
            user_tol = st.selectbox("Self-Assessed Risk Tolerance", ["CONSERVATIVE", "MODERATE", "AGGRESSIVE"], index=1)
            user_goal = st.selectbox("Primary Financial Objective", ["Wealth Accumulation", "Retirement Planning", "Home Down Payment", "Capital Preservation"])
            user_ef = st.number_input("Emergency Savings Cushion (Months)", min_value=0.0, value=4.0, step=0.5)
            
            run_prof = st.form_submit_button("Generate Optimal Asset Allocation", type="primary", use_container_width=True)

    with col_out:
        from backend.app.services.investment_service import investment_service
        profile_res = investment_service.evaluate_risk_profile({
            "age": user_age,
            "investment_horizon_years": user_horizon,
            "risk_tolerance_level": user_tol,
            "emergency_fund_months": user_ef,
            "monthly_income": 6500.0
        })
        
        p_class = profile_res.get("classified_profile", "MODERATE")
        target_ret = profile_res.get("target_annual_return_range", "6.5% - 9.0%")
        
        st.markdown(
            f"""
            <div style="padding: 16px; border-radius: 12px; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.08); margin-bottom: 15px;">
                <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 600; text-transform: uppercase;">Classified Investor Archetype</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #60A5FA;">{p_class} STRATEGY</div>
                <div style="font-size: 0.85rem; color: #34D399;">Target Compounding Range: <b>{target_ret}</b></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        alloc_list = profile_res.get("asset_allocation", [])
        if alloc_list:
            df_al = pd.DataFrame(alloc_list)
            st.dataframe(
                df_al[["asset_class", "allocation_pct", "recommended_amount", "expected_volatility"]],
                column_config={
                    "allocation_pct": st.column_config.NumberColumn("Target (%)", format="%.1f%%"),
                    "recommended_amount": st.column_config.NumberColumn("Monthly Alloc ($)", format="$%.2f")
                },
                use_container_width=True,
                hide_index=True
            )
    st.markdown('</div>', unsafe_allow_html=True)
