from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.education_levels_model import EducationLevel
from typing import List

class EducationLevelRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> EducationLevel:

        query = select(EducationLevel).where(
            EducationLevel.name == name
        )

        result = self.db.execute(query)

        return result.scalars().first()
    
    #METODO TESTE
    def get_all(self) -> List[EducationLevel]:
        query  = select(EducationLevel)
        result = self.db.execute(query)
        return result.scalars().all()