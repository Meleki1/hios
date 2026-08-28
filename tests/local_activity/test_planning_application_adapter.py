from hios.capabilities.local_activity.providers.planning_application_adapter import (
    PlanningApplicationAdapter,
)


def test_planning_application_adapter_normalizes_raw_data():

    raw = {
        "reference": "PA-001",
        "category": "restaurant",
        "status": "approved",
        "description": "New restaurant development",
        "latitude": "51.5074",
        "longitude": "-0.1278",
        "observed_at": (
            "2026-08-10T12:00:00+00:00"
        ),
        "source": "planning_authority",
        "source_url": (
            "https://example.gov.uk/PA-001"
        ),
        "metadata": {
            "ward": "Central",
        },
    }

    adapter = PlanningApplicationAdapter()

    application = adapter.from_raw(
        raw,
    )

    assert application.reference == "PA-001"
    assert application.category == "restaurant"
    assert application.status == "approved"

    assert application.latitude == 51.5074
    assert application.longitude == -0.1278

    assert application.source == (
        "planning_authority"
    )

    assert application.metadata[
        "ward"
    ] == "Central"