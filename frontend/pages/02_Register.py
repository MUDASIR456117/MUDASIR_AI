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
st.markdown("<p class='sub-header-text'>Register to start tracking your finances and receiving personalized AI financial advice.</p>", unsafe_allow_html=True)
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

    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("Create Account", use_container_width=True, type="primary"):
            cleaned_email = email.strip().lower()
            cleaned_user = username.strip()
            cleaned_pass = password.strip()
            cleaned_name = full_name.strip() if full_name else cleaned_user.capitalize()

            if not cleaned_email or not cleaned_pass or not cleaned_user:
                st.error("Please fill in all required fields (Email, Username, Password).")
            elif len(cleaned_pass) < 6:
                st.error("Password must be at least 6 characters.")
            elif "@" not in cleaned_email or "." not in cleaned_email:
                st.error("Please enter a valid email address.")
            else:
                with st.spinner("Creating account and securing session..."):
                    payload = {
                        "username": cleaned_user,
                        "email": cleaned_email,
                        "password": cleaned_pass,
                        "full_name": cleaned_name,
                        "monthly_income": float(monthly_income),
                        "risk_tolerance": risk_tolerance
                    }
                    res = api_client.register(payload)
                    if res.get("access_token"):
                        st.success("Account created successfully! Redirecting...")
                        st.session_state.login_email = cleaned_email
                        st.session_state.login_password = ""
                        st.session_state.token = res["access_token"]
                        st.session_state.user = res.get("user", {
                            "id": "u_new",
                            "username": cleaned_user,
                            "email": cleaned_email,
                            "full_name": cleaned_name,
                            "role": "USER",
                            "monthly_income": float(monthly_income),
                            "risk_tolerance": risk_tolerance
                        })
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        err = res.get("error", "Registration failed. Please check your details.")
                        st.error(f"Registration Failed: {err}")

    with col_b2:
        if st.button("Go to Login", use_container_width=True):
            st.switch_page("pages/01_Login.py")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-panel">
        <h4 style="color: #3B82F6; margin-bottom: 8px;">Key Platform Features</h4>
        <ul style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.8; padding-left: 18px;">
            <li>ss <b>Real-time Financial Dashboard</b></li>
            <li>ss <b>Deep Learning Spending Forecast</b></li>
            <li>sss <b>Fraud & Anomaly Detection</b></li>
            <li>ss <b>Receipt Scanner with OCR</b></li>
            <li>ss <b>AI Financial Chatbot Assistant</b></li>
            <li>ss <b>PDF, Excel, and CSV Report Export</b></li>
        </ul>
        <div style="margin-top: 14px; padding: 12px; background: #0F172A; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 0.8rem; color: #10B981; font-weight: 600;">Privacy First</div>
            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px; line-height: 1.5;">
                Your financial data is stored securely in dedicated MongoDB collections with bcrypt password hashing.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
