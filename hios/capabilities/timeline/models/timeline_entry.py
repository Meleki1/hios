from datetime import datetime, timezone
from uuid import uuid4
from pydantic import Field
from hios.shared.base import HIOSModel


class TimelineEntry(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    subject_id: str

    event_type: str

    event_name: str

    state: str

    description: str

    resource_id: str | None = None

    resource_type: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )