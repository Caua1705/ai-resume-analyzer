from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.education_level_model import EducationLevel


class EducationLevelRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_name(
        self,
        name: str,
    ) -> Optional[EducationLevel]:

        query = select(EducationLevel).where(
            EducationLevel.name == name
        )

        result = self.db.execute(query)

        return result.scalars().first()