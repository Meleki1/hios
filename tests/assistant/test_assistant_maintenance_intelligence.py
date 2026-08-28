import pytest

from hios.capabilities.assistant.graph.nodes import create_nodes
from hios.capabilities.assistant.graph.state import HomeAssistantState
from hios.capabilities.assistant.models.interaction_understanding import (
    InteractionUnderstanding,
)
from hios.capabilities.assistant.models.home_context import (
    HomeContext,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.assistant.graph.workflow import build_home_assistant_graph
from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceStatus,
    MaintenanceType,
)



class FakeContextAssembler:
    async def assemble(
        self,
        *,
        home_id,
        subject_id,
        message,
    ):
        return None


class FakeRouter:
    def route(self, message):
        return None


class FakeIntelligenceGraph:
    def __init__(self):
        self.calls = []

    async def ainvoke(self, state):
        self.calls.append(state)

        return {
            "signals": ["maintenance-signal"],
            "risk": "medium",
            "intent_score": 0.8,
            "prediction": "maintenance-needed",
        }


class FakeMaintenanceIntelligence:
    def __init__(self):
        self.calls = []

    async def analyze(self, **kwargs):
        self.calls.append(kwargs)

        return [
            "maintenance-recommendation",
        ]


class FakeHios:
    async def execute(self, request):
        raise AssertionError(
            "Hios should not be called in this test."
        )


@pytest.mark.asyncio
async def test_assistant_intelligence_uses_maintenance_intelligence():

    intelligence_graph = FakeIntelligenceGraph()

    maintenance_intelligence = (
        FakeMaintenanceIntelligence()
    )

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHios(),
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=(
            maintenance_intelligence
        ),
    )
    
    context = HomeContext(
        home=object(),
        information=object(),
        state=object(),
        property_profile=None,
        memories=[],
        timeline=[
            "timeline-event-1",
            "timeline-event-2",
        ],
    )

    state: HomeAssistantState = {
        "subject_id": "household-1",
        "home_id": "home-1",
        "conversation_id": "conversation-1",
        "message": "I keep seeing mice in the kitchen.",
        "understanding": InteractionUnderstanding(
            explicit_intents=[
                "reported_active_problem",
            ],
        ),
        "context": context,
    }

    result = await nodes["intelligence"](state)

    assert result["maintenance_recommendations"] == [
        "maintenance-recommendation",
    ]

    assert len(
        maintenance_intelligence.calls
    ) == 1

    call = maintenance_intelligence.calls[0]

    assert call["subject_id"] == "household-1"
    assert call["home_id"] == "home-1"

    assert call["explicit_intents"] == [
        "reported_active_problem",
    ]
    assert call["timeline"] == [
        "timeline-event-1",
        "timeline-event-2",
    ]
    assert result["maintenance_recommendations"] == [
        "maintenance-recommendation",
    ]

    assert len(maintenance_intelligence.calls) == 1

    call = maintenance_intelligence.calls[0]

    assert call["subject_id"] == "household-1"
    assert call["home_id"] == "home-1"

    assert call["explicit_intents"] == [
        "reported_active_problem",
    ]

    assert call["timeline"] == [
        "timeline-event-1",
        "timeline-event-2",
    ]

@pytest.mark.asyncio
async def test_assistant_intelligence_passes_maintenance_records():

    intelligence_graph = FakeIntelligenceGraph()

    maintenance_intelligence = (
        FakeMaintenanceIntelligence()
    )

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHios(),
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=(
            maintenance_intelligence
        ),
    )

    context = HomeContext(
        home=object(),
        information=object(),
        state=object(),
        property_profile=None,
        memories=[],
        timeline=[
            "timeline-event-1",
        ],
        maintenance_records=[
            "existing-maintenance",
        ],
    )
    

    state: HomeAssistantState = {
        "subject_id": "household-1",
        "home_id": "home-1",
        "conversation_id": "conversation-1",
        "message": "I keep seeing mice in the kitchen.",
        "understanding": InteractionUnderstanding(
            explicit_intents=[
                "reported_active_problem",
            ],
        ),
        "context": context,
    }

    await nodes["intelligence"](state)

    assert len(
        maintenance_intelligence.calls
    ) == 1

    call = maintenance_intelligence.calls[0]

    assert call["maintenance_records"] == [
        "existing-maintenance",
    ]

@pytest.mark.asyncio
async def test_assistant_builds_response_from_maintenance_recommendation():

    intelligence_graph = FakeIntelligenceGraph()

    maintenance_intelligence = (
        FakeMaintenanceIntelligence()
    )

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHios(),
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=(
            maintenance_intelligence
        ),
    )

    state: HomeAssistantState = {
        "subject_id": "household-1",
        "home_id": "home-1",
        "conversation_id": "conversation-1",
        "message": "I keep seeing mice in the kitchen.",
        "maintenance_recommendations": [
            MaintenanceRecommendation(
                subject_id="household-1",
                home_id="home-1",
                task="Pest inspection",
                maintenance_type="preventive",
                reason="Repeated pest-related concerns.",
            ),
        ],
    }

    result = await nodes["build_response"](state)

    response = result["response"]

    assert response.capability == "maintenance"

    assert "Pest inspection" in response.message

def test_home_assistant_graph_accepts_maintenance_intelligence():

    context_assembler = FakeContextAssembler()
    router = FakeRouter()
    hios = FakeHios()
    intelligence_graph = FakeIntelligenceGraph()
    maintenance_intelligence = FakeMaintenanceIntelligence()

    graph = build_home_assistant_graph(
        context_assembler=context_assembler,
        router=router,
        hios=hios,
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=maintenance_intelligence,
    )

    assert graph is not None

@pytest.mark.asyncio
async def test_assistant_intelligence_does_not_recommend_existing_maintenance():

    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.PLANNED,
    )

    intelligence_graph = FakeIntelligenceGraph()

    maintenance_intelligence = FakeMaintenanceIntelligence()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHios(),
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=maintenance_intelligence,
    )

    context = HomeContext(
        home=object(),
        information=object(),
        state=object(),
        property_profile=None,
        memories=[],
        timeline=["timeline-event"],
        maintenance_records=[existing],
    )

    state: HomeAssistantState = {
        "subject_id": "household-1",
        "home_id": "home-1",
        "conversation_id": "conversation-1",
        "message": "I keep seeing mice in the kitchen.",
        "understanding": InteractionUnderstanding(
            explicit_intents=[
                "reported_active_problem",
            ],
        ),
        "context": context,
    }

    result = await nodes["intelligence"](state)

    assert len(maintenance_intelligence.calls) == 1

    call = maintenance_intelligence.calls[0]

    assert call["maintenance_records"] == [
        existing,
    ]