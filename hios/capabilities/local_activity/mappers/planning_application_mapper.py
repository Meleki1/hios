from hios.capabilities.local_activity.models.local_activity_event import (
    LocalActivityEvent,
)
from hios.capabilities.local_activity.models.planning_application import (
    PlanningApplication,
)


class PlanningApplicationMapper:

    def to_event(
        self,
        application: PlanningApplication,
    ) -> LocalActivityEvent:

        return LocalActivityEvent(
            event_type=(
                "planning_application"
            ),
            category=application.category,
            latitude=application.latitude,
            longitude=application.longitude,
            status=application.status,
            observed_at=application.observed_at,
            source=application.source,
            source_reference=application.reference,
            metadata={
                "description": (
                    application.description
                    or ""
                ),
                "source_url": (
                    application.source_url
                    or ""
                ),
                **application.metadata,
            },
        )