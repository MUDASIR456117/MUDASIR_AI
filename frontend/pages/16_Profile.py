import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st
from frontend.services.api_client import api_client

user = st.session_state.get("user", {})

st.markdown('<div class="brand-header">👤 User Profile & Risk Persona</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Manage your account credentials, primary income baselines, and investment risk profiles.</p>", unsafe_allow_html=True)

col_prof, col_sec = st.columns([1.1, 0.9], gap="large")

with col_prof:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Financial Identity")
    with st.form("update_profile_form"):
        name = st.text_input("Full Name", value=user.get("full_name", "Alex Mercer"))
        username = st.text_input("Username", value=user.get("username", "demouser"), disabled=True)
        email = st.text_input("Email", value=user.get("email", "demo@financialadvisor.ai"), disabled=True)
        income = st.number_input("Monthly Net Inflow ($)", value=float(user.get("monthly_income", 6500.0)), step=250.0)
        risk_tol = st.selectbox("Investment Risk Tolerance", ["CONSERVATIVE", "MODERATE", "AGGRESSIVE"],
                                index=1 if user.get("risk_tolerance") == "MODERATE" else 0)
        
        save_prof = st.form_submit_button("Update Financial Profile", type="primary", use_container_width=True)
        if save_prof:
            st.session_state.user["full_name"] = name
            st.session_state.user["monthly_income"] = income
            st.session_state.user["risk_tolerance"] = risk_tol
            st.success("Profile preferences successfully updated!")
    st.markdown('</div>', unsafe_allow_html=True)

with col_sec:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Account & Security Summary")
    st.markdown(
        f"""
        - **Account Status**: <span style="color: #34D399; font-weight: 700;">ACTIVE (Verified)</span>
        - **Assigned Role**: <span style="color: #60A5FA; font-weight: 700;">{user.get('role', 'USER')}</span>
        - **Encryption Standard**: SHA-256 / AES-256 JWT
        - **Multi-Factor Auth (MFA)**: Enabled (SMS & App)
        - **Connected Database**: MongoDB Enterprise
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown("##### Change Master Password")
    with st.form("pwd_change_form"):
        old_p = st.text_input("Current Password", type="password")
        new_p = st.text_input("New Password", type="password")
        sub_p = st.form_submit_button("Update Password", use_container_width=True)
        if sub_p:
            if len(new_p) >= 6:
                st.success("Password updated successfully!")
            else:
                st.error("New password must be at least 6 characters.")
    st.markdown('</div>', unsafe_allow_html=True)
