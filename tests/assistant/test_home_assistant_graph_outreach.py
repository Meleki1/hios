import pytest

from hios.capabilities.assistant.graph.workflow import (
    build_home_assistant_graph,
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
from hios.capabilities.assistant.models.outreach_decision import (
    OutreachDecision,
)
from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)
from hios.capabilities.timeline.listeners.timeline_listener import (
    TimelineListener,
)
from tests.assistant.test_nodes import FakeHIOS
from tests.assistant.test_maintenance_timeline_integration import FakeEventPublisher, FakeTimelineRepository



class FakeRouter:
    def route(self, message):
        return None

class FakeMaintenanceIntelligence:

    async def analyze(
        self,
        *,
        subject_id,
        home_id,
        timeline,
        maintenance_records,
        explicit_intents,
    ):
        return [
            MaintenanceRecommendation(
                subject_id=subject_id,
                home_id=home_id,
                task="Inspect roof",
                reason="Roof inspection is overdue.",
                maintenance_type="roof",
                priority="high",
            )
        ]

class FakeOutreach:

    async def reason(self, request, context):

        class Result:
            status = OutreachDeliveryStatus.SENT

        return Result()

class FakeContextAssembler:

    async def assemble(
        self,
        *,
        home_id,
        subject_id,
        message,
    ):
        class Context:
            timeline = []
            maintenance_records = []

        return Context()

class FakeIntelligenceGraph:

    async def ainvoke(self, state):
        return {
            "signals": [],
            "risk": None,
            "intent_score": None,
            "prediction": None,
        }


@pytest.mark.asyncio
async def test_end_to_end():
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

    graph = build_home_assistant_graph(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=FakeIntelligenceGraph(),
        maintenance_intelligence=FakeMaintenanceIntelligence(),
        outreach=FakeOutreach(),
        event_publisher=event_publisher,
    )

    result = await graph.ainvoke(
        {
            "subject_id": "subject-1",
            "home_id": "home-1",
            "conversation_id": "conversation-1",
            "message": "My roof inspection is overdue.",
            "image": None,
            "metadata": {
                "email": "test@example.com",
            },
        }
    )
    assert result["outreach_decision"].required is True
    assert (
        result["outreach_result"].status
        == OutreachDeliveryStatus.SENT
    )

    entries = await repository.get_by_subject(
        "subject-1",
    )

    assert len(entries) == 1

    entry = entries[0]

    assert entry.event_type == "outreach"
    assert entry.event_name == "maintenance_alert_sent"
    assert entry.state == "sent"
    assert entry.subject_id == "subject-1"
    assert entry.resource_type == "maintenance"
    assert entry.resource_id == "Inspect roof"