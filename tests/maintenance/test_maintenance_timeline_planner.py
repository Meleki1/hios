import pytest

from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceStatus,
    MaintenanceType,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.maintenance.services.maintenance_timeline_planner import (
    MaintenanceTimelinePlanner,
)
from hios.capabilities.maintenance.models.maintenance_timeline import (
    MaintenanceTimelineItemType,
)


@pytest.mark.asyncio
async def test_planner_combines_maintenance_and_recommendations():

    planner = MaintenanceTimelinePlanner()

    maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Boiler service",
        maintenance_type=MaintenanceType.ROUTINE,
        status=MaintenanceStatus.PLANNED,
    )

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
        priority="normal",
    )

    timeline = await planner.build(
        subject_id="household-1",
        home_id="home-1",
        maintenance_records=[maintenance],
        recommendations=[recommendation],
    )

    assert len(timeline) == 2

    assert timeline[0].task == "Boiler service"
    assert timeline[0].item_type == (
        MaintenanceTimelineItemType.MAINTENANCE
    )

    assert timeline[1].task == "Pest inspection"
    assert timeline[1].item_type == (
        MaintenanceTimelineItemType.RECOMMENDATION
    )

@pytest.mark.asyncio
async def test_planner_only_includes_requested_home():

    planner = MaintenanceTimelinePlanner()

    maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-2",
        task="Roof inspection",
        maintenance_type=MaintenanceType.ROUTINE,
        status=MaintenanceStatus.PLANNED,
    )

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
    )

    timeline = await planner.build(
        subject_id="household-1",
        home_id="home-1",
        maintenance_records=[maintenance],
        recommendations=[recommendation],
    )

    assert len(timeline) == 1
    assert timeline[0].task == "Pest inspection"

@pytest.mark.asyncio
async def test_planner_only_includes_requested_subject():

    planner = MaintenanceTimelinePlanner()

    maintenance = Maintenance(
        subject_id="household-2",
        home_id="home-1",
        task="Roof inspection",
        maintenance_type=MaintenanceType.ROUTINE,
        status=MaintenanceStatus.PLANNED,
    )

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
    )

    timeline = await planner.build(
        subject_id="household-1",
        home_id="home-1",
        maintenance_records=[maintenance],
        recommendations=[recommendation],
    )

    assert len(timeline) == 1
    assert timeline[0].task == "Pest inspection"

from datetime import datetime, timezone


@pytest.mark.asyncio
async def test_planner_orders_timeline_by_date():

    planner = MaintenanceTimelinePlanner()

    later_maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Roof inspection",
        maintenance_type=MaintenanceType.ROUTINE,
        status=MaintenanceStatus.PLANNED,
        scheduled_for=datetime(
            2026,
            10,
            1,
            tzinfo=timezone.utc,
        ),
    )

    earlier_maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Boiler service",
        maintenance_type=MaintenanceType.ROUTINE,
        status=MaintenanceStatus.PLANNED,
        scheduled_for=datetime(
            2026,
            9,
            1,
            tzinfo=timezone.utc,
        ),
    )

    recommendation = MaintenanceRecommendation(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
        recommended_for=datetime(
            2026,
            9,
            15,
            tzinfo=timezone.utc,
        ),
    )

    timeline = await planner.build(
        subject_id="household-1",
        home_id="home-1",
        maintenance_records=[
            later_maintenance,
            earlier_maintenance,
        ],
        recommendations=[
            recommendation,
        ],
    )

    assert [item.task for item in timeline] == [
        "Boiler service",
        "Pest inspection",
        "Roof inspection",
    ]