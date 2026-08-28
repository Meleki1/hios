import pytest
from hios.capabilities.assistant.graph.nodes import create_nodes
from hios.capabilities.assistant.graph.state import HomeAssistantState
from hios.capabilities.assistant.models.assistant_domain import (
    AssistantDomain,
)
from hios.capabilities.assistant.models.home_context import (
    HomeContext,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.capabilities.pest_control.contract import (
    PestControlResult,
)
from hios.capabilities.assistant.models.interaction_understanding import (
    InteractionUnderstanding,
)
from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.intent_score import IntentScore
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.intelligence.models.signal import Signal, SignalSource, SignalType
from hios.capabilities.execution.models.action import Action, ActionType
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.planning.models.task import Task
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.assistant.response.assistant_action_response_builder import AssistantActionResponseBuilder
from hios.capabilities.image_diagnosis.models.image_diagnosis import ImageDiagnosis

class FakeResponseGenerationService:

    def __init__(
        self,
        response: str = "This is a fake assistant response.",
    ):
        self.response = response
        self.received_state = None

    async def generate(
        self,
        *,
        state,
    ) -> str:
        self.received_state = state
        return self.response

class FakeInteractionUnderstandingService:

    async def understand(self, *, state):
        return InteractionUnderstanding(
            explicit_intents=[
                "reported_active_problem",
            ],
        )

class FakeImageDiagnosisService:

    def __init__(self, diagnosis):
        self.diagnosis = diagnosis
        self.calls = []

    async def diagnose(self, *, image):
        self.calls.append(image)
        return self.diagnosis

class FakeInteractionRouter:

    def route(self, message: str):
        return AssistantDomain.PEST_CONTROL

class FakeHomeContextAssembler:

    async def assemble(
        self,
        *,
        home_id: str,
        subject_id: str,
        message: str,
    ):
        return {
            "home_id": home_id,
            "subject_id": subject_id,
            "message": message,
        }

class FakeIntelligenceService:

    def __init__(self):
        self.called = False
        self.received = None

    async def predict(
        self,
        subject_id,
        target,
        horizon_days,
        intent_score,
    ):

        self.called = True

        self.received = {
            "subject_id": subject_id,
            "target": target,
            "horizon_days": horizon_days,
            "intent_score": intent_score,
        }

        return Prediction(
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )

class ExplicitIntentSignalCollectionFake:

    def __init__(self):
        self.received = None

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

        self.received = {
            "subject_id": subject_id,
            "explicit_intents": explicit_intents,
        }

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
        self.received_state = None

    async def ainvoke(self, state):
        self.received_state = state

        return {
            "signals": [],
            "risk": None,
            "intent_score": None,
            "prediction": None,
        }

class FakePestControl:

    async def execute(self, request):

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
            recommendations=[],
        )

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

class FakeInteractionUnderstandingService:

    async def understand(self, *, state):
        return InteractionUnderstanding(
            explicit_intents=[
                "reported_active_problem",
            ],
        )

class FakeRouter:

    def route(
        self,
        message: str,
    ) -> AssistantDomain:

        return AssistantDomain.PEST_CONTROL

class FakeAssistantLLM:

    async def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        return "fake response"


@pytest.mark.asyncio
async def test_assemble_context_node():

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": (
            "I found droppings in my kitchen."
        ),
    }

    result = await nodes["assemble_context"](
        state,
    )

    assert "context" in result

    context = result["context"]

    assert isinstance(
        context,
        HomeContext,
    )

    assert context.home["id"] == "home-123"


@pytest.mark.asyncio
async def test_route_interaction_node():

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": (
            "I found droppings in my kitchen."
        ),
    }

    result = await nodes["route_interaction"](
        state,
    )

    assert result["domain"] == (
        AssistantDomain.PEST_CONTROL
    )


@pytest.mark.asyncio
async def test_dispatch_domain_calls_hios_for_pest_control():

    fake_hios = FakeHIOS()

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=fake_hios,
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": (
            "I found droppings in my kitchen."
        ),
        "domain": AssistantDomain.PEST_CONTROL,
    }

    result = await nodes["dispatch_domain"](
        state,
    )

    assert fake_hios.request.subject_id == (
        "subject-123"
    )

    assert fake_hios.request.home_id == (
        "home-123"
    )

    assert fake_hios.request.message == (
        "I found droppings in my kitchen."
    )

    assert result == {
        "decision": None,
        "plan": None,
        "execution": None,
        "outcome": None,
        "reflection": None,
        "learning": None,
    }

