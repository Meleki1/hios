import pytest

from hios.capabilities.assistant.context.home_context_assembler import (
    HomeContextAssembler,
)
from hios.capabilities.assistant.graph.workflow import (
    build_home_assistant_graph,
)
from hios.capabilities.assistant.models.assistant_request import (
    HomeAssistantRequest,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.capabilities.assistant.router.default_interaction_router import (
    DefaultInteractionRouter,
)
from hios.capabilities.assistant.service import (
    AssistantService,
)

from hios.capabilities.home.models.home import (
    Home,
)
from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.models.home_state import (
    HomeState,
)

from hios.packs.pest_control.builder import create

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

@pytest.mark.asyncio
async def test_assistant_executes_real_hia_to_hios():

    context_assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(),
        information_repository=(
            FakeHomeInformationRepository()
        ),
        state_repository=(
            FakeHomeStateRepository()
        ),
    )

    pest_control_hios = create()
    intelligence_graph = FakeIntelligenceGraph()

    graph = build_home_assistant_graph(
        context_assembler=context_assembler,
        router=DefaultInteractionRouter(),
        hios=pest_control_hios,
        intelligence_graph=intelligence_graph,
    )

    assistant = AssistantService(
        graph=graph,
    )

    request = HomeAssistantRequest(
        subject_id="subject-123",
        home_id="home-123",
        conversation_id="conversation-123",
        message=(
            "I found droppings and "
            "hear scratching around my kitchen."
        ),
    )

    response = await assistant.execute(
        request,
    )

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

    assert response.message