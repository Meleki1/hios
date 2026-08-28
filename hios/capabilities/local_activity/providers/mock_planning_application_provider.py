from datetime import datetime, timezone

from hios.capabilities.local_activity.models.planning_application import (
    PlanningApplication,
)

from hios.capabilities.local_activity.providers.planning_application_provider import (
    PlanningApplicationProvider,
)


class MockPlanningApplicationProvider(
    PlanningApplicationProvider
):

    async def get_recent_applications(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> list[PlanningApplication]:

        return [
            PlanningApplication(
                reference="PA-001",
                category="restaurant",
                status="approved",
                description=(
                    "New restaurant development"
                ),
                latitude=latitude + 0.005,
                longitude=longitude + 0.005,
                observed_at=datetime.now(
                    timezone.utc
                ),
                source="planning_authority",
                source_url=(
                    "https://example.gov.uk/PA-001"
                ),
                metadata={
                    "development_type": (
                        "restaurant"
                    ),
                },
            )
        ]