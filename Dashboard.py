import streamlit as st

from src.database.session import SessionLocal
from src.database.db_init import create_tables

from src.repositories.job_repository import JobRepository
from src.repositories.analysis_repository import AnalysisRepository

from src.services.analysis_dataframe_service import analyses_to_dataframe
from src.services.dashboard_metrics_service import (
    calculate_dashboard_metrics,
    calculate_score_distribution,
    calculate_average_score_by_education,
)
from src.services.ranking_service import prepare_top_candidates

from src.ui.dashboard_sidebar import render_dashboard_sidebar
from src.ui.dashboard_metrics import render_dashboard_metrics, apply_metric_style
from src.ui.dashboard_charts import (
    render_score_distribution,
    render_education_score_chart,
)
from src.ui.dashboard_top_candidates import render_top_candidates
from src.ui.analyzer_layout import render_section_divider

from src.config.settings import SUPABASE_URL


st.set_page_config(page_title="Dashboard", layout="wide")


@st.cache_resource
def init_db():
    create_tables()


init_db()


def main():

    with SessionLocal() as db:

        job_repo = JobRepository(db)
        analysis_repo = AnalysisRepository(db)

        jobs = job_repo.get_all()

        selected_job, score_range = render_dashboard_sidebar(jobs)

        if selected_job == "All Jobs":
            st.title("Candidate Analytics — All Jobs")
            analyses = analysis_repo.get_filtered(score_range=score_range)
        else:
            st.title(f"Candidate Analytics — {selected_job.name}")
            analyses = analysis_repo.get_filtered(
                job_id=selected_job.id,
                score_range=score_range,
            )

        df_base = analyses_to_dataframe(analyses)

        metrics = calculate_dashboard_metrics(df_base)

        apply_metric_style()
        render_dashboard_metrics(metrics)

        score_dist = calculate_score_distribution(df_base)
        education_avg = calculate_average_score_by_education(df_base)

        col1, col2 = st.columns(2)

        with col1:
            render_score_distribution(score_dist)

        with col2:
            render_education_score_chart(education_avg)

        render_section_divider()

        top_candidates = prepare_top_candidates(df_base, SUPABASE_URL)

        render_top_candidates(top_candidates)

        render_section_divider()


if __name__ == "__main__":
    main()