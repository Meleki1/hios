from __future__ import annotations

from datetime import UTC, datetime

from pydantic import Field

from hios.shared.value_object import ValueObject


class InvestigationBlocker(ValueObject):
    """
    Represents why an investigation cannot continue.
    """

    reason: str

    requested_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )