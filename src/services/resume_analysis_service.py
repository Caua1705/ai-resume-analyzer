from langchain_openai import ChatOpenAI
from src.prompts.resume_analysis_prompt import build_resume_analysis_prompt
from src.schemas.candidate_analysis import CandidateAnalysis

def analisar_curriculo(job, texto, api_key):

    prompt = build_resume_analysis_prompt()

    model = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=api_key
    )

    structured_model = model.with_structured_output(CandidateAnalysis)

    chain = prompt | structured_model

    response = chain.invoke({
        "job_name": job.name,
        "main_activities": job.main_activities,
        "prerequisites": job.prerequisites,
        "differentials": job.differentials,
        "curriculo": texto
    })

    return response