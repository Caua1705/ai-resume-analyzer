import streamlit as st


def render_dashboard_metrics(metrics):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Candidates Analyzed", metrics["total"])

    with col2:
        st.metric("Average Candidate Score", round(metrics["avg"], 1))

    with col3:
        st.metric("Best Candidate Score", round(metrics["best"], 1))

    with col4:
        st.metric("Qualified Candidates", metrics["qualified"])