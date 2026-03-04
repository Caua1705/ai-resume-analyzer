from langchain_core.prompts import ChatPromptTemplate

def build_resume_analysis_prompt():

    return ChatPromptTemplate.from_messages([
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