@pytest.mark.asyncio
async def test_dispatch_domain_ignores_non_pest_control():

    fake_hios = FakeHIOS()

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": "Tell me about my home.",
        "domain": AssistantDomain.HOME,
    }

    result = await nodes["dispatch_domain"](
        state,
    )

    assert not hasattr(
        fake_hios,
        "request",
    )

    assert result == {}


@pytest.mark.asyncio
async def test_build_response_for_pest_control():

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "conversation_id": "conversation-123",
        "message": (
            "I found droppings in my kitchen."
        ),
        "domain": AssistantDomain.PEST_CONTROL,
    }

    result = await nodes["build_response"](
        state,
    )

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

    assert result["response"].message == (
        "This is a fake assistant response."
    )

@pytest.mark.asyncio
async def test_build_response_for_unsupported_domain():

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": "Something unsupported.",
        "domain": AssistantDomain.UNSUPPORTED,
    }

    result = await nodes["build_response"](
        state,
    )

    response = result["response"]

    assert isinstance(
        response,
        HomeAssistantResponse,
    )

    assert result["response"].capability == "unsupported"


"""@pytest.mark.asyncio
async def test_understand_interaction_detects_requested_treatment():

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": (
            "I need someone to treat these ants."
        ),
    }

    result = await nodes["understand_interaction"](
        state,
    )

    understanding = result["understanding"]

    assert (
        "requested_treatment"
        in understanding.explicit_intents
    )

@pytest.mark.asyncio
async def test_understand_interaction_detects_price_request():

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": (
            "How much would treatment cost?"
        ),
    }

    result = await nodes["understand_interaction"](
        state,
    )

    understanding = result["understanding"]

    assert (
        "asked_for_price"
        in understanding.explicit_intents
    )
"""

"""@pytest.mark.asyncio
async def test_understand_interaction_returns_empty_intents_when_none_are_explicit():

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": "Hello, how are you?",
    }

    result = await nodes["understand_interaction"](
        state,
    )

    assert (
        result["understanding"].explicit_intents
        == []
    )


@pytest.mark.asyncio
async def test_intelligence_node_receives_explicit_intents():

    intelligence_graph = FakeIntelligenceGraph()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    state = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": (
            "I need someone to treat these ants."
        ),
        "understanding": (
            InteractionUnderstanding(
                explicit_intents=[
                    "requested_treatment",
                ],
            )
        ),
    }

    await nodes["intelligence"](
        state,
    )

    assert (
        intelligence_graph.state[
            "subject_id"
        ]
        == "subject-123"
    )

    assert (
        intelligence_graph.state[
            "explicit_intents"
        ]
        == [
            "requested_treatment",
        ]
    )

async def test_intelligence_node_receives_explicit_intents():
    intelligence_graph = FakeIntelligenceGraph()

    understanding = InteractionUnderstanding(
        explicit_intents=[
            "asked_for_price",
        ],
    )

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=intelligence_graph,
        response_generation_service=(
            FakeResponseGenerationService()
        ),
        interaction_understanding_service=(
            FakeInteractionUnderstandingService(
                intents=["asked_for_price"],
            )
        ),
        action_response_builder=AssistantActionResponseBuilder(),
    )

    state = {
        "message": "How much does this cost?",
        "understanding": understanding,
    }

    await nodes["intelligence"](state)

    assert intelligence_graph.received_state is not None
    assert (
        intelligence_graph.received_state["understanding"]
        == understanding
    )"""

