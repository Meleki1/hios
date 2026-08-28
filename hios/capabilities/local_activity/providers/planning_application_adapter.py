from datetime import datetime

from hios.capabilities.local_activity.models.planning_application import (
    PlanningApplication,
)


class PlanningApplicationAdapter:

    def from_raw(
        self,
        data: dict,
    ) -> PlanningApplication:

        return PlanningApplication(
            reference=data["reference"],
            category=data["category"],
            status=data["status"],
            description=data.get(
                "description",
            ),
            latitude=float(
                data["latitude"],
            ),
            longitude=float(
                data["longitude"],
            ),
            observed_at=datetime.fromisoformat(
                data["observed_at"],
            ),
            source=data["source"],
            source_url=data.get(
                "source_url",
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )