import streamlit as st

from src.database.session import SessionLocal
from src.database.db_init import criar_tabelas

from src.repositories.job_repository import JobRepository
from src.repositories.analysis_repository import AnalysisRepository

from src.services.dataframe_service import analyses_to_dataframe
from src.services.dashboard_service import build_dashboard_dataframe

from src.ui.dashboard_sidebar import render_dashboard_sidebar

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
            analyses = analysis_repo.get_filtered(
                score_range=score_range
            )
        else:
            analyses = analysis_repo.get_filtered(
                job_id=selected_job.id,
                score_range=score_range
            )

        df_base = analyses_to_dataframe(analyses)

        df_dashboard = build_dashboard_dataframe(df_base)

        st.write(df_dashboard)


        total_candidatos = len(df_dashboard)
        media_scores = df_dashboard['score'].mean()
        maior_score = df_dashboard['score'].max()
        qualificados = df_dashboard.loc[df_dashboard['score']>=70] 


        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Total Candidates Analyzed', total_candidatos)
        with col2:
            st.metric('Average Candidate Score', media_scores)
        with col3:
            st.metric('Best Candidate Score', maior_score)
        with col4:
            st.metric('Qualified Candidate', len(qualificados))



if __name__ == "__main__":
    main()