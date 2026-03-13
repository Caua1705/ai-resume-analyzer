import streamlit as st

from src.ui.dashboard_metrics import score_badge


def render_top_candidates(df):

    st.subheader("Top Candidates")

    if df.empty:
        st.info("No candidates found.")
        return

    for _, row in df.iterrows():

        badge = score_badge(row["score"])

        languages = (
            ", ".join(row["languages"][:2])
            if row["languages"]
            else "No languages"
        )

        title = (
            f"Score {row['score']} — "
            f"{row['education_level']} — "
            f"{languages} {badge}"
        )

        with st.expander(title):

            col1, col2 = st.columns([3, 1])

            with col1:

                st.write("**Languages**")
                st.write(
                    ", ".join(row["languages"])
                    if row["languages"]
                    else "Not specified"
                )

                st.write("**Strengths**")
                st.write(row["strengths"])

                st.write("**Weaknesses**")
                st.write(row["weaknesses"])

                st.write("**AI Opinion**")
                st.write(row["opinion"])

            with col2:

                st.link_button(
                    "Open Resume",
                    row["resume"],
                    use_container_width=True,
                )