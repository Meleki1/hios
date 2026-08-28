from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class TimelineEntryRecord(Base):
    __tablename__ = "timeline_entries"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    subject_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    event_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    resource_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    resource_type: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )