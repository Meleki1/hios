from datetime import datetime, timezone

from hios.capabilities.local_activity.mappers.planning_application_mapper import (
    PlanningApplicationMapper,
)
from hios.capabilities.local_activity.models.planning_application import (
    PlanningApplication,
)


def test_planning_application_mapper_creates_local_activity_event():

    observed_at = datetime(
        2026,
        8,
        10,
        tzinfo=timezone.utc,
    )

    application = PlanningApplication(
        reference="PA-001",
        category="restaurant",
        status="approved",
        description="New restaurant development",
        latitude=51.5074,
        longitude=-0.1278,
        observed_at=observed_at,
        source="planning_authority",
        source_url="https://example.gov.uk/PA-001",
        metadata={
            "ward": "Central",
        },
    )

    mapper = PlanningApplicationMapper()

    event = mapper.to_event(
        application,
    )

    assert event.event_type == (
        "planning_application"
    )

    assert event.category == "restaurant"

    assert event.status == "approved"

    assert event.latitude == 51.5074

    assert event.longitude == -0.1278

    assert event.observed_at == observed_at

    assert event.source == (
        "planning_authority"
    )

    assert event.source_reference == "PA-001"

    assert event.metadata[
        "description"
    ] == "New restaurant development"

    assert event.metadata[
        "source_url"
    ] == "https://example.gov.uk/PA-001"

    assert event.metadata[
        "ward"
    ] == "Central"