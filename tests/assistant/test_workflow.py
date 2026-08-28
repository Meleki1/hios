import pytest

from hios.capabilities.assistant.graph.workflow import (
    build_home_assistant_graph,
)
from hios.capabilities.assistant.models.assistant_domain import (
    AssistantDomain,
)
from hios.capabilities.assistant.models.home_context import (
    HomeContext,
)
from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.models.home_state import (
    HomeState,
)
from hios.capabilities.home.models.home import (
    Home,
)

from hios.capabilities.pest_control.contract import (
    PestControlResult,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.capabilities.intelligence.graph.workflow import (
    build_intelligence_graph,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.models.signal import (
    Signal,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.assistant.router.default_interaction_router import (
    DefaultInteractionRouter,
)
from hios.capabilities.assistant.context.home_context_assembler import (
    HomeContextAssembler,
)
from hios.packs.pest_control.builder import create
from hios.capabilities.assistant.context.home_context_assembler import (
    HomeContextAssembler,
)
from hios.capabilities.assistant.graph.workflow import (
    build_home_assistant_graph,
)
from hios.capabilities.assistant.models.interaction_understanding import (
    InteractionUnderstanding,
)
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)


class FakeMaintenanceIntelligence:

    def __init__(self):
        self.calls = []

    async def analyze(self, **kwargs):
        self.calls.append(kwargs)

        return [
            MaintenanceRecommendation(
                subject_id="household-1",
                home_id="home-1",
                task="Pest inspection",
                maintenance_type="preventive",
                reason="Repeated pest-related concerns.",
                priority="normal",
            )
        ]

class WorkflowFakeHios:
    async def execute(self, request):
        return None

class FakeHomeRepository:

    async def get(
        self,
        home_id: str,
    ) -> Home | None:

        return Home(
            id=home_id,
            name="Test Home",
            home_type="house",
        )

class FakeHomeInformationRepository:

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeInformation | None:

        return HomeInformation(
            home_id=home_id,
            country="Nigeria",
            city="Lagos",
            address="123 Test Street",
        )


class FakeHomeStateRepository:

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeState | None:

        return HomeState(
            home_id=home_id,
        )

class FakeRiskAssessment:

    risks = []

class FakeRiskAssessmentService:

    async def assess(
        self,
        risk_types,
        property_characteristics=None,
        environmental_observations=None,
    ):

        return FakeRiskAssessment()

class FakeRiskSignalAdapter:

    def to_signals(
        self,
        assessment,
    ):

        return []

class FakeIntelligenceService:

    def __init__(self):
        self.called = False

    async def predict(
        self,
        subject_id,
        target,
        horizon_days,
        intent_score,
    ):

        self.called = True

        return Prediction(
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )

class ExplicitIntentSignalCollectionFake:

    async def collect(
        self,
        subject_id,
        property_profile=None,
        environmental_observation=None,
        explicit_intents=None,
        interactions=None,
        local_activities=None,
        platform_behaviours=None,
        radius_km=5.0,
        include_local_activity=True,
    ):

        signals = []

        for intent in explicit_intents or []:

            signals.append(
                Signal(
                    type=SignalType.EXPLICIT_INTENT,
                    source=SignalSource.HOME_ASSIST,
                    name="explicit_intent",
                    value=intent,
                    strength=1.0,
                    confidence=1.0,
                )
            )

        return signals

    async def score_signals(
        self,
        signals,
    ):

        return IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=1.0,
            signals=signals,
        )

    async def collect_local_activity_with_status(
        self,
        subject_id,
        property_profile,
        radius_km=5.0,
    ):
        return [], []

class FakeIntelligenceGraph:

    def __init__(self):
        self.state = None

    async def ainvoke(self, state):
        self.state = state

        return {
            "signals": [],
            "risk": None,
            "prediction": None,
        }

class FakeHIOS:

    async def execute(
        self,
        request,
    ) -> PestControlResult:

        self.request = request

        return PestControlResult(
            observation=None,
            assessment=None,
            goals=None,
            plans=None,
            decision=None,
            execution=None,
            outcome=None,
            reflection=None,
            learning=None,
        )


class FakeContextAssembler:

    async def assemble(
        self,
        *,
        home_id: str,
        subject_id: str,
        message: str,
    ) -> HomeContext:

        return HomeContext(
            home={"id": home_id},
            information={},
            state={},
            property_profile=None,
            memories=[],
            timeline=[],

        )


class FakeRouter:

    def route(
        self,
        message: str,
    ) -> AssistantDomain:

        return AssistantDomain.PEST_CONTROL


@pytest.mark.asyncio
async def test_home_assistant_workflow():

    intelligence_graph = FakeIntelligenceGraph()

    graph = build_home_assistant_graph(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
    )

    result = await graph.ainvoke(
        {
            "subject_id": "subject-123",
            "home_id": "home-123",
            "message": (
                "I found droppings in my kitchen."
            ),
        }
    )

    assert result["context"] is not None

    assert result["domain"] == (
        AssistantDomain.PEST_CONTROL
    )


@pytest.mark.asyncio
async def test_home_assistant_workflow():

    fake_hios = FakeHIOS()
    
    intelligence_graph = FakeIntelligenceGraph()

    graph = build_home_assistant_graph(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=fake_hios,
        intelligence_graph=intelligence_graph,
    )

    result = await graph.ainvoke(
        {
            "subject_id": "subject-123",
            "home_id": "home-123",
            "conversation_id": "conversation-123",
            "message": (
                "I found droppings in my kitchen."
            ),
        }
    )

    # Context was assembled.
    assert result["context"] is not None

    # Interaction was routed.
    assert result["domain"] == (
        AssistantDomain.PEST_CONTROL
    )

    # HIOS received the correct request.
    assert fake_hios.request.subject_id == (
        "subject-123"
    )

    assert fake_hios.request.home_id == (
        "home-123"
    )

    assert fake_hios.request.message == (
        "I found droppings in my kitchen."
    )

    # HIA produced its final response.
    response = result["response"]

    assert isinstance(
        response,
        HomeAssistantResponse,
    )

    assert response.conversation_id == (
        "conversation-123"
    )

    assert response.capability == (
        "pest_control"
    )

    assert response.message == (
        "I've reviewed the information "
        "you provided about the pest issue."
    )




@pytest.mark.asyncio
async def test_hia_workflow_builds_interaction_understanding():

    intelligence_graph = FakeIntelligenceGraph()
    
    graph = build_home_assistant_graph(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "conversation_id": "conversation-123",
        "message": (
            "I need someone to treat these ants."
        ),
    }

    result = await graph.ainvoke(
        state,
    )

    understanding = result["understanding"]

    assert (
        "requested_treatment"
        in understanding.explicit_intents
    )




@pytest.mark.asyncio
async def test_hia_executes_real_intelligence_graph():

    context_assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(),
        information_repository=(
            FakeHomeInformationRepository()
        ),
        state_repository=(
            FakeHomeStateRepository()
        ),
    )

    pest_control_hios = FakeHIOS()
    #pest_control_hios = create()

    intelligence_graph = build_intelligence_graph(
        signal_collection_service=(
            ExplicitIntentSignalCollectionFake()
        ), 
        intelligence_service=(
            FakeIntelligenceService()
        ),
        risk_assessment_service=(
            FakeRiskAssessmentService()
        ),
        risk_signal_adapter=(
            FakeRiskSignalAdapter()
        ),
    )

    graph = build_home_assistant_graph(
        context_assembler=context_assembler,
        router=DefaultInteractionRouter(),
        hios=pest_control_hios,
        intelligence_graph=intelligence_graph,
    )

    result = await graph.ainvoke(
        {
            "subject_id": "subject-123",
            "home_id": "home-123",
            "conversation_id": "conversation-123",
            "message": (
                "I need someone to treat these ants."
            ),
        }
    )

    understanding = result["understanding"]

    assert (
        "requested_treatment"
        in understanding.explicit_intents
    )

    assert result["intent_score"] is not None

    assert (
        result["intent_score"].level
        == IntentLevel.HIGH
    )

    assert result["prediction"] is not None

