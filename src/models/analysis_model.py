from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from typing import List
from src.database.base import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    resume_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False
    )

    job_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    score: Mapped[float | None] = mapped_column(Float)
    opinion: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    resume: Mapped["Resume"] = relationship(back_populates="analyses")
    job: Mapped["Job"] = relationship(back_populates="analyses")

    educations: Mapped[List["Education"]] = relationship(
        back_populates="analysis",
        cascade="all, delete"
    )

    languages: Mapped[List["Language"]] = relationship(
        back_populates="analysis",
        cascade="all, delete"
    )