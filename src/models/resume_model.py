from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from typing import List
from src.database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    job_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    file_path: Mapped[str | None] = mapped_column(Text)
    raw_content: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    # relacionamento com Job
    job = relationship("Job", back_populates="resumes")

    # relacionamento com Analysis
    analyses: Mapped[List["Analysis"]] = relationship(
        back_populates="resume",
        cascade="all, delete"
    )