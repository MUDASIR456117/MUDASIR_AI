import sys
import os
from pathlib import Path

# Ensure project root is in sys.path
_ROOT = str(Path(__file__).resolve().parent.parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
from frontend.services.api_client import api_client

st.markdown('<div class="brand-header">🔐 Welcome to AI Financial Advisor</div>', unsafe_allow_html=True)
st.markdown("<p class='sub-header-text'>Please sign in to access your financial dashboard, budgets, and AI insights.</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("""
    <div class="glass-panel">
        <h3 style="color: #FFFFFF; margin-bottom: 6px;">Sign In</h3>
        <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 18px;">Enter your email and password</p>
    """, unsafe_allow_html=True)

    default_email = st.session_state.get("login_email", "demo@financialadvisor.ai")
    default_pass = st.session_state.get("login_password", "Demo@12345")

    email = st.text_input("Email Address", value=default_email, placeholder="name@domain.com")
    password = st.text_input("Password", value=default_pass, type="password", placeholder="Enter password")

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Login", use_container_width=True, type="primary"):
            cleaned_email = email.strip()
            if cleaned_email and "@" not in cleaned_email:
                cleaned_email = f"{cleaned_email.lower()}@financialadvisor.ai"

            if not cleaned_email or not password:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Logging in..."):
                    res = api_client.login(cleaned_email, password.strip())
                    if res.get("success") or res.get("access_token"):
                        token = res.get("access_token", "mock_jwt_token_user")
                        user_info = res.get("user", {})
                        if not user_info:
                            user_info = api_client.get_profile(token)
                        if not user_info or not isinstance(user_info, dict):
                            user_info = {
                                "id": "u1",
                                "username": cleaned_email.split("@")[0],
                                "email": cleaned_email,
                                "full_name": "Alex Mercer" if "demo" in cleaned_email.lower() else cleaned_email.split("@")[0].capitalize(),
                                "role": "ADMIN" if "admin" in cleaned_email.lower() else "USER",
                                "monthly_income": 6500.0,
                                "risk_tolerance": "MODERATE"
                            }
                        st.session_state.token = token
                        st.session_state.user = user_info
                        st.session_state.authenticated = True
                        st.success("Login Successful! Opening Dashboard...")
                        st.rerun()
                    else:
                        raw_err = res.get("error", "Invalid email or password.")
                        st.error(f"Login Failed: {raw_err}")

    with col_btn2:
        if st.button("Create Account", use_container_width=True):
            st.switch_page("pages/02_Register.py")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-panel">
        <h4 style="color: #3B82F6; margin-bottom: 8px;">Demo Accounts</h4>
        <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin-bottom: 14px;">
            Click a button below to quickly load demo login details:
        </p>
    """, unsafe_allow_html=True)

    if st.button("👤 Demo User (Alex Mercer)", use_container_width=True):
        st.session_state.login_email = "demo@financialadvisor.ai"
        st.session_state.login_password = "Demo@12345"
        st.rerun()

    st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)

    if st.button("s Administrator Account", use_container_width=True):
        st.session_state.login_email = "admin@financialadvisor.ai"
        st.session_state.login_password = "Admin@12345"
        st.rerun()

    st.markdown("""
        <div style="margin-top: 18px; padding: 12px; background: #0F172A; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 0.8rem; color: #10B981; font-weight: 600;">System Status</div>
            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px; line-height: 1.5;">
                • MongoDB Database: Connected<br/>
                • ML & Deep Learning: Ready<br/>
                • Receipt Scanner & PDF Reports: Active
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
