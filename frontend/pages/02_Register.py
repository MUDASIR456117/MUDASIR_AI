import sys
import os
from pathlib import Path

# Ensure project root is in sys.path
_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
from frontend.services.api_client import api_client

st.markdown('<div class="brand-header">📝 Create Account</div>', unsafe_allow_html=True)
st.markdown("<p class='sub-header-text'>Register to start tracking your finances and using AI financial advice.</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("""
    <div class="glass-panel">
        <h3 style="color: #FFFFFF; margin-bottom: 6px;">Register New User</h3>
        <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 18px;">Please fill in the form below</p>
    """, unsafe_allow_html=True)

    full_name = st.text_input("Full Name", placeholder="e.g. John Doe")
    username = st.text_input("Username", placeholder="e.g. johndoe")
    email = st.text_input("Email Address", placeholder="name@domain.com")
    password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=5000.0, step=100.0)
    with col_f2:
        risk_tolerance = st.selectbox("Risk Tolerance", ["LOW", "MODERATE", "HIGH"], index=1)

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("Create Account", use_container_width=True, type="primary"):
            if not email or not password or not username:
                st.error("Please fill in all required fields.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                with st.spinner("Creating account..."):
                    payload = {
                        "username": username.strip(),
                        "email": email.strip().lower(),
                        "password": password.strip(),
                        "full_name": full_name.strip() if full_name else username.strip(),
                        "monthly_income": float(monthly_income),
                        "risk_tolerance": risk_tolerance
                    }
                    res = api_client.register(payload)
                    if res.get("success") or res.get("id") or res.get("email"):
                        st.success("Account created successfully! Logging in...")
                        st.session_state.login_email = email.strip()
                        st.session_state.login_password = password.strip()
                        st.session_state.token = res.get("access_token", "mock_token")
                        st.session_state.user = {
                            "id": res.get("id", "u_new"),
                            "username": username.strip(),
                            "email": email.strip(),
                            "full_name": full_name.strip() if full_name else username.strip(),
                            "role": "USER",
                            "monthly_income": float(monthly_income),
                            "risk_tolerance": risk_tolerance
                        }
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        err = res.get("error", "Email might already exist.")
                        st.warning(f"Registration note: {err}")
                        st.info("If you already have an account, please click Login below.")

    with col_b2:
        if st.button("Go to Login", use_container_width=True):
            st.switch_page("pages/01_Login.py")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-panel">
        <h4 style="color: #3B82F6; margin-bottom: 8px;">Key Features</h4>
        <ul style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.8; padding-left: 18px;">
            <li>📊 Real-time Financial Dashboard</li>
            <li>📈 Deep Learning Spending Forecast</li>
            <li>🛡️ Fraud & Anomaly Detection</li>
            <li>🧾 Receipt Scanner with OCR</li>
            <li>🤖 AI Financial Chatbot Assistant</li>
            <li>📑 PDF, Excel, and CSV Report Export</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
