import streamlit as st
import pandas as pd

def render_ranking(analises):

    st.subheader("Ranking de candidatos")

    dados = []

    for a in analises:
        dados.append({
            "Score": a.score,
            "Languages": ", ".join(a.languages) if a.languages else "Not specified",
            "Strengths": (a.strengths[:80] + "...") if len(a.strengths) > 80 else a.strengths,
            "Weaknesses": (a.weaknesses[:80] + "...") if len(a.weaknesses) > 80 else a.weaknesses,
            "Created": pd.to_datetime(a.created_at).strftime("%d/%m/%Y %H:%M")
        })

    st.dataframe(dados, use_container_width=True, hide_index=True)