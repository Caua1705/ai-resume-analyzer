import streamlit as st

from src.config.settings import METRIC_COLORS


def score_badge(score):

    if score >= 85:
        return "🟢 Excellent"
    if score >= 70:
        return "🟡 Good"
    if score >= 50:
        return "🟠 Moderate"
    if score >= 30:
        return "🔴 Weak"

    return "⚫ Very Weak"


def apply_metric_style():

    colors = METRIC_COLORS

    st.markdown(
        f"""
        <style>
        .stMetric {{
            background-color: #ffffff;
            border-radius: 10px;
            padding: 12px;
        }}

        [data-testid="stColumn"]:nth-of-type(1) .stMetric {{
            border-left: 6px solid {colors.get("col1")};
        }}

        [data-testid="stColumn"]:nth-of-type(2) .stMetric {{
            border-left: 6px solid {colors.get("col2")};
        }}

        [data-testid="stColumn"]:nth-of-type(3) .stMetric {{
            border-left: 6px solid {colors.get("col3")};
        }}

        [data-testid="stColumn"]:nth-of-type(4) .stMetric {{
            border-left: 6px solid {colors.get("col4")};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_metrics(metrics):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Candidates", metrics["total"])

    with col2:
        st.metric("Average Score", f"{metrics['avg']:.1f}")

    with col3:
        st.metric("Best Score", f"{metrics['best']:.1f}")

    with col4:
        st.metric("Qualified Candidates", metrics["qualified"])