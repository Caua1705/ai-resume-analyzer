from sqlalchemy.orm import Session
from src.models.resume_model import Resume


class ResumeRepository:

    def __init__(self, db: Session):
        self.db = db

    def add_resume(self, file_path: str, raw_content: str, job_id) -> Resume:

        resume = Resume(
            file_path=file_path,
            raw_content=raw_content,
            job_id=job_id
        )

        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)

        return resume