import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st
import pandas as pd
from datetime import datetime
from frontend.services.api_client import api_client
from backend.app.services.report_service import report_service

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">📑 Executive Financial Report Generator</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Generate comprehensive audit-ready financial statements in PDF, CSV, and multi-tab Excel formats.</p>", unsafe_allow_html=True)

col_gen, col_preview = st.columns([1, 1.2], gap="large")

with col_gen:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Report Configuration")
    
    with st.form("report_config_form"):
        rep_type = st.selectbox("Report Scope", ["Monthly Financial Statement", "Quarterly Executive Review", "Annual Tax & Wealth Summary"])
        period = st.selectbox("Reporting Period", ["2026-08 (Current Cycle)", "2026-07 (Previous Month)", "2026-Q2 (Apr - Jun)", "2026 Full Year"])
        rep_format = st.radio("Export Format", ["PDF Document (.pdf)", "Excel Workbook (.xlsx)", "CSV Data (.csv)"], index=0)
        
        inc_insights = st.checkbox("Include Predictive Forecasts & AI Insights", value=True)
        inc_xai = st.checkbox("Include Explainable AI Risk Scorecards", value=True)
        
        generate_btn = st.form_submit_button("⚡ Generate Official Report", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_preview:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Generated Report Preview & Downloads")
    
    # Live summary data
    metrics = api_client.get_dashboard_metrics(token)
    txs = api_client.get_transactions(token, limit=100)
    
    summary = {
        "total_income": metrics.get("kpis", {}).get("total_income", 6500.0),
        "total_expenses": metrics.get("kpis", {}).get("total_expenses", 2850.0),
        "net_savings": metrics.get("kpis", {}).get("total_savings", 3650.0),
        "savings_rate_pct": metrics.get("kpis", {}).get("savings_rate_pct", 56.2),
        "top_spending_category": "Housing / Rent",
        "anomaly_count": 0,
        "health_score": metrics.get("kpis", {}).get("financial_health_score", 82),
        "key_insights": metrics.get("ai_insights", [])
    }
    
    st.markdown(
        f"""
        <div style="padding: 14px 18px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 15px;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #FFFFFF;">AI Financial Advisor Statement</div>
            <div style="font-size: 0.85rem; color: #94A3B8;">Period: <b>August 2026</b> • Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</div>
            <div style="font-size: 0.85rem; color: #34D399; margin-top: 4px;">Health Score: <b>82/100 (Optimal Standing)</b></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # PDF generation & download
    pdf_path = report_service.generate_pdf_report(
        user_name=st.session_state.get("user", {}).get("username", "Alex"),
        period="2026-08",
        summary_data=summary,
        transactions=txs
    )
    
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            label="📄 Download Official PDF",
            data=pdf_bytes,
            file_name=f"Financial_Statement_2026_08.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
    with d2:
        excel_bytes = report_service.generate_excel_report(summary, txs)
        st.download_button(
            label="📊 Download Excel (.xlsx)",
            data=excel_bytes,
            file_name=f"Financial_Ledger_2026_08.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
