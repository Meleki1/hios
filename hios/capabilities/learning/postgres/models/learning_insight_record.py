from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class LearningInsightModel(Base):
    __tablename__ = "learning_insights"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    target: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    signal_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    sample_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    correct_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    incorrect_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    accuracy: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    insight: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )