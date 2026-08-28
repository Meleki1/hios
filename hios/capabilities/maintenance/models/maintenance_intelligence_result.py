from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.maintenance.models.maintenance_timeline import (
    MaintenanceTimelineItem,
)


class MaintenanceIntelligenceResult:
    def __init__(
        self,
        *,
        recommendations: list[MaintenanceRecommendation],
        timeline: list[MaintenanceTimelineItem],
    ):
        self.recommendations = recommendations
        self.timeline = timeline