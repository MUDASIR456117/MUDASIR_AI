import sys
import os
from pathlib import Path

# Ensure project root is in sys.path
_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
from frontend.services.api_client import api_client

# Page Config
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Clean CSS
css_path = Path(__file__).resolve().parent / "styles" / "custom.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session State
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Backend Health Check
health = api_client.check_health()
status_color = "#10B981" if health.get("status") == "healthy" else "#EF4444"

# Sidebar
with st.sidebar:
    st.markdown('<div class="brand-header">💼 AI Financial Advisor</div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #94A3B8; margin-top: -4px;'>Personal Finance & Wealth Platform</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Status Box
    st.markdown(
        f"""
        <div style="background: #131B2E; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px 14px; margin-bottom: 14px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 0.78rem; color: #94A3B8; font-weight: 600;">SYSTEM STATUS</span>
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: {status_color};"></span>
            </div>
            <div style="font-size: 0.88rem; font-weight: 700; color: #FFFFFF; margin-top: 4px;">
                FastAPI: Online (v1.0.0)
            </div>
            <div style="font-size: 0.75rem; color: #10B981;">MongoDB Atlas: Connected</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.get("authenticated") and st.session_state.get("user"):
        u = st.session_state.user
        st.markdown(
            f"""
            <div style="padding: 12px 14px; background: #1E293B; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 14px;">
                <div style="font-size: 0.75rem; color: #3B82F6; font-weight: 600;">ACTIVE USER</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF;">{u.get('full_name', 'Alex Mercer')}</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Role: <span style="color: #10B981; font-weight: 600;">{u.get('role', 'USER')}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()

# Navigation (Locked until login)
if not st.session_state.get("authenticated"):
    pages = {
        "Account Access": [
            st.Page("pages/01_Login.py", title="Login", icon="🔐", default=True),
            st.Page("pages/02_Register.py", title="Register", icon="📝")
        ]
    }
else:
    user_role = st.session_state.user.get("role", "USER") if st.session_state.user else "USER"
    
    pages = {
        "Core Finance": [
            st.Page("pages/03_Dashboard.py", title="Dashboard", icon="📊", default=True),
            st.Page("pages/04_Transactions.py", title="Transactions", icon="💳"),
            st.Page("pages/05_Income.py", title="Income Inflow", icon="💰"),
            st.Page("pages/06_Expense_Analytics.py", title="Expense Analytics", icon="📉"),
            st.Page("pages/07_Receipt_Scanner.py", title="Receipt Scanner", icon="🧾")
        ],
        "AI & Predictions": [
            st.Page("pages/08_AI_Budget_Planner.py", title="AI Budget Planner", icon="🧠"),
            st.Page("pages/09_Financial_Forecast.py", title="Spending Forecast", icon="📈"),
            st.Page("pages/10_Fraud_Detection.py", title="Fraud Detection", icon="🛡️"),
            st.Page("pages/11_Credit_Risk.py", title="Credit Risk (XAI)", icon="⚖️"),
            st.Page("pages/14_AI_Financial_Assistant.py", title="AI Assistant", icon="🤖")
        ],
        "Wealth Planning": [
            st.Page("pages/12_Investment_Advisor.py", title="Investment Advisor", icon="💼"),
            st.Page("pages/13_Financial_Goals.py", title="Financial Goals", icon="🎯"),
            st.Page("pages/15_Reports.py", title="Financial Reports", icon="📑")
        ],
        "Settings": [
            st.Page("pages/16_Profile.py", title="Profile", icon="👤"),
            st.Page("pages/17_Settings.py", title="Settings", icon="⚙️")
        ]
    }
    
    if user_role == "ADMIN":
        pages["Admin"] = [
            st.Page("pages/18_Admin_Dashboard.py", title="Admin Dashboard", icon="s")
        ]

nav = st.navigation(pages)
nav.run()
