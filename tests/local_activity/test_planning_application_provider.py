import pytest

from hios.capabilities.local_activity.models.planning_application import (
    PlanningApplication,
)
from hios.capabilities.local_activity.providers.mock_planning_application_provider import (
    MockPlanningApplicationProvider,
)


@pytest.mark.asyncio
async def test_mock_planning_application_provider_returns_planning_applications():

    provider = MockPlanningApplicationProvider()

    applications = await provider.get_recent_applications(
        latitude=51.5074,
        longitude=-0.1278,
        radius_km=5.0,
    )

    assert len(applications) == 1

    application = applications[0]

    assert isinstance(
        application,
        PlanningApplication,
    )

    assert application.reference == "PA-001"

    assert application.category == (
        "restaurant"
    )

    assert application.status == "approved"

    assert application.description == (
        "New restaurant development"
    )

    assert application.latitude == pytest.approx(
        51.5124
    )

    assert application.longitude == pytest.approx(
        -0.1228
    )

    assert application.source == (
        "planning_authority"
    )

    assert application.source_url == (
        "https://example.gov.uk/PA-001"
    )

    assert application.metadata[
        "development_type"
    ] == "restaurant"

    assert application.observed_at is not None