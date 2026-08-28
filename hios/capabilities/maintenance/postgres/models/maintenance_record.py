import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base


class MaintenanceRecord(Base):

    __tablename__ = "maintenance_records"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    subject_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    home_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    task: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    maintenance_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="planned",
    )

    scheduled_for: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    evidence: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    extra_data: Mapped[dict[str, str]] = mapped_column(
        "metadata",
        JSON,
        nullable=False,
        default=dict,
    )