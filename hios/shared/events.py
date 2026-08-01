from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class DomainEvent(HIOSModel):
    """
    Base class for all domain events.
    """

    event_id: UUID = Field(default_factory=uuid4)

    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    event_type: str