from pydantic import BaseModel, Field
from typing import List, Literal


class CandidateAnalysis(BaseModel):

    score: float = Field(
        ge=0,
        le=100,
        description="Candidate score from 0 to 100 based on how well the resume matches the job description"
    )

    opinion: str = Field(
        description="Short overall evaluation of the candidate"
    )

    strengths: str = Field(
        description="Main strengths of the candidate related to the job"
    )

    weaknesses: str = Field(
        description="Main weaknesses or missing skills of the candidate"
    )

    languages: List[str] = Field(
        description="Languages mentioned in the resume (example: English, Portuguese, Spanish)"
    )

    education_level: Literal[
        "High School",
        "Associate Degree",
        "Technical Degree",
        "Bachelor's Degree",
        "Postgraduate",
        "Master's Degree",
        "Doctorate",
        "Course / Certification",
        "Not Informed"
    ] = Field(
        description="Highest education level found in the resume"
    )