from datetime import datetime, timezone

from hios.core.events.base_event import BaseEvent


class HomeCreatedEvent(BaseEvent):

    def __init__(
        self,
        home_id: str,
        subject_id: str 
    ):
        super().__init__(
            event_type="home",
            event_name="home_created",
            state="created",
            description="Home created successfully",
            created_at=datetime.now(timezone.utc),
            resource_id=home_id,
            resource_type="home",
            subject_id=subject_id,
        )