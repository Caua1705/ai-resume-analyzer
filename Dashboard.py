from src.services.dashboard_service import (
    calcular_score_distribution,
    calcular_media_por_educacao
)

import streamlit as st

from src.ui.analyzer_section_divider import render_section_divider
from src.database.session import SessionLocal
from src.database.db_init import criar_tabelas

from src.repositories.job_repository import JobRepository
from src.repositories.analysis_repository import AnalysisRepository

from src.services.dataframe_service import analyses_to_dataframe
from src.services.dashboard_service import calcular_metricas_dashboard

from src.ui.dashboard_sidebar import render_dashboard_sidebar
from src.ui.dashboard_metrics import render_dashboard_metrics
from src.ui.dashboard_styles import aplicar_estilo_metricas
from src.ui.dashboard_charts import (
    render_score_distribution,
    render_education_score_chart
)

from src.core.config import SUPABASE_URL


st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

criar_tabelas()


def score_badge(score):

    if score >= 85:
        return "🟢 Excellent"
    elif score >= 70:
        return "🟡 Good"
    elif score >= 50:
        return "🟠 Moderate"
    elif score >= 30:
        return "🔴 Weak"
    else:
        return "⚫ Very Weak"


def main():

    with SessionLocal() as db:

        job_repo = JobRepository(db)
        analysis_repo = AnalysisRepository(db)

        jobs = job_repo.get_all()

        selected_job, score_range = render_dashboard_sidebar(jobs)

        if selected_job == "All Jobs":
            st.title("Candidate Analytics — All Jobs")
        else:
            st.title(f"Candidate Analytics — {selected_job.name}")

        if selected_job == "All Jobs":
            analyses = analysis_repo.get_filtered(
                score_range=score_range
            )
        else:
            analyses = analysis_repo.get_filtered(
                job_id=selected_job.id,
                score_range=score_range
            )

        df_base = analyses_to_dataframe(analyses)

        metrics = calcular_metricas_dashboard(df_base)

        aplicar_estilo_metricas({
            "col1": "#2563eb",
            "col2": "#10b981",
            "col3": "#f59e0b",
            "col4": "#ef4444"
        })

        render_dashboard_metrics(metrics)

        score_dist = calcular_score_distribution(df_base)
        media = calcular_media_por_educacao(df_base)

        col1, col2 = st.columns(2)

    with col1:
        render_score_distribution(score_dist)

    with col2:
        render_education_score_chart(media)

    render_section_divider()
# ----------------------------------------------------------------------------
    st.subheader("Top Candidates")

    if df_base.empty:
        st.info("No candidates found with the selected filters.")
        return

    df_base["resume"] = df_base["file_path"].apply(
        lambda x: f"{SUPABASE_URL}/storage/v1/object/public/curriculos/{x}"
    )

    df_base = df_base.sort_values("score", ascending=False)

    top_candidates = df_base.head(3)

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

    render_section_divider()

if __name__ == "__main__":
    main()