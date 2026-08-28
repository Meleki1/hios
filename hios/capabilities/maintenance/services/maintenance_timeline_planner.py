from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.maintenance.models.maintenance_timeline import (
    MaintenanceTimelineItem,
    MaintenanceTimelineItemType,
)
from datetime import datetime, timezone


class MaintenanceTimelinePlanner:

    async def build(
        self,
        *,
        subject_id: str,
        home_id: str,
        maintenance_records: list[Maintenance] | None = None,
        recommendations: list[
            MaintenanceRecommendation
        ] | None = None,
    ) -> list[MaintenanceTimelineItem]:

        maintenance_records = (
            maintenance_records or []
        )

        recommendations = recommendations or []

        timeline: list[MaintenanceTimelineItem] = []

        # Existing maintenance
        for maintenance in maintenance_records:

            if maintenance.subject_id != subject_id:
                continue

            if maintenance.home_id != home_id:
                continue

            timeline.append(
                MaintenanceTimelineItem(
                    subject_id=maintenance.subject_id,
                    home_id=maintenance.home_id,
                    task=maintenance.task,
                    item_type=(
                        MaintenanceTimelineItemType.MAINTENANCE
                    ),
                    status=maintenance.status.value,
                    scheduled_for=(
                        maintenance.scheduled_for
                    ),
                    maintenance_type=(
                        maintenance.maintenance_type.value
                    ),
                    metadata=maintenance.metadata,
                )
            )

        # Intelligence recommendations
        for recommendation in recommendations:

            if recommendation.subject_id != subject_id:
                continue

            if recommendation.home_id != home_id:
                continue

            timeline.append(
                MaintenanceTimelineItem(
                    subject_id=recommendation.subject_id,
                    home_id=recommendation.home_id,
                    task=recommendation.task,
                    item_type=(
                        MaintenanceTimelineItemType.RECOMMENDATION
                    ),
                    status="recommended",
                    recommended_for=(
                        recommendation.recommended_for
                    ),
                    maintenance_type=(
                        recommendation.maintenance_type
                    ),
                    reason=recommendation.reason,
                    priority=recommendation.priority,
                    source_signals=(
                        recommendation.source_signals
                    ),
                    metadata=recommendation.metadata,
                )
            )

        timeline.sort(
            key=lambda item: (
                item.scheduled_for
                or item.recommended_for
                or datetime.max.replace(
                    tzinfo=timezone.utc
                )
            )
        )

        return timeline