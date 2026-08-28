from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Float,
    JSON,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from hios.db.base import Base


class LearningRecordModel(Base):

    __tablename__ = "learning_records"

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

    evaluation_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    target: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    signal_names: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    signal_values: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    signal_strengths: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    signal_confidences: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    intent_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    prediction_confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    lesson: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )