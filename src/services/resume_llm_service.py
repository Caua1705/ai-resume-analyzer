from langchain_openai import ChatOpenAI

from src.prompts.resume_analysis_prompt import build_resume_analysis_prompt
from src.schemas.candidate_analysis_schema import CandidateAnalysis


class LLMResumeAnalyzer:

    def __init__(self, api_key: str):

        model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
        )

        structured_model = model.with_structured_output(
            CandidateAnalysis
        )

        prompt = build_resume_analysis_prompt()

        self.chain = prompt | structured_model

    def analyze(self, job, resumes_texts: list[str]):

        inputs = [
            {
                "job_name": job.name,
                "main_activities": job.main_activities,
                "prerequisites": job.prerequisites,
                "differentials": job.differentials,
                "curriculo": text,
            }
            for text in resumes_texts
        ]

        responses = self.chain.batch(inputs)

        return responses