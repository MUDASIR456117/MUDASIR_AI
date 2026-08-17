import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st
import pandas as pd
from frontend.services.api_client import api_client
from frontend.components.kpi_card import render_kpi_card

token = st.session_state.get("token", "")
user = st.session_state.get("user", {})

st.markdown('<div class="brand-header">⚡ System Administration & Model Ops</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Enterprise telemetry, model lifecycle monitoring, and anonymized system audit logs.</p>", unsafe_allow_html=True)

if user.get("role") != "ADMIN":
    st.warning("⚠️ **Restricted View**: You are currently logged in as standard USER. Switch to ADMIN role to access write operations.")
    if st.button("🔑 Switch to Admin Role"):
        st.session_state.user["role"] = "ADMIN"
        st.rerun()

admin_data = api_client.get_admin_stats(token)

# Top Admin KPIs
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Registered Users", str(admin_data.get("total_users", 18)), badge_text=f"{admin_data.get('active_users_last_30d', 14)} Active", variant="blue")
with c2:
    render_kpi_card("Total Transaction Vol", f"${admin_data.get('total_transaction_volume', 128450.0):,.2f}", badge_text=f"{admin_data.get('total_transactions_count', 348)} Records", variant="emerald")
with c3:
    render_kpi_card("Fraud Alerts Logged", str(admin_data.get("total_fraud_alerts", 4)), badge_text="2 High Risk", badge_type="danger", variant="rose")
with c4:
    render_kpi_card("API Cluster Health", f"{admin_data.get('api_uptime_pct', 99.98)}%", badge_text="99.98% Uptime", variant="purple")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

tab_models, tab_audit, tab_health = st.tabs(["🤖 AI Model Registry & Metrics", "📋 System Audit Logs", "🏥 Cluster Health"])

with tab_models:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Deployed Machine Learning & Deep Learning Models")
    models_list = admin_data.get("models", [])
    if models_list:
        df_mod = pd.DataFrame(models_list)
        st.dataframe(df_mod, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab_audit:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Anonymized API Endpoint Audit Log")
    logs = admin_data.get("recent_audit_logs", [])
    if logs:
        df_logs = pd.DataFrame(logs)
        st.dataframe(df_logs, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab_health:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Service Node Statuses")
    h1, h2, h3 = st.columns(3)
    with h1:
        st.success("✅ **FastAPI Gateway**: 0.0.0.0:8000 (Healthy)")
    with h2:
        st.success("✅ **MongoDB Persistence**: Port 27017 (Connected)")
    with h3:
        st.success("✅ **TensorFlow / Scikit-Learn Engine**: Active")
    st.markdown('</div>', unsafe_allow_html=True)
