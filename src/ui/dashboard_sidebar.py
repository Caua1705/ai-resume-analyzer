import streamlit as st
from src.ui.analyzer_section_divider import render_section_divider


def render_dashboard_sidebar(jobs):

    with st.sidebar:

        st.title("📊 Dashboard")

        render_section_divider()

        st.markdown("**Filtros de análise**")

        job_options = ["All Jobs"] + jobs

        selected_job = st.selectbox(
            "Selecionar vaga",
            job_options,
            format_func=lambda j: j if j == "All Jobs" else j.name
        )

        score_range = st.slider(
            "Score dos candidatos",
            min_value=0,
            max_value=100,
            value=(0, 100)
        )

        render_section_divider()

    return selected_job, score_range