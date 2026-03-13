import streamlit as st

def render_ranking(df):
    st.subheader("Ranking de candidatos")

    st.data_editor(
        df,
        hide_index=True,
        column_config={
            "Resume": st.column_config.LinkColumn(
                "Resume",
                help="Open candidate resume",
                display_text="Open resume"
            )
        },
        use_container_width=True
    )