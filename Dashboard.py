from src.services.dashboard_service import (
    calcular_score_distribution,
    calcular_media_por_educacao
)

import streamlit as st

from src.ui.analyzer_section_divider import render_section_divider
from src.ui.dashboard_top_candidates import render_top_candidates

from src.database.session import SessionLocal
from src.database.db_init import criar_tabelas

from src.repositories.job_repository import JobRepository
from src.repositories.analysis_repository import AnalysisRepository

from src.services.dataframe_service import analyses_to_dataframe
from src.services.dashboard_service import calcular_metricas_dashboard

from src.ui.dashboard_sidebar import render_dashboard_sidebar
from src.ui.dashboard_metrics import render_dashboard_metrics, aplicar_estilo_metricas
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

        aplicar_estilo_metricas()

        render_dashboard_metrics(metrics)

        score_dist = calcular_score_distribution(df_base)
        media = calcular_media_por_educacao(df_base)

        col1, col2 = st.columns(2)

    with col1:
        render_score_distribution(score_dist)

    with col2:
        render_education_score_chart(media)

    render_section_divider()

    render_top_candidates(df_base, SUPABASE_URL)

    render_section_divider()


if __name__ == "__main__":
    main()