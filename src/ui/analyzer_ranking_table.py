import streamlit as st


def render_candidate_ranking(df):

    st.subheader("Candidate Ranking")

    st.data_editor(
        df,
        hide_index=True,
        column_config={
            "Resume": st.column_config.LinkColumn(
                "Resume",
                help="Open candidate resume",
                display_text="Open resume",
            )
        },
        use_container_width=True,
    )