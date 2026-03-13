import streamlit as st

from src.database.session import SessionLocal
from src.database.db_init import create_tables

from src.repositories.job_repository import JobRepository
from src.repositories.education_level_repository import EducationLevelRepository
from src.repositories.analysis_repository import AnalysisRepository
from src.repositories.resume_repository import ResumeRepository

from src.services.resume_analysis_pipeline import run_resume_analysis_pipeline
from src.services.analysis_dataframe_service import analyses_to_dataframe
from src.services.ranking_service import build_ranking_dataframe

from src.ui.analyzer_sidebar import render_sidebar
from src.ui.analyzer_layout import render_header, render_section_divider
from src.ui.analyzer_ranking_table import render_candidate_ranking
from src.ui.analyzer_job_metrics import render_job_metrics

from src.config.settings import SUPABASE_URL


st.set_page_config(page_title="AI Resume Analyzer", layout="wide")


@st.cache_resource
def init_db():
    create_tables()


init_db()


if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0


def main():

    with SessionLocal() as db:

        job_repo = JobRepository(db)
        education_repo = EducationLevelRepository(db)
        resume_repo = ResumeRepository(db)
        analysis_repo = AnalysisRepository(db)

        jobs = job_repo.get_all()

        selected_job, files, analyze = render_sidebar(
            jobs,
            st.session_state["uploader_key"],
        )

        render_header()

        if analyze and files:

            if len(files) > 10:
                st.error("You can upload a maximum of 10 resumes.")
                st.stop()

            status = st.empty()
            progress_bar = st.progress(0)

            status.write("Extracting text from resumes...")
            progress_bar.progress(30)

            run_resume_analysis_pipeline(
                files,
                selected_job,
                education_repo,
                resume_repo,
                analysis_repo,
            )

            progress_bar.progress(100)
            status.write("Analysis completed.")

            st.session_state["uploader_key"] += 1
            st.rerun()

        if selected_job:

            analyses = analysis_repo.get_filtered(
                job_id=selected_job.id
            )

            render_job_metrics(selected_job, analyses)

            if analyses:

                df_base = analyses_to_dataframe(analyses)
                df_ranking = build_ranking_dataframe(
                    df_base,
                    SUPABASE_URL,
                )

                render_section_divider()
                render_candidate_ranking(df_ranking)
                render_section_divider()

                st.caption(
                    "Analysis generated automatically by AI Resume Analyzer. "
                    "Use the resume links to review candidates."
                )

            else:
                st.info("No resumes analyzed for this job yet.")


if __name__ == "__main__":
    main()