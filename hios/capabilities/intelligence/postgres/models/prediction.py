from uuid import uuid4

from sqlalchemy import Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class PredictionRecord(Base):

    __tablename__ = "intelligence_predictions"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    subject_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    target: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    horizon_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    probability: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
    )

    evidence: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    intent_score: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )