import pytest

from hios.capabilities.assistant.context.home_context_assembler import (
    HomeContextAssembler,
)
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.assistant.graph.nodes import create_nodes
from hios.capabilities.assistant.response.assistant_action_response_builder import (
    AssistantActionResponseBuilder,
)
from hios.capabilities.timeline.services.timeline_service import TimelineService
from tests.assistant.test_maintenance_timeline_integration import FakeTimelineRepository
from tests.assistant.test_home_context_assembler import FakeHomeInformationRepository, FakeHomeStateRepository
from tests.assistant.test_nodes import FakeIntelligenceGraph
from hios.capabilities.home.models.home import Home
from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.models.home_state import (
    HomeState,
)
from hios.capabilities.timeline.repositories.postgres_timeline_repository import (
    PostgresTimelineRepository,
)
from hios.db.session import SessionLocal
from uuid import uuid4


class FakeMaintenanceIntelligence:
    def __init__(self):
        self.received_timeline = None

    async def analyze(
        self,
        *,
        subject_id,
        home_id,
        timeline,
        maintenance_records,
        explicit_intents,
    ):
        self.received_timeline = timeline

        return []

class FakeHomeContext:
    def __init__(
        self,
        *,
        timeline=None,
        maintenance_records=None,
        memories=None,
        property_profile=None,
    ):
        self.timeline = timeline or []
        self.maintenance_records = maintenance_records or []
        self.memories = memories or []
        self.property_profile = property_profile


class CapturingIntelligenceGraph:

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
        self.entries = []

    async def record(self, entry):
        self.entries.append(entry)
        return entry

    async def get_by_subject(self, subject_id):
        return [
            entry
            for entry in self.entries
            if entry.subject_id == subject_id
        ]


@pytest.mark.asyncio
async def test_previous_outreach_event_is_available_to_later_context():

    timeline_service = FakeTimelineService()

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(),
        information_repository=FakeInformationRepository(),
        state_repository=FakeStateRepository(),
        timeline_service=timeline_service,
    )

    # Simulate the event produced by the first interaction.
    previous_event = TimelineEntry(
        subject_id="subject-1",
        event_type="outreach",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Maintenance alert sent: Inspect roof",
        resource_id="Inspect roof",
        resource_type="maintenance",
    )

    await timeline_service.record(
        previous_event,
    )

    # Simulate a later assistant interaction.
    context = await assembler.assemble(
        home_id="home-1",
        subject_id="subject-1",
        message="What happened with my roof?",
    )

    assert len(context.timeline) == 1

    entry = context.timeline[0]

    assert entry.event_type == "outreach"
    assert entry.event_name == "maintenance_alert_sent"
    assert entry.state == "sent"
    assert entry.resource_id == "Inspect roof"


@pytest.mark.asyncio
async def test_timeline_reaches_intelligence():

    intelligence_graph = CapturingIntelligenceGraph()

    timeline_entry = TimelineEntry(
        subject_id="subject-1",
        event_type="outreach",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Maintenance alert sent: Inspect roof",
        resource_id="Inspect roof",
        resource_type="maintenance",
    )

    class FakeContext:
        timeline = [timeline_entry]
        maintenance_records = []

    nodes = create_nodes(
        context_assembler=None,
        router=None,
        hios=None,
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=None,
        outreach=None,
        event_publisher=None,
        action_response_builder=AssistantActionResponseBuilder(),
    )

    state = {
        "subject_id": "subject-1",
        "home_id": "home-1",
        "message": "What happened with my roof?",
        "context": FakeContext(),
        "understanding": None,
    }

    await nodes["intelligence"](state)

    assert intelligence_graph.received_state is not None

    assert intelligence_graph.received_state["subject_id"] == "subject-1"

    assert len(
        intelligence_graph.received_state["timeline"]
    ) == 1

    assert (
        intelligence_graph.received_state["timeline"][0]
        == timeline_entry
    )

@pytest.mark.asyncio
async def test_timeline_context_returns_subject_history():

    repository = FakeTimelineRepository()

    service = TimelineService(
        repository=repository,
    )

    first = TimelineEntry(
        subject_id="home-1",
        event_type="maintenance",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Roof maintenance alert sent.",
    )

    second = TimelineEntry(
        subject_id="home-1",
        event_type="prediction",
        event_name="prediction_created",
        state="created",
        description="Roof failure prediction created.",
    )

    await repository.save(first)
    await repository.save(second)

    history = await service.get_by_subject(
        "home-1",
    )

    assert history == [
        first,
        second,
    ]

@pytest.mark.asyncio
async def test_assistant_receives_timeline_history():

    home = Home(
        id="home-123",
        name="My Home",
        home_type="residential",
        description=None,
        status="active",
    )

    information = HomeInformation(
        home_id="home-123",
        country="United Kingdom",
        city="London",
        address="10 Example Road",
    )

    state = HomeState(
        home_id="home-123",
        status="active",
    )


    timeline_repository = FakeTimelineRepository()

    timeline_service = TimelineService(
        repository=timeline_repository,
    )

    historical_entry = TimelineEntry(
        subject_id="home-1",
        event_type="maintenance",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Roof maintenance alert sent.",
        resource_id="Inspect roof",
        resource_type="maintenance",
    )

    await timeline_service.record(
        historical_entry,
    )

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(),
        information_repository=FakeHomeInformationRepository(information),
        state_repository=FakeHomeStateRepository(state),
        timeline_service=timeline_service,
    )


    context = await assembler.assemble(
        home_id="home-1",
        subject_id="home-1",
        message="What has happened with my roof maintenance?",
    )

    assert len(context.timeline) == 1
    assert context.timeline[0] == historical_entry
    assert context.timeline[0].event_name == (
        "maintenance_alert_sent"
    )

@pytest.mark.asyncio
async def test_timeline_reaches_intelligence_graph():

    intelligence_graph = FakeIntelligenceGraph()

    historical_entry = TimelineEntry(
        subject_id="home-1",
        event_type="maintenance",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Roof maintenance alert sent.",
        resource_id="Inspect roof",
        resource_type="maintenance",
    )

    context = FakeHomeContext(
        timeline=[historical_entry],
    )

    state = {
        "subject_id": "home-1",
        "home_id": "home-1",
        "context": context,
    }

    node = create_nodes(
        context_assembler=None,
        router=None,
        hios=None,
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=None,
        outreach=None,
        action_response_builder=AssistantActionResponseBuilder(),
    )

    await node["intelligence"](state)

    assert intelligence_graph.received_state["timeline"] == [
        historical_entry
    ]

@pytest.mark.asyncio
async def test_timeline_reaches_maintenance_intelligence():

    intelligence_graph = FakeIntelligenceGraph()

    maintenance_intelligence = FakeMaintenanceIntelligence()

    historical_entry = TimelineEntry(
        subject_id="home-1",
        event_type="maintenance",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Roof maintenance alert sent.",
        resource_id="Inspect roof",
        resource_type="maintenance",
    )

    context = FakeHomeContext(
        timeline=[historical_entry],
    )

    state = {
        "subject_id": "home-1",
        "home_id": "home-1",
        "context": context,
    }

    nodes = create_nodes(
        context_assembler=None,
        router=None,
        hios=None,
        intelligence_graph=intelligence_graph,
        maintenance_intelligence=maintenance_intelligence,
        outreach=None,
        action_response_builder=AssistantActionResponseBuilder(),
    )

    await nodes["intelligence"](state)

    assert maintenance_intelligence.received_timeline == [
        historical_entry
    ]

@pytest.mark.asyncio
async def test_persisted_timeline_reaches_intelligence_graph():

    subject_id = f"integration-home-{uuid4()}"   

    entry = TimelineEntry(
        subject_id=subject_id,
        event_type="maintenance",
        event_name="maintenance_alert_sent",
        state="sent",
        description="Roof maintenance alert sent.",
        resource_id="maintenance-1",
        resource_type="maintenance",
    )

    async with SessionLocal() as session:

        

        timeline_repository = (
            PostgresTimelineRepository(
                session=session,
            )
        )

        timeline_service = TimelineService(
            repository=timeline_repository,
        )

        information = HomeInformation(
            home_id=subject_id,
            country="United Kingdom",
            city="London",
            address="10 Example Road",
        )

        await timeline_service.record(entry)

        assembler = HomeContextAssembler(
            home_repository=FakeHomeRepository(),
            information_repository=FakeHomeInformationRepository(
                information=information
            ),
            state_repository=FakeHomeStateRepository(
                state=HomeState(
                    home_id="integration-home-1",
                    status="active",
                ),
            ),
            timeline_service=timeline_service,
        )

        intelligence_graph = FakeIntelligenceGraph()

        nodes = create_nodes(
            context_assembler=assembler,
            router=None,
            hios=None,
            intelligence_graph=intelligence_graph,
            maintenance_intelligence=None,
            outreach=None,
            action_response_builder=AssistantActionResponseBuilder(),
        )

        state = {
            "home_id": subject_id,
            "subject_id": subject_id,
            "message": "What maintenance should I be aware of?",
        }

        context_result = await nodes["assemble_context"](state)

        state.update(context_result)

        await nodes["intelligence"](state)

    assert intelligence_graph.received_state is not None

    received = intelligence_graph.received_state["timeline"]

    assert len(received) == 1

    received_entry = received[0]

    print("ORIGINAL:", repr(entry))
    print("RECEIVED:", repr(received_entry))
    print("ORIGINAL CREATED:", repr(entry.created_at))
    print("RECEIVED CREATED:", repr(received_entry.created_at))

    assert received_entry.id == entry.id
    assert received_entry.subject_id == entry.subject_id
    assert received_entry.event_type == entry.event_type
    assert received_entry.event_name == entry.event_name
    assert received_entry.state == entry.state
    assert received_entry.description == entry.description
    assert received_entry.resource_id == entry.resource_id
    assert received_entry.resource_type == entry.resource_type