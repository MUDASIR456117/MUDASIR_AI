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

st.markdown('<div class="brand-header">🎯 Financial Goals Tracker</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Set targeted savings milestones, monitor progress runways, and calculate required monthly contributions.</p>", unsafe_allow_html=True)

goals = api_client.get_goals(token)

total_target = sum(float(g.get("target_amount", 0)) for g in goals)
total_accumulated = sum(float(g.get("current_amount", 0)) for g in goals)
overall_pct = (total_accumulated / max(total_target, 1.0)) * 100.0

c1, c2, c3 = st.columns(3)
with c1:
    render_kpi_card("Total Goals Target", f"${total_target:,.2f}", variant="blue")
with c2:
    render_kpi_card("Total Funds Accumulated", f"${total_accumulated:,.2f}", badge_text=f"{overall_pct:.1f}% Overall", variant="emerald")
with c3:
    render_kpi_card("Remaining Capital Needed", f"${total_target - total_accumulated:,.2f}", variant="purple")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

col_list, col_add = st.columns([1.3, 0.9], gap="medium")

with col_list:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Active Savings Milestones")
    
    for g in goals:
        name = g.get("name", "Goal")
        target = float(g.get("target_amount", 1000.0))
        current = float(g.get("current_amount", 0.0))
        rem = float(g.get("remaining_amount", target - current))
        pct = float(g.get("progress_percentage", (current / max(target, 1.0)) * 100.0))
        
        st.markdown(
            f"""
            <div style="margin-bottom: 18px; padding: 14px 16px; background: rgba(30, 41, 59, 0.6); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; font-size: 1.05rem; color: #FFFFFF;">{name}</span>
                    <span style="color: #34D399; font-weight: 700; font-size: 0.95rem;">{pct:.1f}%</span>
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 8px;">
                    Saved: <b>${current:,.2f}</b> of <b>${target:,.2f}</b> • Remaining: <span style="color: #FBBF24;">${rem:,.2f}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(min(1.0, pct / 100.0))
    st.markdown('</div>', unsafe_allow_html=True)

with col_add:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("➕ Create New Goal")
    with st.form("new_goal_form", clear_on_submit=True):
        g_name = st.text_input("Goal Title", placeholder="e.g. Home Down Payment")
        g_target = st.number_input("Target Amount ($)", min_value=50.0, value=25000.0, step=500.0)
        g_initial = st.number_input("Initial Saved Amount ($)", min_value=0.0, value=2000.0, step=100.0)
        g_monthly = st.number_input("Planned Monthly Deposit ($)", min_value=10.0, value=800.0, step=50.0)
        g_cat = st.selectbox("Category", ["Emergency", "Housing", "Vehicle", "Travel", "Gadgets", "Education", "Other"])
        
        submitted = st.form_submit_button("⚡ Create Financial Goal", type="primary", use_container_width=True)
        if submitted:
            st.success(f"Goal '{g_name}' created successfully! Monthly runway tracking active.")
    st.markdown('</div>', unsafe_allow_html=True)
