import pytest

from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.repositories.postgres_timeline_repository import (
    PostgresTimelineRepository,
)
from hios.db.session import SessionLocal


@pytest.mark.asyncio
async def test_postgres_timeline_repository_saves_and_reads_entry():
    entry = TimelineEntry(
        subject_id="test-home-1",
        event_type="maintenance",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Roof maintenance alert sent.",
        resource_id="maintenance-1",
        resource_type="maintenance",
    )

    async with SessionLocal() as session:
        repository = PostgresTimelineRepository(
            session=session,
        )

        saved = await repository.save(entry)

        results = await repository.get_by_subject(
            "test-home-1",
        )

    assert saved.id == entry.id
    assert saved.subject_id == "test-home-1"
    assert saved.event_type == "maintenance"
    assert saved.event_name == "maintenance_alert_sent"
    assert saved.state == "sent"
    assert saved.description == "Roof maintenance alert sent."
    assert saved.resource_id == "maintenance-1"
    assert saved.resource_type == "maintenance"

    assert len(results) == 1

    result = results[0]

    assert result.id == entry.id
    assert result.subject_id == entry.subject_id
    assert result.event_type == entry.event_type
    assert result.event_name == entry.event_name
    assert result.state == entry.state
    assert result.description == entry.description
    assert result.resource_id == entry.resource_id
    assert result.resource_type == entry.resource_type
    assert result.created_at == entry.created_at