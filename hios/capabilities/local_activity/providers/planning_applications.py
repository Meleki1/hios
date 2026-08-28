from hios.capabilities.local_activity.local_activity_provider import (
    LocalActivityProvider,
)
from hios.capabilities.local_activity.models.local_activity_event import (
    LocalActivityEvent,
)


class MockPlanningApplicationProvider(
    LocalActivityProvider
):

    async def get_events(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> list[LocalActivityEvent]:

        return [
            LocalActivityEvent(
                event_type=(
                    "planning_application_approved"
                ),
                category="restaurant",
                latitude=latitude + 0.005,
                longitude=longitude + 0.005,
                status="approved",
                source="planning_authority",
                source_reference="PA-001",
                metadata={
                    "development_type": (
                        "restaurant"
                    ),
                },
            )
        ]