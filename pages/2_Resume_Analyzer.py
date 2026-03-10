import streamlit as st

from src.database.session import SessionLocal
from src.database.db_init import criar_tabelas

from src.repositories.job_repository import JobRepository
from src.repositories.education_level_repository import EducationLevelRepository
from src.repositories.analysis_repository import AnalysisRepository
from src.repositories.resume_repository import ResumeRepository

from src.services.analysis_pipeline_service import run_resume_analysis_pipeline

from src.ui.analyzer_sidebar import render_sidebar
from src.ui.analyzer_header import render_header
from src.ui.analyzer_ranking_table import render_ranking
from src.services.ranking_service import build_ranking_dataframe
from src.ui.analyzer_job_metrics import render_job_metrics
from src.ui.analyzer_section_divider import render_section_divider


st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

criar_tabelas()

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0


def main():

    with SessionLocal() as db:

        job_repo = JobRepository(db)
        edu_repo = EducationLevelRepository(db)
        resume_repo = ResumeRepository(db)
        analysis_repo = AnalysisRepository(db)

        jobs = job_repo.get_all()

        vaga_escolhida, arquivos, analisar = render_sidebar(
            jobs,
            st.session_state["uploader_key"]
        )

        render_header()

        if analisar and arquivos:

            if len(arquivos) > 10:
                st.error("You can upload a maximum of 10 resumes.")
                st.stop()

            status = st.empty()
            progress_bar = st.progress(0)

            status.write("Extracting text from resumes...")
            progress_bar.progress(30)


            run_resume_analysis_pipeline(
                arquivos,
                vaga_escolhida,
                edu_repo,
                resume_repo,
                analysis_repo
            )

            progress_bar.progress(100)
            status.write("Analysis completed.")

            st.session_state["uploader_key"] += 1
            st.rerun()

        if vaga_escolhida:

            analises = analysis_repo.get_all(
                job_id=vaga_escolhida.id
            )

            render_job_metrics(
                vaga_escolhida,
                analises
            )

            if analises:
                df_analises = build_ranking_dataframe(analises)
                render_section_divider()
                render_ranking(df_analises)
            else:
                st.info("No resumes analyzed for this job yet.")


if __name__ == "__main__":
    main()