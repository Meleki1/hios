from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class OutcomeRecord(Base):

    __tablename__ = "intelligence_outcomes"

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

    subject_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    target: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    occurred: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    )

    details: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )