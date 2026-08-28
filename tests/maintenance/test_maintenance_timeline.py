from datetime import datetime, timezone

from hios.capabilities.maintenance.models.maintenance_timeline import (
    MaintenanceTimelineItem,
    MaintenanceTimelineItemType,
)


def test_maintenance_timeline_item_can_represent_maintenance():

    scheduled_for = datetime(
        2026,
        9,
        1,
        tzinfo=timezone.utc,
    )

    item = MaintenanceTimelineItem(
        subject_id="household-1",
        home_id="home-1",
        task="Boiler service",
        item_type=MaintenanceTimelineItemType.MAINTENANCE,
        status="planned",
        scheduled_for=scheduled_for,
        maintenance_type="routine",
    )

    assert item.subject_id == "household-1"
    assert item.home_id == "home-1"
    assert item.task == "Boiler service"
    assert (
        item.item_type
        == MaintenanceTimelineItemType.MAINTENANCE
    )
    assert item.status == "planned"
    assert item.scheduled_for == scheduled_for
    assert item.maintenance_type == "routine"


def test_maintenance_timeline_item_can_represent_recommendation():

    recommended_for = datetime(
        2026,
        9,
        15,
        tzinfo=timezone.utc,
    )

    item = MaintenanceTimelineItem(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        item_type=MaintenanceTimelineItemType.RECOMMENDATION,
        status="recommended",
        recommended_for=recommended_for,
        maintenance_type="preventive",
        reason="Repeated pest-related concerns.",
        priority="normal",
        source_signals=[
            "Asked about mice",
            "Reported seeing mice again",
        ],
    )

    assert item.item_type == (
        MaintenanceTimelineItemType.RECOMMENDATION
    )
    assert item.task == "Pest inspection"
    assert item.status == "recommended"
    assert item.recommended_for == recommended_for
    assert item.reason == (
        "Repeated pest-related concerns."
    )
    assert item.priority == "normal"
    assert len(item.source_signals) == 2