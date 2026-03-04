from pydantic import BaseModel, Field
from typing import List


class CandidateAnalysis(BaseModel):

    score: float = Field(
        description="Candidate score from 0 to 100"
    )

    opinion: str = Field(
        description="Short evaluation of the candidate"
    )

    strengths: str = Field(
        description="Main strengths of the candidate related to the job"
    )

    weaknesses: str = Field(
        description="Main weaknesses or missing skills of the candidate"
    )

    languages: List[str] = Field(
        description="Languages mentioned in the resume"
    )

    education_level: str = Field(
        description="Highest education level found in the resume"
    )