from src.config.config import METRIC_COLORS
import streamlit as st


def aplicar_estilo_metricas():

    cores = METRIC_COLORS

    st.markdown(f"""
    <style>
        .stMetric {{
            background-color: #ffffff;
            border-radius: 10px;
            padding: 12px;
            box-shadow: 0 0 5px rgba(0,0,0,0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            color: #111827;
        }}

        .stMetric:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}

        [data-testid="stColumn"]:nth-of-type(1) .stMetric {{
            border-left: 6px solid {cores.get("col1")};
        }}

        [data-testid="stColumn"]:nth-of-type(2) .stMetric {{
            border-left: 6px solid {cores.get("col2")};
        }}

        [data-testid="stColumn"]:nth-of-type(3) .stMetric {{
            border-left: 6px solid {cores.get("col3")};
        }}

        [data-testid="stColumn"]:nth-of-type(4) .stMetric {{
            border-left: 6px solid {cores.get("col4")};
        }}
    </style>
    """, unsafe_allow_html=True)


def render_dashboard_metrics(metrics):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Candidates Analyzed", metrics["total"])

    with col2:
        st.metric("Average Candidate Score", f"{metrics['avg']:.1f}")

    with col3:
        st.metric("Best Candidate Score", f"{metrics['best']:.1f}")

    with col4:
        st.metric("Qualified Candidates", metrics["qualified"])