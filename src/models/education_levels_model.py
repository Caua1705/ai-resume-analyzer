import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from typing import List
from src.database.base import Base


class EducationLevel(Base):
    __tablename__ = "education_levels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(Text, nullable=False)

    analyses: Mapped[List["Analysis"]] = relationship(
        back_populates="education_level"
    )