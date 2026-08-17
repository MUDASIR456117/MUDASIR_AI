import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
from frontend.services.api_client import api_client

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">📷 AI Receipt Scanner & OCR Engine</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Upload paper or digital receipts (JPG, PNG, PDF) for automated OpenCV preprocessing and itemized OCR extraction.</p>", unsafe_allow_html=True)

col_upload, col_result = st.columns([1, 1.2], gap="large")

with col_upload:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Upload Receipt Image")
    
    uploaded_file = st.file_uploader("Select Receipt File (JPG, PNG, PDF)", type=["jpg", "jpeg", "png", "pdf"])
    
    if uploaded_file is not None:
        if uploaded_file.type.startswith("image"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Receipt Preview", use_container_width=True)
        else:
            st.info(f"PDF document attached: {uploaded_file.name}")

        scan_btn = st.button("🚀 Process with Computer Vision & OCR", type="primary", use_container_width=True)
        if scan_btn:
            with st.spinner("Running OpenCV bilateral noise filter, adaptive thresholding, and OCR entity parsing..."):
                file_bytes = uploaded_file.getvalue()
                res = api_client.scan_receipt(token, file_bytes, uploaded_file.name)
                st.session_state["last_receipt_parsed"] = res
                st.success("Receipt successfully parsed!")
    else:
        st.markdown(
            """
            <div style="text-align: center; padding: 40px 20px; border: 2px dashed rgba(255,255,255,0.15); border-radius: 12px; margin-top: 10px;">
                <div style="font-size: 2.5rem; margin-bottom: 8px;">🧾</div>
                <div style="font-weight: 600; color: #E2E8F0;">Drag and drop receipt image here</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">Supports high-res retail receipts, dining bills, grocery vouchers</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

with col_result:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("Extracted Receipt Metadata & Items")
    
    parsed = st.session_state.get("last_receipt_parsed", None)
    if parsed:
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"**Merchant:** `{parsed.get('merchant', 'Target')}`")
            st.markdown(f"**Date:** `{parsed.get('date', '2026-08-16')}`")
            st.markdown(f"**Payment Method:** `{parsed.get('payment_method', 'Credit Card')}`")
        with m2:
            st.markdown(f"**Subtotal:** `${parsed.get('subtotal', 0.0):.2f}`")
            st.markdown(f"**Tax:** `${parsed.get('tax', 0.0):.2f}`")
            st.markdown(f"**Total Amount:** `💵 ${parsed.get('total', 0.0):.2f}`")

        st.markdown("---")
        st.markdown("##### Itemized Line Items")
        items = parsed.get("items", [])
        if items:
            df_items = pd.DataFrame(items)
            st.dataframe(
                df_items,
                column_config={"price": st.column_config.NumberColumn("Unit Price ($)", format="$%.2f")},
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown("---")
        st.markdown("##### Confirm & Save to Transactions")
        with st.form("confirm_receipt_tx_form"):
            c_desc = st.text_input("Transaction Description", value=f"{parsed.get('merchant', 'Retail')} Purchase")
            c_cat = st.selectbox("Category", ["Grocery", "Food", "Shopping", "Fuel", "Utilities", "Other"],
                                 index=0 if parsed.get('suggested_category') == "Grocery" else 2)
            c_amt = st.number_input("Final Amount ($)", value=float(parsed.get('total', 50.0)), step=1.0)
            
            save_tx = st.form_submit_button("⚡ Create Verified Transaction Record", type="primary", use_container_width=True)
            if save_tx:
                tx_payload = {
                    "description": c_desc,
                    "merchant": parsed.get("merchant", "Retail"),
                    "amount": c_amt,
                    "type": "EXPENSE",
                    "category": c_cat,
                    "payment_method": parsed.get("payment_method", "Credit Card"),
                    "currency": "USD"
                }
                api_client.create_transaction(token, tx_payload)
                st.success("Transaction verified and saved directly into your financial ledger!")
    else:
        st.info("Upload and process a receipt to view itemized text parsing.")
    st.markdown('</div>', unsafe_allow_html=True)
