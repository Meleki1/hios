from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class BaseEvent:
    event_type: str
    event_name: str
    state: str
    description: str
    subject_id: str
    resource_id: str | None = None
    resource_type: str | None = None
    created_at: datetime | None = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(
                timezone.utc
            )