import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st

st.markdown('<div class="brand-header">⚙️ System & Alert Settings</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Configure currency localization, threshold notifications, and ML model parameters.</p>", unsafe_allow_html=True)

col_s1, col_s2 = st.columns(2, gap="large")

with col_s1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Display & Currency")
    currency = st.selectbox("Display Currency", ["USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "JPY (¥)"], index=0)
    theme = st.selectbox("Dashboard Theme Aesthetics", ["Fintech Dark Luxury (Default)", "Light High Contrast", "Cyberpunk Emerald Neon"], index=0)
    date_format = st.selectbox("Date Presentation Format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD-MM-YYYY"], index=0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Notification Preferences")
    st.toggle("Push notifications for flagged transactions", value=True)
    st.toggle("Weekly AI Financial Digest email", value=True)
    st.toggle("Monthly budget ceiling threshold alerts (85%+)", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_s2:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("AI / ML Tuning Thresholds")
    fraud_thresh = st.slider("Anomaly Sensitivity (Isolation Forest)", min_value=1, max_value=10, value=5, help="Higher sensitivity flags smaller statistical outliers")
    forecast_horizon = st.slider("LSTM Forecast Horizon (Days)", min_value=7, max_value=60, value=30)
    budget_safety = st.slider("Budget Overrun Warning Threshold (%)", min_value=70, max_value=95, value=85)
    
    if st.button("💾 Save System Preferences", type="primary", use_container_width=True):
        st.success("Preferences updated and synchronized across all AI services!")
    st.markdown('</div>', unsafe_allow_html=True)