@pytest.mark.asyncio
async def test_home_assistant_workflow_uses_maintenance_intelligence():

    context_assembler = FakeContextAssembler()

    maintenance_intelligence = (
        FakeMaintenanceIntelligence()
    )

    graph = build_home_assistant_graph(
        context_assembler=context_assembler,
        router=FakeRouter(),
        hios=WorkflowFakeHios(),
        intelligence_graph=FakeIntelligenceGraph(),
        maintenance_intelligence=maintenance_intelligence,
    )

    result = await graph.ainvoke(
        {
            "subject_id": "household-1",
            "home_id": "home-1",
            "conversation_id": "conversation-1",
            "message": (
                "I keep seeing mice "
                "in the kitchen."
            ),
        }
    )

    assert result["response"] is not None

    assert (
        result["response"].capability
        == "maintenance"
    )

    assert (
        "Pest inspection"
        in result["response"].message
    )

@pytest.mark.asyncio
async def test_home_assistant_workflow_builds_maintenance_response():

    context_assembler = FakeContextAssembler()
    maintenance_intelligence = FakeMaintenanceIntelligence()

    graph = build_home_assistant_graph(
        context_assembler=context_assembler,
        router=FakeRouter(),
        hios=WorkflowFakeHios(),
        intelligence_graph=FakeIntelligenceGraph(),
        maintenance_intelligence=maintenance_intelligence,
    )

    result = await graph.ainvoke(
        {
            "subject_id": "household-1",
            "home_id": "home-1",
            "conversation_id": "conversation-1",
            "message": "I keep seeing mice in the kitchen.",
        }
    )

    response = result["response"]

    assert response.capability == "maintenance"

    assert "Pest inspection" in response.message

    assert response.metadata["task"] == "Pest inspection"

    assert (
        response.metadata["maintenance_type"]
        == "preventive"
    )