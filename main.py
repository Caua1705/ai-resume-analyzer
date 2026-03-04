import streamlit as st

from src.database.session import SessionLocal
from src.repositories.job_repository import JobRepository
from src.database.db_init import criar_tabelas

from src.services.pdf_service import extrair_texto_pdf
from src.services.storage_service import upload_curriculo
from src.services.resume_analysis_service import analisar_curriculo

from src.core.config import OPENAI_API_KEY

criar_tabelas()

with SessionLocal() as db:
    repo = JobRepository(db)
    jobs = repo.get_all()

vaga_escolhida = st.selectbox(
    "Selecione uma vaga",
    jobs,
    format_func=lambda job: job.name
)

arquivo = st.file_uploader("Upload PDF", type="pdf")

if arquivo:

    pdf_bytes = arquivo.getvalue()

    file_path = upload_curriculo(
        pdf_bytes,
        vaga_escolhida.name
    )

    texto = extrair_texto_pdf(pdf_bytes)

    resposta = analisar_curriculo(
        vaga_escolhida,
        texto,
        OPENAI_API_KEY
    )

    st.write(resposta.model_dump())