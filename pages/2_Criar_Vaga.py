import streamlit as st
from src.database.session import SessionLocal
from src.repositories.job_repository import JobRepository
from src.database.db_init import criar_tabelas

st.set_page_config(
    page_title="Criar Vaga",
    layout="wide"
)

criar_tabelas()


# ==============================
# HEADER
# ==============================

st.title("📌 Criar Nova Vaga")

st.markdown(
    "Preencha as informações abaixo para criar uma nova vaga que será utilizada na análise de currículos."
)

st.markdown("---")


# ==============================
# FORMULÁRIO
# ==============================

with st.container():

    with st.form("create_job_form"):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Nome da vaga",
                placeholder="Ex: Estágio em Data Science"
            )

        st.markdown("### 📋 Descrição da vaga")

        main_activities = st.text_area(
            "Principais atividades",
            placeholder="Descreva as principais responsabilidades da vaga...",
            height=150
        )

        prerequisites = st.text_area(
            "Pré-requisitos",
            placeholder="Ex: Python, SQL, estatística básica...",
            height=150
        )

        differentials = st.text_area(
            "Diferenciais",
            placeholder="Ex: experiência com IA, projetos pessoais, portfólio...",
            height=150
        )

        st.markdown("")

        submitted = st.form_submit_button(
            "🚀 Criar Vaga",
            use_container_width=True
        )


# ==============================
# PROCESSAMENTO
# ==============================

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

        st.success("✅ Vaga criada com sucesso!")

        st.info(f"ID da vaga: **{job.id}**")