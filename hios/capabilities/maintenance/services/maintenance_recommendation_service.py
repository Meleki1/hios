from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceStatus,
    MaintenanceType,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)


class MaintenanceRecommendationService:

    def __init__(
        self,
        maintenance_repository,
    ):
        self._maintenance_repository = (
            maintenance_repository
        )

    async def accept(
        self,
        *,
        recommendation: MaintenanceRecommendation,
    ) -> Maintenance:

        existing = (
            await self._maintenance_repository.find_active_by_task(
                home_id=recommendation.home_id,
                task=recommendation.task,
            )
        )

        if existing is not None:
            return existing

        maintenance = Maintenance(
            subject_id=recommendation.subject_id,
            home_id=recommendation.home_id,
            task=recommendation.task,
            maintenance_type=MaintenanceType(
                recommendation.maintenance_type
            ),
            status=MaintenanceStatus.PLANNED,
            scheduled_for=(
                recommendation.recommended_for
            ),
            metadata={
                **recommendation.metadata,
                "recommendation_reason": (
                    recommendation.reason
                ),
            },
        )

        return await self._maintenance_repository.create(
            maintenance
        )