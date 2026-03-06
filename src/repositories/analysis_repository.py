from sqlalchemy.orm import Session
from src.models.analysis_model import Analysis


class AnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def add_analysis(
        self,
        resume_id,
        job_id,
        education_level_id,
        score,
        opinion,
        strengths,
        weaknesses,
        languages
    ) -> Analysis:

        analysis = Analysis(
            resume_id=resume_id,
            job_id=job_id,
            education_level_id=education_level_id,
            score=score,
            opinion=opinion,
            strengths=strengths,
            weaknesses=weaknesses,
            languages=languages
        )

        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        return analysis