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

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">💳 Transaction Management</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Record, categorize, filter, and audit all personal financial inflows and outflows.</p>", unsafe_allow_html=True)

# Action Tabs
tab_list, tab_add, tab_export = st.tabs(["📋 Activity Feed", "➕ Add Transaction", "📥 Export Data"])

CATEGORIES = ["Food", "Grocery", "Rent", "Utilities", "Transport", "Fuel", "Shopping", "Entertainment", "Education", "Healthcare", "Travel", "Salary", "Freelancing", "Business", "Investment", "Other"]
TYPES = ["EXPENSE", "INCOME", "TRANSFER", "INVESTMENT"]

with tab_add:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("New Transaction Entry")
    
    with st.form("add_tx_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            desc = st.text_input("Description / Title", placeholder="e.g. Weekly organic groceries")
            merchant = st.text_input("Merchant / Payee", placeholder="e.g. Whole Foods Market")
            amount = st.number_input("Amount ($)", min_value=0.01, value=45.0, step=5.0)
            tx_type = st.selectbox("Transaction Type", TYPES, index=0)
        with c2:
            category = st.selectbox("Category (Leave 'Other' for AI auto-tag)", CATEGORIES, index=CATEGORIES.index("Other"))
            payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Bank Transfer", "Apple Pay", "Cash"], index=0)
            date = st.date_input("Transaction Date", value=datetime.utcnow())
            location = st.text_input("Location", value="In-Store")

        submitted = st.form_submit_button("⚡ Save Transaction (Run AI Categorization & Fraud Check)", type="primary", use_container_width=True)
        if submitted:
            if not desc:
                st.error("Please enter a description.")
            else:
                payload = {
                    "description": desc,
                    "merchant": merchant,
                    "amount": amount,
                    "type": tx_type,
                    "category": category,
                    "payment_method": payment_method,
                    "date": datetime.combine(date, datetime.min.time()).isoformat(),
                    "location": location,
                    "currency": "USD"
                }
                res = api_client.create_transaction(token, payload)
                if "error" in res:
                    st.error(res["error"])
                else:
                    st.success(f"Transaction recorded! Assigned Category: **{res.get('category')}** (AI Anomaly Risk: {res.get('anomaly_score', 10.0):.1f}%)")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_list:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    # Search and Filter Toolbar
    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        search_query = st.text_input("🔍 Search Transactions", placeholder="Filter by merchant or description...")
    with f2:
        filter_cat = st.selectbox("Filter Category", ["All Categories"] + CATEGORIES)
    with f3:
        filter_type = st.selectbox("Filter Type", ["All Types"] + TYPES)

    txs = api_client.get_transactions(token, limit=100)
    
    if txs:
        df = pd.DataFrame(txs)
        
        # Apply filters
        if search_query:
            df = df[df["description"].str.contains(search_query, case=False, na=False) | df["merchant"].str.contains(search_query, case=False, na=False)]
        if filter_cat != "All Categories":
            df = df[df["category"] == filter_cat]
        if filter_type != "All Types":
            df = df[df["type"] == filter_type]

        st.markdown(f"<p style='font-size: 0.85rem; color: #94A3B8;'>Showing <b>{len(df)}</b> matching transactions</p>", unsafe_allow_html=True)
        
        st.dataframe(
            df[["date", "merchant", "description", "category", "type", "amount", "payment_method"]],
            column_config={
                "amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
                "date": st.column_config.TextColumn("Date")
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No transaction records found.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_export:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Export Transaction Ledger")
    st.markdown("<p style='color: #94A3B8;'>Download clean formatted records for accounting and tax preparation.</p>", unsafe_allow_html=True)
    
    txs = api_client.get_transactions(token, limit=500)
    df_export = pd.DataFrame(txs)
    
    if not df_export.empty:
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV Ledger",
            data=csv_data,
            file_name=f"transactions_ledger_{datetime.utcnow().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            type="primary"
        )
    else:
        st.info("No records to export.")
    st.markdown('</div>', unsafe_allow_html=True)
