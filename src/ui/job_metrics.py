import streamlit as st


def render_job_metrics(vaga, analises):
    st.subheader("Análise da vaga")

    col1, col2 = st.columns(2)

    col1.metric("Candidatos analisados", len(analises))
    col2.metric("Vaga", vaga.name)