@pytest.mark.asyncio
async def test_build_response_returns_image_request_for_image_action():
    action = Action(
        action_type=ActionType.IMAGE_REQUEST,
        name="Request Image Evidence",
        description=(
            "Request an image of the affected area "
            "to gather visual evidence."
        ),
    )
    nodes = create_nodes(
        context_assembler=FakeHomeContextAssembler(),
        router=FakeInteractionRouter(),
        hios=FakeHIOS(),
        intelligence_graph=FakeIntelligenceGraph(),
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    build_response = nodes["build_response"]

    execution = Execution(
        decision=Decision(
            plan=Plan(
                goal_id="goal-1",
                name="Gather Visual Evidence",
                description="Gather visual evidence.",
                priority=GoalPriority.HIGH,
                tasks=[
                    Task(
                        name="Request Image Evidence",
                        description=(
                            "Request an image of the affected area "
                            "to gather visual evidence."
                        ),
                        required=True,
                    )
                ],
            ),
            rationale="Visual evidence is required.",
            score=1.0,
        ),
        actions=[action],
    )

    state = HomeAssistantState(
        subject_id="household-1",
        home_id="home-1",
        message="I think I have a pest problem.",
        conversation_id="conversation-1",
        domain=AssistantDomain.PEST_CONTROL,
        execution=execution,
    )

    result = await build_response(state)

    response = result["response"]

    assert response.capability == "image_diagnosis"
    assert response.conversation_id == "conversation-1"
    assert "photo" in response.message.lower()
    assert response.metadata["requires_user_input"] is True
    assert (
        response.metadata["action_type"]
        == ActionType.IMAGE_REQUEST.value
    )

"""@pytest.mark.asyncio
async def test_build_response_keeps_existing_pest_control_response():
    execution = Execution(
        decision=Decision(
            plan=Plan(
                goal_id="goal-1",
                name="Inspection",
                description="Inspect the property.",
                priority=GoalPriority.HIGH,
            ),
            rationale="Inspection is required.",
            score=1.0,
        ),
        actions=[],
    )

    nodes = create_nodes(
        context_assembler=FakeHomeContextAssembler(),
        router=FakeInteractionRouter(),
        hios=FakeHIOS(),
        intelligence_graph=FakeIntelligenceGraph(),
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    build_response = nodes["build_response"]

    state = HomeAssistantState(
        subject_id="household-1",
        home_id="home-1",
        message="There may be pests in my house.",
        conversation_id="conversation-1",
        domain=AssistantDomain.PEST_CONTROL,
        execution=execution,
    )

    result = await build_response(state)

    response = result["response"]

    assert response.capability == "pest_control"
    assert (
        response.message
        == "I've reviewed the information you provided about the pest issue."
    )"""

@pytest.mark.asyncio
async def test_diagnose_image_uses_image_diagnosis_service():

    diagnosis = ImageDiagnosis(
        findings=[],
        overall_confidence=0.8,
    )

    service = FakeImageDiagnosisService(
        diagnosis,
    )

    nodes = create_nodes(
        context_assembler=FakeHomeContextAssembler(),
        router=FakeInteractionRouter(),
        hios=FakeHIOS(),
        intelligence_graph=None,
        action_response_builder=AssistantActionResponseBuilder(),
        image_diagnosis_service=service,
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    image = b"fake-image"

    result = await nodes["diagnose_image"](
        {
            "image": image,
        }
    )

    assert result["image_diagnosis"] is diagnosis
    assert service.calls == [image]

@pytest.mark.asyncio
async def test_diagnose_image_does_nothing_without_image():

    diagnosis = ImageDiagnosis(
        findings=[],
        overall_confidence=0.0,
    )

    service = FakeImageDiagnosisService(
        diagnosis,
    )

    nodes = create_nodes(
        context_assembler=FakeHomeContextAssembler(),
        router=FakeInteractionRouter(),
        hios=FakeHIOS(),
        intelligence_graph=None,
        action_response_builder=AssistantActionResponseBuilder(),
        image_diagnosis_service=service,
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    result = await nodes["diagnose_image"]({})

    assert result == {}
    assert service.calls == []

@pytest.mark.asyncio
async def test_create_nodes_accepts_assistant_llm():
    llm = FakeAssistantLLM()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=FakeIntelligenceGraph(),
        maintenance_intelligence=None,
        action_response_builder=AssistantActionResponseBuilder(),
        response_generation_service=(
            FakeResponseGenerationService()
        ),

        interaction_understanding_service=(
            FakeInteractionUnderstandingService()
        ),
    )

    assert "understand_interaction" in nodes
    assert "build_response" in nodes

@pytest.mark.asyncio
async def test_understand_interaction_uses_understanding_service():
    service = FakeInteractionUnderstandingService()

    nodes = create_nodes(
        context_assembler=FakeContextAssembler(),
        router=FakeRouter(),
        hios=FakeHIOS(),
        intelligence_graph=FakeIntelligenceGraph(),
        response_generation_service=FakeResponseGenerationService(),
        interaction_understanding_service=service,
        action_response_builder=AssistantActionResponseBuilder(),

    )

    result = await nodes["understand_interaction"](
        {
            "message": "The kitchen situation has gotten worse.",
        }
    )

    assert result["understanding"].explicit_intents == [
        "reported_active_problem",
    ]