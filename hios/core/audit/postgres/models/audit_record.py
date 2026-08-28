import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class AuditRecord(Base):

    __tablename__ = "audit_records"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    event_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    event_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    state: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    subject_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    resource_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        index=True,
    )

    resource_type: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    details: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )