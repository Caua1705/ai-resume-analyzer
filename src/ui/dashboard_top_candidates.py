import streamlit as st
from src.ui.dashboard_helpers import score_badge


def render_top_candidates(df, supabase_url):

    st.subheader("Top Candidates")

    if df.empty:
        st.info("No candidates found with the selected filters.")
        return

    df = df.copy()

    df["resume"] = df["file_path"].apply(
        lambda x: f"{supabase_url}/storage/v1/object/public/curriculos/{x}"
    )

    df = df.sort_values("score", ascending=False)

    top_candidates = df.head(3)

    for _, row in top_candidates.iterrows():

        badge = score_badge(row["score"])

        languages = (
            ", ".join(row["languages"][:2])
            if row["languages"]
            else "No languages"
        )

        titulo = f"Score {row['score']} — {row['education_level']} — {languages} {badge}"

        with st.expander(titulo):

            col1, col2 = st.columns([3,1])

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
                    use_container_width=True
                )