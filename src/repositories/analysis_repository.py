from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.analysis_model import Analysis


class AnalysisRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_filtered(
        self,
        job_id: Optional[str] = None,
        score_range: Optional[Tuple[int, int]] = None,
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
                    score_range[1],
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
        score: float,
        opinion: str,
        strengths: str,
        weaknesses: str,
        languages,
    ) -> Analysis:

        analysis = Analysis(
            resume_id=resume_id,
            job_id=job_id,
            education_level_id=education_level_id,
            score=score,
            opinion=opinion,
            strengths=strengths,
            weaknesses=weaknesses,
            languages=languages,
        )

        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        return analysis