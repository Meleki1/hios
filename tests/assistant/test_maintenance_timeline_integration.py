import pytest

from hios.capabilities.assistant.graph.nodes import create_nodes
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.capabilities.assistant.models.outreach_decision import (
    OutreachDecision,
)
from hios.capabilities.assistant.response.assistant_action_response_builder import (
    AssistantActionResponseBuilder,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.outreach.models import (
    OutreachDeliveryStatus,
)
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)
from hios.capabilities.timeline.listeners.timeline_listener import (
    TimelineListener,
)

class FakeTimelineRepository:

    def __init__(self):
        self.entries = []

    async def save(self, entry):
        self.entries.append(entry)
        return entry

    async def get_by_subject(self, subject_id):
        return [
            entry
            for entry in self.entries
            if entry.subject_id == subject_id
        ]


class FakeEventPublisher:

    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def publish(self, event):
        for subscriber in self.subscribers:
            await subscriber.listen(event)


class FakeOutreach:

    async def reason(self, request, context):
        class Result:
            status = OutreachDeliveryStatus.SENT

        return Result()

@pytest.mark.asyncio
async def test_high_priority_maintenance_flows_to_timeline():

    repository = FakeTimelineRepository()

    timeline_service = TimelineService(
        repository=repository,
    )

    timeline_listener = TimelineListener(
        service=timeline_service,
    )

    event_publisher = FakeEventPublisher()

    event_publisher.subscribe(
        timeline_listener,
    )

    fake_outreach = FakeOutreach()

    nodes = create_nodes(
        context_assembler=None,
        router=None,
        hios=None,
        intelligence_graph=None,
        maintenance_intelligence=None,
        outreach=fake_outreach,
        event_publisher=event_publisher,
        action_response_builder=AssistantActionResponseBuilder(),
    )

    recommendation = MaintenanceRecommendation(
        subject_id="subject-1",
        home_id="home-1",
        task="Inspect roof",
        reason="Roof inspection is overdue.",
        maintenance_type="roof",
        priority="high",
    )

    state = {
        "subject_id": "subject-1",
        "home_id": "home-1",
        "metadata": {
            "email": "test@example.com",
        },
        "maintenance_recommendations": [
            recommendation,
        ],
        "outreach_decision": OutreachDecision(
            required=True,
            reason=(
                "A high-priority maintenance recommendation "
                "requires user notification."
            ),
            priority="high",
        ),
    }

    result = await nodes["execute_outreach"](
        state,
    )

    assert "outreach_result" in result

    entries = await repository.get_by_subject(
        "subject-1",
    )

    assert len(entries) == 1

    entry = entries[0]

    assert entry.subject_id == "subject-1"
    assert entry.event_type == "outreach"
    assert entry.event_name == "maintenance_alert_sent"
    assert entry.state == "sent"
    assert entry.resource_type == "maintenance"
    assert entry.resource_id == "Inspect roof"