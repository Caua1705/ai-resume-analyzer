from langchain_openai import ChatOpenAI
from src.prompts.resume_analysis_prompt import build_resume_analysis_prompt
from src.schemas.candidate_analysis_schema import CandidateAnalysis

class LLMResumeAnalyzer:

    def __init__(self, api_key):
        prompt = build_resume_analysis_prompt()

        model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key
        )

        structured = model.with_structured_output(CandidateAnalysis)

        self.chain = prompt | structured

    def analyze(self, job, texto):

        return self.chain.invoke({
            "job_name": job.name,
            "main_activities": job.main_activities,
            "prerequisites": job.prerequisites,
            "differentials": job.differentials,
            "curriculo": texto
        })