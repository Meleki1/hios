from datetime import datetime, UTC
from uuid import uuid4
from sqlalchemy import DateTime, Float, Integer

from sqlalchemy import (
    DateTime,
    Float,
    JSON,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from pgvector.sqlalchemy import Vector
from hios.db.base import Base


class MemoryRecord(Base):

    __tablename__ = "memory_entries"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=1.0,
    )

    details: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(1536),
        nullable=True,
    )

    importance = mapped_column(
        Float,
        nullable=False,
        default=0.5,
    )

    access_count = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    last_accessed_at = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )