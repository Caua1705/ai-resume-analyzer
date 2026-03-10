from src.ui.dashboard_sidebar import render_dashboard_sidebar
from src.repositories.job_repository import JobRepository
from src.repositories.education_level_repository import EducationLevelRepository
from src.database.session import SessionLocal
from src.database.db_init import criar_tabelas

criar_tabelas()
with SessionLocal() as db:


    job_repo = JobRepository(db)
    edu_repo = EducationLevelRepository(db)

    jobs = job_repo.get_all()
    education_levels = edu_repo.get_all()

    selected_job, selected_education, score_range = render_dashboard_sidebar(
        jobs,
        education_levels
    )



