from hios.capabilities.maintenance.models.maintenance_intelligence_result import (
    MaintenanceIntelligenceResult,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.maintenance.models.maintenance_timeline import (
    MaintenanceTimelineItem,
)


def test_maintenance_intelligence_result_contains_recommendations_and_timeline():

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
    )

    timeline_item = MaintenanceTimelineItem(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        item_type="recommendation",
        status="recommended",
        maintenance_type="preventive",
    )

    result = MaintenanceIntelligenceResult(
        recommendations=[recommendation],
        timeline=[timeline_item],
    )

    assert result.recommendations == [
        recommendation,
    ]

    assert result.timeline == [
        timeline_item,
    ]