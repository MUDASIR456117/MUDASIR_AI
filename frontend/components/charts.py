import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List

CHART_THEME = {
    "paper_bgcolor": "rgba(18, 24, 38, 0.4)",
    "plot_bgcolor": "rgba(18, 24, 38, 0.4)",
    "font": {"family": "Inter, sans-serif", "color": "#F8FAFC", "size": 12},
    "margin": dict(l=30, r=30, t=40, b=30)
}

def create_income_vs_expense_chart(monthly_data: List[Dict[str, Any]]) -> go.Figure:
    """Create comparison bar chart for Monthly Inflow vs Outflow."""
    df = pd.DataFrame(monthly_data)
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['month'],
        y=df['income'],
        name='Income',
        marker_color='#10B981',
        marker_line=dict(width=0),
        hovertemplate='<b>Income</b>: $%{y:,.2f}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=df['month'],
        y=df['expenses'],
        name='Expenses',
        marker_color='#F43F5E',
        marker_line=dict(width=0),
        hovertemplate='<b>Expenses</b>: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='group',
        title="<b>Monthly Cash Flow (Inflow vs Outflow)</b>",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False, tickprefix="$"),
        **CHART_THEME
    )
    return fig

def create_category_donut_chart(category_spending: Dict[str, float]) -> go.Figure:
    """Create donut chart showing expense breakdown by category."""
    labels = list(category_spending.keys())
    values = list(category_spending.values())
    
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4', '#64748B', '#14B8A6']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color='#0B0F19', width=2)),
        textinfo='percent+label',
        hoverinfo='label+value+percent',
        hovertemplate='<b>%{label}</b><br>$%{value:,.2f} (%{percent})<extra></extra>'
    )])
    
    fig.update_layout(
        title="<b>Spending by Category</b>",
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
        **CHART_THEME
    )
    return fig

def create_forecast_ribbon_chart(forecast_points: List[Dict[str, Any]], historical_points: List[Dict[str, Any]] = None) -> go.Figure:
    """Create interactive spending forecast curve with upper/lower confidence ribbons."""
    fig = go.Figure()
    
    # Historical series if available
    if historical_points:
        df_hist = pd.DataFrame(historical_points)
        if "date" in df_hist.columns and "amount" in df_hist.columns:
            fig.add_trace(go.Scatter(
                x=df_hist["date"],
                y=df_hist["amount"],
                mode='lines+markers',
                name='Historical Spending',
                line=dict(color='#94A3B8', width=2),
                marker=dict(size=4),
                hovertemplate='<b>Actual</b>: $%{y:,.2f}<extra></extra>'
            ))

    # Forecast series
    if forecast_points:
        df_fore = pd.DataFrame(forecast_points)
        # Upper Bound (transparent)
        fig.add_trace(go.Scatter(
            x=df_fore["date"],
            y=df_fore["upper_bound"],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        # Lower Bound + Fill
        fig.add_trace(go.Scatter(
            x=df_fore["date"],
            y=df_fore["lower_bound"],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(59, 130, 246, 0.18)',
            name='Confidence Interval (90%)',
            hoverinfo='skip'
        ))
        # Mean Predicted Line
        fig.add_trace(go.Scatter(
            x=df_fore["date"],
            y=df_fore["predicted_amount"],
            mode='lines+markers',
            name='AI Forecast (LSTM/GBM)',
            line=dict(color='#3B82F6', width=3, dash='dash'),
            marker=dict(size=5, color='#60A5FA'),
            hovertemplate='<b>Forecast</b>: $%{y:,.2f}<extra></extra>'
        ))

    fig.update_layout(
        title="<b>Spending Trajectory & 30-Day Deep Learning Forecast</b>",
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zeroline=False, tickprefix="$"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **CHART_THEME
    )
    return fig

def create_portfolio_distribution_chart(allocation: Dict[str, float]) -> go.Figure:
    """Create portfolio allocation chart."""
    labels = list(allocation.keys())
    values = list(allocation.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4']),
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b>: %{value:.1f}%<extra></extra>'
    )])
    fig.update_layout(title="<b>Portfolio Asset Class Allocation</b>", **CHART_THEME)
    return fig
