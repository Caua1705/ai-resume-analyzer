from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from src.models.analysis_model import Analysis


class AnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_filtered(
        self,
        job_id=None,
        score_range=None
    ) -> List[Analysis]:

        query = select(Analysis)

        if job_id:
            query = query.where(
                Analysis.job_id == job_id
            )

        if score_range:
            query = query.where(
                Analysis.score.between(
                    score_range[0],
                    score_range[1]
                )
            )

        query = query.order_by(
            Analysis.created_at.desc()
        )

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