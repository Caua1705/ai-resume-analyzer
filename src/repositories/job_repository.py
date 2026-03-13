from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.job_model import Job


class JobRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Job]:

        query = select(Job).order_by(
            Job.created_at.desc()
        )

        result = self.db.execute(query)

        return result.scalars().all()

    def create(
        self,
        name: str,
        main_activities: str,
        prerequisites: str,
        differentials: str,
    ) -> Job:

        job = Job(
            name=name,
            main_activities=main_activities,
            prerequisites=prerequisites,
            differentials=differentials,
            created_at=datetime.utcnow(),
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job