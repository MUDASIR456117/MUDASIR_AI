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
from frontend.components.kpi_card import render_kpi_card

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">🛡️ AI Fraud & Anomaly Detection</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Real-time statistical anomaly monitoring powered by Isolation Forest & Deep Autoencoders.</p>", unsafe_allow_html=True)

st.info("ℹ️ **Statistical Disclosure**: Anomaly detection identifies irregular statistical outliers and risk signals; it is not definitive proof of fraud.")

tab_sim, tab_history = st.tabs(["🧪 Real-Time Transaction Risk Sandbox", "🚨 Flagged Anomaly Alerts"])

with tab_sim:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Test Transaction Anomaly Scanner")
    st.markdown("<p style='color: #94A3B8;'>Simulate transaction features to evaluate live Isolation Forest anomaly scoring:</p>", unsafe_allow_html=True)
    
    col_in, col_out = st.columns([1, 1.2], gap="large")
    with col_in:
        with st.form("fraud_sim_form"):
            sim_amt = st.number_input("Transaction Amount ($)", min_value=1.0, value=1250.0, step=50.0)
            sim_cat = st.selectbox("Category", ["Food", "Grocery", "Shopping", "Travel", "Fuel", "Other"], index=2)
            sim_merch = st.text_input("Merchant Name", value="Apex Foreign Luxury Goods")
            sim_time = st.selectbox("Transaction Time of Day", ["Daytime (2:30 PM)", "Late Night (3:15 AM)", "Evening (8:00 PM)"], index=1)
            
            run_check = st.form_submit_button("🔍 Run Multi-Feature Anomaly Check", type="primary", use_container_width=True)
    
    with col_out:
        if run_check:
            # Parse simulated time
            hour = 3 if "3:15" in sim_time else (14 if "2:30" in sim_time else 20)
            sim_dt = datetime.utcnow().replace(hour=hour)
            
            with st.spinner("Executing Isolation Forest multidimensional boundary test..."):
                res = api_client.check_fraud(token, {
                    "amount": sim_amt,
                    "category": sim_cat,
                    "merchant": sim_merch,
                    "transaction_time": sim_dt.isoformat()
                })
                
                risk_level = res.get("risk_level", "LOW")
                risk_score = res.get("risk_score", 20.0)
                reasons = res.get("reasons", [])
                action = res.get("recommended_action", "")
                
                badge_type = "danger" if risk_level == "HIGH" else ("warning" if risk_level == "MEDIUM" else "success")
                st.markdown(
                    f"""
                    <div style="padding: 18px; border-radius: 12px; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 1.1rem; font-weight: 700; color: #FFFFFF;">Risk Classification:</span>
                            <span class="kpi-badge badge-{badge_type}" style="font-size: 0.9rem;">{risk_level} RISK</span>
                        </div>
                        <div style="font-size: 2.2rem; font-weight: 800; color: {'#F43F5E' if risk_level == 'HIGH' else ('#F59E0B' if risk_level == 'MEDIUM' else '#10B981')}; margin-top: 6px;">
                            {risk_score:.1f}% Risk Score
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown("##### 📌 Trigger Reasons Identified:")
                for r in reasons:
                    st.markdown(f"• {r}")
                
                st.markdown("##### ⚡ Recommended Action:")
                st.info(action)
        else:
            st.markdown(
                """
                <div style="text-align: center; padding: 40px 20px; border: 2px dashed rgba(255,255,255,0.1); border-radius: 12px;">
                    <div style="font-size: 2.5rem; margin-bottom: 8px;">🛡️</div>
                    <div style="color: #94A3B8;">Submit transaction parameters on the left to trigger the AI Anomaly Detector.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

with tab_history:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Historical Fraud Anomaly Log")
    sample_alerts = [
        {"Timestamp": "2026-08-16 03:22 AM", "Merchant": "Apex Global Electronics", "Amount": "$2,850.00", "Risk Level": "HIGH (88%)", "Status": "Under Review"},
        {"Timestamp": "2026-08-10 02:45 AM", "Merchant": "Crypto Express Overseas", "Amount": "$1,420.00", "Risk Level": "HIGH (79%)", "Status": "Resolved (Legitimate)"},
        {"Timestamp": "2026-08-04 11:15 PM", "Merchant": "Luxury Watch Boutique", "Amount": "$750.00", "Risk Level": "MEDIUM (48%)", "Status": "Verified by User"}
    ]
    st.dataframe(pd.DataFrame(sample_alerts), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
