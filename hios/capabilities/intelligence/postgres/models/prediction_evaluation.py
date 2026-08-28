from uuid import uuid4

from sqlalchemy import Boolean, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class PredictionEvaluationRecord(Base):

    __tablename__ = "intelligence_prediction_evaluations"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    prediction_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    outcome_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    details: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )