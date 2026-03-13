import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    main_activities: Mapped[str | None] = mapped_column(Text)
    prerequisites: Mapped[str | None] = mapped_column(Text)
    differentials: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    resumes: Mapped[List["Resume"]] = relationship(
        back_populates="job",
        cascade="all, delete",
    )

    analyses: Mapped[List["Analysis"]] = relationship(
        back_populates="job",
        cascade="all, delete",
    )