import streamlit as st
from src.database.session import SessionLocal
from src.repositories.job_repository import JobRepository
from src.database.db_init import criar_tabelas

st.title("Criar Nova Vaga")

criar_tabelas()
with st.form("create_job_form"):

    name = st.text_input("Nome da Vaga")

    main_activities = st.text_area(
        "Main Activities",
        height=150
    )

    prerequisites = st.text_area(
        "Prerequisites",
        height=150
    )

    differentials = st.text_area(
        "Differentials",
        height=150
    )

    submitted = st.form_submit_button("Criar Vaga")

if submitted:

    if not name.strip():
        st.error("O nome da vaga é obrigatório.")
    else:
        with SessionLocal() as db:
            repo = JobRepository(db)

            job = repo.create(
                name=name,
                main_activities=main_activities,
                prerequisites=prerequisites,
                differentials=differentials
            )

        st.success("Vaga criada com sucesso!")
        st.write(f"ID da vaga: {job.id}")