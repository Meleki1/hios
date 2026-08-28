from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from hios.db.base import Base
from hios.capabilities.consent.models.consent import ConsentPurpose


class ConsentRecord(Base):
    __tablename__ = "consents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    subject_id: Mapped[str] = mapped_column(
        String(36),
        index=True,
        nullable=False,
    )

    purpose: Mapped[ConsentPurpose] = mapped_column(
        Enum(ConsentPurpose),
        nullable=False,
    )

    granted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    granted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )