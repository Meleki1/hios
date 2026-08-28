import pytest

from hios.capabilities.assistant.context.home_context_assembler import (
    HomeContextAssembler,
)
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)


class FakeHomeRepository:

    async def get(self, home_id):
        return {
            "id": home_id,
        }


class FakeInformationRepository:

    async def get_by_home(self, home_id):
        return {
            "home_id": home_id,
        }


class FakeStateRepository:

    async def get_by_home(self, home_id):
        return {
            "home_id": home_id,
        }


class FakeTimelineService:

    def __init__(self):
        self.entries = [
            TimelineEntry(
                subject_id="subject-1",
                event_type="outreach",
                event_name="maintenance_alert_sent",
                state="sent",
                description="Maintenance alert sent: Inspect roof",
                resource_id="Inspect roof",
                resource_type="maintenance",
            )
        ]

    async def get_by_subject(self, subject_id):
        return [
            entry
            for entry in self.entries
            if entry.subject_id == subject_id
        ]

@pytest.mark.asyncio
async def test_home_context_includes_timeline_history():

    timeline_service = FakeTimelineService()

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(),
        information_repository=FakeInformationRepository(),
        state_repository=FakeStateRepository(),
        timeline_service=timeline_service,
    )

    context = await assembler.assemble(
        home_id="home-1",
        subject_id="subject-1",
        message="What happened with my roof?",
    )

    assert len(context.timeline) == 1

    entry = context.timeline[0]

    assert entry.subject_id == "subject-1"
    assert entry.event_type == "outreach"
    assert entry.event_name == "maintenance_alert_sent"
    assert entry.state == "sent"
    assert entry.resource_type == "maintenance"
    assert entry.resource_id == "Inspect roof"