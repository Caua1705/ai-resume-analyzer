import streamlit as st

from src.database.session import SessionLocal
from src.database.db_init import criar_tabelas

from src.repositories.job_repository import JobRepository
from src.repositories.education_level_repository import EducationLevelRepository
from src.repositories.analysis_repository import AnalysisRepository
from src.repositories.resume_repository import ResumeRepository

from src.services.pdf_service import extrair_texto_pdf
from src.services.resume_analysis_llm_service import LLMResumeAnalyzer
from src.services.storage_service import upload_curriculo

from src.ui.sidebar import render_sidebar
from src.ui.header import render_header
from src.ui.ranking_table import render_ranking

from src.core.config import OPENAI_API_KEY


st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

criar_tabelas()

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

with SessionLocal() as db:
    jobs = JobRepository(db).get_all()

vaga_escolhida, arquivos, analisar = render_sidebar(
    jobs,
    st.session_state["uploader_key"]
)

render_header()

if vaga_escolhida:

    st.subheader("Análise da vaga")

    with SessionLocal() as db:
        analises = AnalysisRepository(db).get_all(job_id=vaga_escolhida.id)

    col1, col2 = st.columns(2)

    col1.metric("Candidatos analisados", len(analises))
    col2.metric("Vaga", vaga_escolhida.name)

if analisar and arquivos:

    if len(arquivos) > 10:
        st.error("Você só pode enviar no máximo 10 currículos.")
        st.stop()

    progress_bar = st.progress(0)
    status = st.empty()

    with st.spinner("Analisando currículos com IA..."):

        total = len(arquivos)

        textos = []

        for i, arquivo in enumerate(arquivos, start=1):

            texto = extrair_texto_pdf(arquivo.getvalue())
            textos.append(texto)

            status.text(f"Extraindo texto {i}/{total}")
            progress_bar.progress(int(i * 40 / total))

        analyzer = LLMResumeAnalyzer(OPENAI_API_KEY)
        responses = analyzer.analyze(vaga_escolhida, textos)


        with SessionLocal() as db:

            edu_repo = EducationLevelRepository(db)
            resume_repo = ResumeRepository(db)
            analise_repo = AnalysisRepository(db)

            for i, arquivo in enumerate(arquivos):

                texto = textos[i]
                resp = responses[i]

                file_path = upload_curriculo(
                    arquivo.getvalue(),
                    vaga_escolhida.name
                )

                resume = resume_repo.add_resume(
                    file_path,
                    texto,
                    vaga_escolhida.id
                )

                analise_repo.add_analysis(
                    resume_id=resume.id,
                    job_id=vaga_escolhida.id,
                    education_level_id=edu_repo.get_by_name(resp.education_level).id,
                    score=resp.score,
                    opinion=resp.opinion,
                    strengths=resp.strengths,
                    weaknesses=resp.weaknesses,
                    languages=resp.languages
                )

                status.text(f"Processando currículo {i+1}/{total}")
                progress_bar.progress(40 + int((i + 1) / total * 60))

    progress_bar.empty()
    status.empty()

    st.success("Currículos analisados com sucesso.")

    st.session_state["uploader_key"] += 1
    st.rerun()

if vaga_escolhida:

    with SessionLocal() as db:
        analises = AnalysisRepository(db).get_all(job_id=vaga_escolhida.id)

    if analises:
        render_ranking(analises)
    else:
        st.info("Nenhum currículo analisado para essa vaga ainda.")