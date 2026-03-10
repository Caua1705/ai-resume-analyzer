import streamlit as st

def render_ranking(df):

    st.subheader("Ranking de candidatos")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )