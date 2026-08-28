from datetime import datetime, timezone

from hios.capabilities.local_activity.models.local_activity_event import (
    LocalActivityEvent,
)

from hios.capabilities.local_activity.models.provider_result import (
    LocalActivityProviderResult,
    ProviderStatus,
)


def test_provider_result_represents_success():

    event = LocalActivityEvent(
        event_type="planning_application",
        category="restaurant",
        latitude=51.5074,
        longitude=-0.1278,
        source="planning_authority",
        source_reference="PA-001",
        observed_at=datetime.now(
            timezone.utc,
        ),
        metadata={
            "development_type": "restaurant",
        },
    )

    result = LocalActivityProviderResult(
        status=ProviderStatus.SUCCESS,
        provider="planning_authority",
        events=[event],
    )

    assert result.status == (
        ProviderStatus.SUCCESS
    )

    assert len(result.events) == 1

    assert result.error is None


def test_provider_result_represents_unavailable():

    result = LocalActivityProviderResult(
        status=ProviderStatus.UNAVAILABLE,
        provider="planning_authority",
        error="Planning API unavailable",
    )

    assert result.status == (
        ProviderStatus.UNAVAILABLE
    )

    assert result.events == []

    assert result.error == (
        "Planning API unavailable"
    )


def test_provider_result_represents_partial_data():

    result = LocalActivityProviderResult(
        status=ProviderStatus.PARTIAL,
        provider="planning_authority",
        error="Some records could not be processed",
    )

    assert result.status == (
        ProviderStatus.PARTIAL
    )

    assert result.events == []

    assert result.error is not None