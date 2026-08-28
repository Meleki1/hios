from datetime import datetime, timezone
from hios.capabilities.local_activity.models.planning_application import (
    PlanningApplication,
)

def test_planning_application_contains_normalized_fields():

    application = PlanningApplication(
        reference="PA-001",
        category="restaurant",
        status="approved",
        description="New restaurant development",
        latitude=51.5074,
        longitude=-0.1278,
        observed_at=datetime(
            2026,
            8,
            10,
            tzinfo=timezone.utc,
        ),
        source="planning_authority",
        source_url="https://example.gov.uk/PA-001",
        metadata={
            "ward": "Central",
        },
    )

    assert application.reference == "PA-001"

    assert application.category == (
        "restaurant"
    )

    assert application.status == "approved"

    assert application.latitude == 51.5074

    assert application.longitude == -0.1278

    assert application.source == (
        "planning_authority"
    )

    assert application.metadata["ward"] == (
        "Central"
    )