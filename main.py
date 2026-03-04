import streamlit as st
from src.schemas.analysis_schema import CandidateAnalysis
from src.database.session import SessionLocal
from src.repositories.job_repository import JobRepository
from src.database.db_init import criar_tabelas
from pypdf import PdfReader
import uuid
from src.core.supabase_client import supabase
import fitz
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
api_key_model = os.get_env("OPENAI_KEY")


criar_tabelas()



with SessionLocal() as db:
    instancia = JobRepository(db)
    repo = instancia.get_all()
   
vaga_escolhida = st.selectbox('Selecione uma vaga', 
                              repo, 
                              format_func=lambda job: job.name)

id_vaga_escolhida = vaga_escolhida.id
nome_vaga_escolhida = vaga_escolhida.name

arquivo = st.file_uploader("Upload PDF", type = 'pdf', accept_multiple_files=False)

st.write(f'ID vaga : {id_vaga_escolhida}')
st.write(f'Nome vaga: {nome_vaga_escolhida}')

if arquivo:
    st.write(f'PDF: {arquivo}')
    st.write(f'Tipo arquivo: {type(arquivo)}')
    st.write(f'Teste: {uuid.uuid4()}')

    #Salvar arquivo no bucket supabase
    file_id = str(uuid.uuid4())
    file_path = f"{vaga_escolhida.name}/{file_id}.pdf"
    pdf_bytes = arquivo.getvalue()

    supabase.storage.from_("curriculos").upload(
        file_path,
        pdf_bytes,
        {"content-type": "application/pdf"}
    )
    st.success("Arquivo Salvo")

    # ===== Extração de texto com PyMuPDF =====
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    texto_paginas = []

    for page in doc:
        texto_paginas.append(page.get_text())

    texto = "\n".join(texto_paginas)

    st.subheader("Texto extraído:")
    st.write(texto)

    
    #Estrutura de Análise Agente de IA

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Você é um recrutador técnico especialista em avaliação de candidatos."
        ),
        (
            "human",
            """
    Avalie o currículo abaixo com base na vaga.

    VAGA:
    Nome: {job_name}
    Atividades: {main_activities}
    Requisitos: {prerequisites}
    Diferenciais: {differentials}

    CURRÍCULO:
    {curriculo}
    """
        )
    ])

    model = ChatOpenAI(model="gpt-4o-mini", api_key=api_key_model)

    modelo_estruturado = model.with_structured_output(CandidateAnalysis)

    chain = prompt | modelo_estruturado

    response = chain.invoke(

        
    )


