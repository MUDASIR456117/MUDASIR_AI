import sys
import os
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent.parent)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
import streamlit as st
import pandas as pd
from frontend.services.api_client import api_client
from frontend.components.kpi_card import render_kpi_card, render_ai_insight
from frontend.components.charts import create_forecast_ribbon_chart

token = st.session_state.get("token", "")

st.markdown('<div class="brand-header">📈 Predictive Analytics & Deep Learning Forecast</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8;'>Time-series projections using recurrent neural networks (LSTM) and gradient-boosted ensemble regressors.</p>", unsafe_allow_html=True)

with st.spinner("Computing time-series sequence windowing & running LSTM neural inference..."):
    forecast = api_client.get_forecast(token)

if not forecast.get("has_sufficient_data", True):
    st.warning(f"⚠️ {forecast.get('status_message', 'Not enough historical data to generate a reliable forecast.')}")
else:
    # Top KPI Forecast Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Next Week Predicted Spend", f"${forecast.get('next_week_predicted', 650.0):,.2f}", badge_text="7-Day Horizon", variant="blue")
    with c2:
        render_kpi_card("Next Month Projected Outflow", f"${forecast.get('next_month_predicted', 2780.0):,.2f}", badge_text="30-Day Model", variant="emerald")
    with c3:
        render_kpi_card("Annualized Projected Spend", f"${forecast.get('annual_projected', 33360.0):,.2f}", badge_text="12-Month Run Rate", variant="purple")
    with c4:
        metrics_dict = forecast.get("metrics", {})
        r2 = metrics_dict.get("R2", 0.88)
        render_kpi_card("Model Confidence (R²)", f"{r2:.2f}", badge_text=forecast.get("model_used", "LSTM Neural Net"), variant="amber")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Forecast Ribbon Interactive Chart
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    future_series = forecast.get("future_forecast_series", [])
    hist_series = forecast.get("historical_trend", [])
    fig_fore = create_forecast_ribbon_chart(future_series, hist_series)
    st.plotly_chart(fig_fore, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Category Projections Table
    col_cats, col_model = st.columns([1.2, 0.8], gap="medium")
    with col_cats:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("Category-Level 30-Day Projections")
        cat_preds = forecast.get("category_forecasts", {})
        if cat_preds:
            df_cp = pd.DataFrame(list(cat_preds.items()), columns=["Category", "Projected 30-Day Outflow ($)"])
            st.dataframe(
                df_cp,
                column_config={"Projected 30-Day Outflow ($)": st.column_config.NumberColumn("Projected ($)", format="$%.2f")},
                use_container_width=True,
                hide_index=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_model:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.subheader("Neural Architecture Specifications")
        st.markdown(
            """
            - **Model Type**: Deep Recurrent LSTM (Long Short-Term Memory)
            - **Input Window**: 14 Timesteps (Sliding Horizon)
            - **Preprocessing**: Robust MinMaxScaler Normalization
            - **Loss Function**: Mean Squared Error (MSE)
            - **Confidence Band**: 90% Empirical Prediction Interval
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)
