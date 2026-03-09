from sqlalchemy.orm import Session
from src.models.analysis_model import Analysis
from sqlalchemy import select
from typing import List


class AnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, job_id) -> List[Analysis]:
            query  = select(Analysis).where(Analysis.job_id==job_id).order_by(Analysis.created_at.desc())
            result = self.db.execute(query)
            return result.scalars().all()
            
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