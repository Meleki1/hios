from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from hios.shared.value_object import ValueObject


class AuditInfo(ValueObject):
    """
    Audit metadata for an entity.
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )