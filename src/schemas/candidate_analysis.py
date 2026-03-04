from pydantic import BaseModel, Field
from typing import List

class CandidateAnalysis(BaseModel):

    score: float = Field(description="Candidate score from 0 to 100")

    opinion: str = Field(description="Short evaluation of the candidate")

    languages: List[str] = Field(description="Languages mentioned in resume")

    education: List[str] = Field(description="Education mentioned in resume")