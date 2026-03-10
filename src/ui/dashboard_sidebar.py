import streamlit as st


def render_dashboard_sidebar(jobs, education_levels):

    with st.sidebar:

        st.title("Dashboard Filters")

        # ---------- JOB ----------
        job_options = ["All Jobs"] + jobs

        selected_job = st.selectbox(
            "Job",
            job_options,
            format_func=lambda j: j if j == "All Jobs" else j.name
        )

        # ---------- EDUCATION ----------
        selected_education = st.multiselect(
            "Education Level",
            education_levels,
            default=education_levels,  # todos selecionados por padrão
            format_func=lambda e: e.name
        )

        # ---------- SCORE ----------
        score_range = st.slider(
            "Score Range",
            min_value=0,
            max_value=100,
            value=(0, 100)
        )

    return selected_job, selected_education, score_range