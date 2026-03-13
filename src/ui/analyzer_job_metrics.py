import streamlit as st


def render_job_metrics(job, analyses):

    st.subheader("Job Analysis")

    col1, col2 = st.columns(2)

    col1.metric("Analyzed Candidates", len(analyses))
    col2.metric("Job", job.name)