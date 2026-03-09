import streamlit as st

def render_header():

    st.title("AI Resume Analyzer")

    st.markdown(
        "<hr style='margin-top:10px;margin-bottom:15px;border:1px solid #e6e6e6;'>",
        unsafe_allow_html=True
    )