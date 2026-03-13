from src.database.base import Base
from src.database.session import engine

from src.models.analysis_model import Analysis
from src.models.education_level_model import EducationLevel
from src.models.job_model import Job
from src.models.resume_model import Resume


def create_tables() -> None:
    Base.metadata.create_all(engine)