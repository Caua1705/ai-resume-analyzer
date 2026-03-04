from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    analysis_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="CASCADE"),
        nullable=False
    )

    language: Mapped[str] = mapped_column(Text, nullable=False)

    analysis: Mapped["Analysis"] = relationship(back_populates="languages")