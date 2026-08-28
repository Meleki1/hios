from datetime import datetime, timezone

from pydantic import Field

from hios.shared.base import HIOSModel


class LocalActivityEvent(HIOSModel):

    event_type: str

    category: str

    latitude: float | None = None

    longitude: float | None = None

    status: str | None = None

    observed_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc,
        )
    )

    source: str

    source_reference: str | None = None

    metadata: dict[str, str] = Field(
        default_factory=dict,
    )