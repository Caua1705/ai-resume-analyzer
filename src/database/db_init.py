from src.database.base import Base
from src.database.session import engine
from src.models.analysis_model import Analysis
from src.models.job_model import Job
from src.models.resume_model import Resume
from src.models.education_levels_model import EducationLevel

def criar_tabelas():
    Base.metadata.create_all(engine)
