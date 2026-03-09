import streamlit as st
import pandas as pd

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


st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
criar_tabelas()


# ==============================
# SESSION STATE
# ==============================

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0


# ==============================
# CARREGAR VAGAS
# ==============================

with SessionLocal() as db:
    repo_jobs = JobRepository(db)
    jobs = repo_jobs.get_all()

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.title("📄 Análise de currículos")

    vaga_escolhida = st.selectbox(
        "Selecionar vaga",
        jobs,
        format_func=lambda j: j.name
    )

    st.markdown("<hr style='margin-top:10px;margin-bottom:15px;'>", unsafe_allow_html=True)

    st.markdown("**Enviar currículos (PDF)**")
    st.caption("Máximo de 10 arquivos")

    arquivos = st.file_uploader(
        "Arraste ou selecione arquivos",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}"
    )

    if arquivos:
        st.caption(f"{len(arquivos)} arquivo(s) selecionado(s)")

    analisar = st.button("🚀 Analisar currículos", type="primary", use_container_width=True)


# ==============================
# HEADER
# ==============================

st.title("AI Resume Analyzer")

st.markdown(
    "<hr style='margin-top:10px;margin-bottom:15px;border:1px solid #e6e6e6;'>",
    unsafe_allow_html=True
)

if vaga_escolhida:

    st.subheader("Análise da vaga")

    with SessionLocal() as db:
        repo_analyzers = AnalysisRepository(db)
        analyzers = repo_analyzers.get_all(job_id=vaga_escolhida.id)
        total_analises = len(analyzers)

    col1, col2 = st.columns(2)
    col1.metric("Candidatos analisados", total_analises)
    col2.metric("Vaga", vaga_escolhida.name)


# ==============================
# PROCESSAR ANÁLISE
# ==============================

if analisar and arquivos:

    if len(arquivos) > 10:
        st.error("Você só pode enviar no máximo 10 currículos.")
        st.stop()

    progress_bar = st.progress(0)
    status = st.empty()

    with st.spinner("Analisando currículos com IA..."):

        total = len(arquivos)

        textos = []
        for i, arquivo in enumerate(arquivos):
            textos.append(extrair_texto_pdf(arquivo.getvalue()))

            status.text(f"Extraindo texto {i+1}/{total}")
            progress_bar.progress(int((i + 1) / total * 40))

        analyser = LLMResumeAnalyzer(OPENAI_API_KEY)
        responses = analyser.analyze(vaga_escolhida, textos)
 
        with SessionLocal() as db:

            edu_repo = EducationLevelRepository(db)
            resume_repo = ResumeRepository(db)
            analise_repo = AnalysisRepository(db)

            for i, arquivo in enumerate(arquivos):

                texto = textos[i]
                resp = responses[i]

                file_path = upload_curriculo(arquivo.getvalue(), vaga_escolhida.name)

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


# ==============================
# RESULTADOS
# ==============================

if vaga_escolhida:

    with SessionLocal() as db:
        analises = AnalysisRepository(db).get_all(job_id=vaga_escolhida.id)

    if analises:

        st.subheader("Ranking de candidatos")

        dados = []
        for a in analises:
            dados.append({
                "Score": a.score,
                "Languages": ", ".join(a.languages) if a.languages else "Not specified",
                "Strengths": (a.strengths[:80] + "...") if len(a.strengths) > 80 else a.strengths,
                "Weaknesses": (a.weaknesses[:80] + "...") if len(a.weaknesses) > 80 else a.weaknesses,
                "Created": pd.to_datetime(a.created_at).strftime("%d/%m/%Y %H:%M")
            })

        st.dataframe(dados, use_container_width=True, hide_index=True)

    else:
        st.info("Nenhum currículo analisado para essa vaga ainda.")