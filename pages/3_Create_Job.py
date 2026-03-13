import streamlit as st

from src.database.session import SessionLocal
from src.database.db_init import create_tables

from src.repositories.job_repository import JobRepository
from src.ui.create_job_form import render_create_job_form


st.set_page_config(page_title="Create Job", layout="wide")


@st.cache_resource
def init_db():
    create_tables()


init_db()


def main():

    submitted, name, main_activities, prerequisites, differentials = (
        render_create_job_form()
    )

    if submitted:

        if not name.strip():
            st.error("Job title is required.")
            return

        with SessionLocal() as db:

            repo = JobRepository(db)

            job = repo.create(
                name=name,
                main_activities=main_activities,
                prerequisites=prerequisites,
                differentials=differentials,
            )

        st.success("Job created successfully.")
        st.info(f"Job ID: {job.id}")


if __name__ == "__main__":
    main()