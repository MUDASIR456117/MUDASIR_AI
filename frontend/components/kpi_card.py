import streamlit as st

def render_kpi_card(title: str, value: str, badge_text: str = "", badge_type: str = "success",
                    variant: str = "blue", subtitle: str = ""):
    """Render a luxury glassmorphism KPI card."""
    badge_html = f'<div class="kpi-badge badge-{badge_type}">{badge_text}</div>' if badge_text else ''
    subtitle_html = f'<div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">{subtitle}</div>' if subtitle else ''
    
    html = f"""
    <div class="kpi-card {variant}">
        <div class="kpi-label">{title}</div>
        <div class="kpi-value">{value}</div>
        {badge_html}
        {subtitle_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_ai_insight(text: str, icon: str = "💡", tag: str = "AI Insight"):
    html = f"""
    <div class="ai-insight-box">
        <div style="font-size: 1.4rem;">{icon}</div>
        <div>
            <div style="font-size: 0.75rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">{tag}</div>
            <div class="ai-insight-text">{text}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
