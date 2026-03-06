import streamlit as st

from src.database.session import SessionLocal
from src.repositories.job_repository import JobRepository
from src.repositories.education_level_repository import EducationLevelRepository
from src.repositories.analysis_repository import AnalysisRepository
from src.repositories.resume_repository import ResumeRepository

from src.database.db_init import criar_tabelas
from src.services.pdf_service import extrair_texto_pdf
from src.services.storage_service import upload_curriculo
from src.services.resume_analysis_llm_service import LLMResumeAnalyzer

from src.core.config import OPENAI_API_KEY


criar_tabelas()


# carregar vagas
with SessionLocal() as db:
    repo = JobRepository(db)
    jobs = repo.get_all()


vaga_escolhida = st.selectbox(
    "Selecione uma vaga",
    jobs,
    format_func=lambda job: job.name
)


arquivos = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=True
)


if arquivos:

    if len(arquivos) > 10:
        st.error("Você só pode enviar no máximo 10 currículos.")
        st.stop()

    if st.button("Fazer análise"):

        analyzer = LLMResumeAnalyzer(OPENAI_API_KEY)

        textos = []

        # 1️⃣ extrair texto de todos PDFs
        for arquivo in arquivos:

            pdf_bytes = arquivo.getvalue()

            texto = extrair_texto_pdf(pdf_bytes)

            textos.append(texto)

        # 2️⃣ análise em batch na IA
        responses = analyzer.analyze(
            vaga_escolhida,
            textos
        )

        with SessionLocal() as db:

            repo_education = EducationLevelRepository(db)
            repo_resume = ResumeRepository(db)
            analise_repo = AnalysisRepository(db)

            for i, response in enumerate(responses):

                arquivo = arquivos[i]
                texto = textos[i]

                # 3️⃣ upload só depois da IA
                pdf_bytes = arquivo.getvalue()

                file_path = upload_curriculo(
                    pdf_bytes,
                    vaga_escolhida.name
                )

                education = repo_education.get_by_name(
                    response.education_level
                )

                resume = repo_resume.add_resume(
                    file_path,
                    texto,
                    vaga_escolhida.id
                )

                analise_repo.add_analysis(
                    resume_id=resume.id,
                    job_id=vaga_escolhida.id,
                    education_level_id=education.id,
                    score=response.score,
                    opinion=response.opinion,
                    strengths=response.strengths,
                    weaknesses=response.weaknesses,
                    languages=response.languages
                )

                st.write(f"Currículo analisado: {arquivo.name}")

        st.success("Todos os currículos foram analisados!")