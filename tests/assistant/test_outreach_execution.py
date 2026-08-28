import pytest

from hios.capabilities.assistant.graph.nodes import create_nodes
from hios.capabilities.assistant.models.outreach_decision import (
    OutreachDecision,
)
from hios.capabilities.assistant.response.assistant_action_response_builder import (
    AssistantActionResponseBuilder,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.outreach.contracts import OutreachResult
from hios.capabilities.outreach.models import OutreachChannel, OutreachDeliveryStatus
from hios.capabilities.timeline.listeners.timeline_listener import TimelineListener
from hios.capabilities.timeline.services.timeline_service import TimelineService
from hios.core.events.base_event import BaseEvent
from tests.timeline.test_timeline_repository import FakeTimelineRepository
from hios.core.events.event_publisher import EventPublisher




class FakeEventPublisher:

    def __init__(self):
        self.events = []
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def publish(self, event):
        self.events.append(event)

        for subscriber in self.subscribers:
            await subscriber.listen(event)

class FakeOutreach:
    def __init__(self):
        self.requests = []

    async def reason(self, request, context):
        self.requests.append(request)

        return OutreachResult(
            status=OutreachDeliveryStatus.SENT,
            channel=OutreachChannel.EMAIL,
            recipient=request.recipient,
            message_id="test-message-id",
        )


@pytest.mark.asyncio
async def test_high_priority_maintenance_executes_outreach():

    fake_outreach = FakeOutreach()

    nodes = create_nodes(
        context_assembler=None,
        router=None,
        hios=None,
        intelligence_graph=None,
        maintenance_intelligence=None,
        outreach=fake_outreach,
        action_response_builder=AssistantActionResponseBuilder(),
    )

    recommendation = MaintenanceRecommendation(
        subject_id="subject-123",
        home_id="home-123",
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
            MaintenanceRecommendation(
                subject_id="subject-1",
                home_id="home-1",
                task="Inspect roof",
                reason="Roof inspection is overdue.",
                maintenance_type="roof",
                priority="high",
            )
        ],
        "outreach_decision": OutreachDecision(
            required=True,
            reason="A high-priority maintenance recommendation requires user notification.",
            priority="high",
        ),
    }

    result = await nodes["execute_outreach"](state)

   

    assert len(fake_outreach.requests) == 1

    request = fake_outreach.requests[0]

    assert request.recipient == "test@example.com"
    assert request.channel == OutreachChannel.EMAIL
    assert request.subject == (
        "HIOS Maintenance Alert: Inspect roof"
    )
    assert "Roof inspection is overdue." in request.message
    assert "Priority: high" in request.message
    assert result["outreach_result"].status == OutreachDeliveryStatus.SENT
    assert result["outreach_result"].message_id == "test-message-id"


@pytest.mark.asyncio
async def test_high_priority_maintenance_executes_outreach():

    fake_outreach = FakeOutreach()
    event_publisher = FakeEventPublisher()
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
        subject_id="subject-123",
        home_id="home-123",
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
            MaintenanceRecommendation(
                subject_id="subject-1",
                home_id="home-1",
                task="Inspect roof",
                reason="Roof inspection is overdue.",
                maintenance_type="roof",
                priority="high",
            )
        ],
        "outreach_decision": OutreachDecision(
            required=True,
            reason="A high-priority maintenance recommendation requires user notification.",
            priority="high",
        ),
    }

    result = await nodes["execute_outreach"](state)

    assert len(event_publisher.events) == 1

    event = event_publisher.events[0]

    assert event.event_type == "outreach"
    assert event.event_name == "maintenance_alert_sent"
    assert event.state == "sent"
    assert event.subject_id == "subject-1"
    assert event.resource_type == "maintenance"
    assert event.resource_id == "Inspect roof"

@pytest.mark.asyncio
async def test_timeline_listener_records_event():
    repository = FakeTimelineRepository()
    service = TimelineService(repository)
    listener = TimelineListener(service)

    event = BaseEvent(
        event_type="outreach",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Maintenance alert sent: Inspect roof",
        subject_id="subject-1",
        resource_id="Inspect roof",
        resource_type="maintenance",
    )

    await listener.listen(event)

    assert len(repository.entries) == 1

    entry = repository.entries[0]

    assert entry.subject_id == "subject-1"
    assert entry.event_type == "outreach"
    assert entry.event_name == "maintenance_alert_sent"
    assert entry.state == "sent"
    assert entry.description == "Maintenance alert sent: Inspect roof"
    assert entry.resource_id == "Inspect roof"
    assert entry.resource_type == "maintenance"

@pytest.mark.asyncio
async def test_high_priority_maintenance_outreach_is_recorded_on_timeline():

    # Timeline infrastructure
    repository = FakeTimelineRepository()
    timeline_service = TimelineService(repository)
    timeline_listener = TimelineListener(timeline_service)

    # Event infrastructure
    event_publisher = FakeEventPublisher()
    event_publisher.subscribe(timeline_listener)

    # Outreach infrastructure
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

    result = await nodes["execute_outreach"](state)

    # Outreach succeeded
    assert result["outreach_result"].status == (
        OutreachDeliveryStatus.SENT
    )

    # Event was published
    assert len(event_publisher.events) == 1

    event = event_publisher.events[0]

    assert event.event_type == "outreach"
    assert event.event_name == "maintenance_alert_sent"
    assert event.state == "sent"
    assert event.subject_id == "subject-1"

    # Timeline listener consumed the event
    assert len(repository.entries) == 1

    entry = repository.entries[0]

    assert entry.subject_id == "subject-1"
    assert entry.event_type == "outreach"
    assert entry.event_name == "maintenance_alert_sent"
    assert entry.state == "sent"
    assert entry.resource_id == "Inspect roof"
    assert entry.resource_type == "maintenance"

@pytest.mark.asyncio
async def test_timeline_listener_records_event():
    repository = FakeTimelineRepository()
    service = TimelineService(repository)
    listener = TimelineListener(service)

    event = BaseEvent(
        event_type="outreach",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Maintenance alert sent: Inspect roof",
        subject_id="subject-1",
        resource_id="Inspect roof",
        resource_type="maintenance",
    )

    await listener.listen(event)

    assert len(repository.entries) == 1

    entry = repository.entries[0]

    assert entry.subject_id == "subject-1"
    assert entry.event_type == "outreach"
    assert entry.event_name == "maintenance_alert_sent"
    assert entry.state == "sent"
    assert entry.description == (
        "Maintenance alert sent: Inspect roof"
    )
    assert entry.resource_id == "Inspect roof"
    assert entry.resource_type == "maintenance"


class FakeSubscriber:

    def __init__(self):
        self.events = []

    async def listen(
        self,
        event: BaseEvent,
    ) -> None:
        self.events.append(event)


@pytest.mark.asyncio
async def test_event_publisher_notifies_subscribers():
    publisher = EventPublisher()
    subscriber = FakeSubscriber()

    publisher.subscribe(subscriber)

    event = BaseEvent(
        event_type="outreach",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Maintenance alert sent",
        subject_id="subject-1",
    )

    await publisher.publish(event)

    assert subscriber.events == [event]