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






