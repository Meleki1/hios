import pytest

from hios.capabilities.assistant.context.home_context_assembler import (
    HomeContextAssembler,
)
from hios.capabilities.property.models.property_profile import (
    PropertyProfile,
)

from hios.capabilities.home.models.home import Home
from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.models.home_state import (
    HomeState,
)
from hios.capabilities.memory.models.memory_entry import MemoryEntry
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceType,
    MaintenanceStatus,
)


class FakeMaintenanceRepository:
    def __init__(self, records):
        self.records = records

    async def get_by_home(self, home_id):
        return [
            record
            for record in self.records
            if record.home_id == home_id
        ]

class TimelineServiceFake:

    def __init__(self):
        self.entries = [
            TimelineEntry(
                subject_id="subject-123",
                event_type="conversation",
                event_name="message_received",
                state="observed",
                description="I found ants in my kitchen.",
                resource_id="conversation-1",
                resource_type="conversation",
            ),
            TimelineEntry(
                subject_id="subject-123",
                event_type="outcome",
                event_name="outcome_recorded",
                state="observed",
                description="Pest treatment was completed.",
                resource_id="outcome-1",
                resource_type="outcome",
            ),
        ]

    async def get_by_subject(
        self,
        subject_id: str,
    ):

        return [
            entry
            for entry in self.entries
            if entry.subject_id == subject_id
        ]

class FakeTimelineService:

    def __init__(self, entries):
        self.entries = entries
        self.subject_id = None

    async def get_by_subject(
        self,
        subject_id: str,
    ):
        self.subject_id = subject_id
        return self.entries

class FakeMemoryService:

    def __init__(self, memories):
        self.memories = memories
        self.query = None

    async def recall(
        self,
        query: str,
    ):
        self.query = query
        return self.memories

class FakeHomeRepository:

    def __init__(self, home):
        self.home = home

    async def get(self, home_id):
        return self.home


class FakeHomeInformationRepository:

    def __init__(self, information):
        self.information = information

    async def get_by_home(self, home_id):
        return self.information


class FakeHomeStateRepository:

    def __init__(self, state):
        self.state = state

    async def get_by_home(self, home_id):
        return self.state


class FakeHomePropertyService:

    def __init__(self, reference):
        self.reference = reference
        self.home_id = None

    async def get_by_home(
        self,
        home_id: str,
    ):
        self.home_id = home_id
        return self.reference


class FakePropertyService:

    def __init__(self, property_profile):
        self.property_profile = property_profile
        self.uprn = None

    async def get_property(
        self,
        uprn: str,
    ):
        self.uprn = uprn
        return self.property_profile


@pytest.mark.asyncio
async def test_home_context_assembler_loads_home_context():

    home = Home(
        id="home-123",
        name="My Home",
        home_type="residential",
        description="Family home",
        status="active",
    )

    information = HomeInformation(
        home_id="home-123",
        country="United Kingdom",
        city="London",
        address="10 Example Road",
        postcode="SW1A 1AA",
    )

    state = HomeState(
        home_id="home-123",
        status="active",
    )

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(home),
        information_repository=(
            FakeHomeInformationRepository(
                information
            )
        ),
        state_repository=(
            FakeHomeStateRepository(state)
        ),
    )

    context = await assembler.assemble(
        "home-123",
        subject_id="subject-123",
    )

    assert context.home.id == "home-123"
    assert context.home.name == "My Home"

    assert context.information.city == "London"
    assert context.information.postcode == "SW1A 1AA"

    assert context.state.home_id == "home-123"
    assert context.state.status == "active"

    assert context.property_profile is None


@pytest.mark.asyncio
async def test_home_context_assembler_rejects_unknown_home():

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(None),
        information_repository=(
            FakeHomeInformationRepository(None)
        ),
        state_repository=(
            FakeHomeStateRepository(None)
        ),
    )

    with pytest.raises(
        ValueError,
        match="Home not found",
    ):
        await assembler.assemble(
            "unknown-home",
            subject_id="subject-123",
        )


@pytest.mark.asyncio
async def test_home_context_assembler_recalls_relevant_memories():

    home = Home(
        id="home-123",
        name="My Home",
        home_type="residential",
        description="Family home",
        status="active",
    )

    information = HomeInformation(
        home_id="home-123",
        country="United Kingdom",
        city="London",
        address="10 Example Road",
        postcode="SW1A 1AA",
    )

    state = HomeState(
        home_id="home-123",
        status="active",
    )

    memory = MemoryEntry(
        category="home_preference",
        description="The homeowner prefers preventative maintenance.",
        confidence=0.9,
    )

    memory_service = FakeMemoryService(
        [memory],
    )

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(home),
        information_repository=(
            FakeHomeInformationRepository(
                information
            )
        ),
        state_repository=(
            FakeHomeStateRepository(state)
        ),
        memory_service=memory_service,
    )

    context = await assembler.assemble(
        home_id="home-123",
        subject_id="subject-123",
        message="How can I prevent problems with my home?",
    )

    assert len(context.memories) == 1

    assert (
        context.memories[0].description
        == "The homeowner prefers preventative maintenance."
    )

    assert memory_service.query == (
        "How can I prevent problems with my home?"
    )


@pytest.mark.asyncio
async def test_home_context_assembler_does_not_recall_memory_without_message():

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

    memory_service = FakeMemoryService(
        [],
    )

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(home),
        information_repository=(
            FakeHomeInformationRepository(
                information
            )
        ),
        state_repository=(
            FakeHomeStateRepository(state)
        ),
        memory_service=memory_service,
    )

    context = await assembler.assemble(
        home_id="home-123",
        subject_id="subject-123",
    )

    assert context.memories == []
    assert memory_service.query is None


@pytest.mark.asyncio
async def test_home_context_assembler_loads_timeline():

    home = Home(
        id="home-123",
        name="My Home",
        home_type="residential",
        description="Family home",
        status="active",
    )

    information = HomeInformation(
        home_id="home-123",
        country="United Kingdom",
        city="London",
        address="10 Example Road",
        postcode="SW1A 1AA",
    )

    state = HomeState(
        home_id="home-123",
        status="active",
    )

    entry = TimelineEntry(
        subject_id="subject-123",
        event_type="HOME",
        event_name="HomeCreated",
        state="SUCCESS",
        description="Home was created.",
        resource_id="home-123",
        resource_type="home",
    )

    timeline_service = FakeTimelineService(
        [entry],
    )

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(home),
        information_repository=(
            FakeHomeInformationRepository(
                information
            )
        ),
        state_repository=(
            FakeHomeStateRepository(state)
        ),
        timeline_service=timeline_service,
    )

    context = await assembler.assemble(
        home_id="home-123",
        subject_id="subject-123",
    )

    assert len(context.timeline) == 1

    assert (
        context.timeline[0].event_name
        == "HomeCreated"
    )

    assert (
        context.timeline[0].subject_id
        == "subject-123"
    )

    assert (
        timeline_service.subject_id
        == "subject-123"
    )


@pytest.mark.asyncio
async def test_home_context_assembler_allows_empty_timeline():

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

    timeline_service = FakeTimelineService([])

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(home),
        information_repository=(
            FakeHomeInformationRepository(
                information
            )
        ),
        state_repository=(
            FakeHomeStateRepository(state)
        ),
        timeline_service=timeline_service,
    )

    context = await assembler.assemble(
        home_id="home-123",
        subject_id="subject-123",
    )

    assert context.timeline == []

@pytest.mark.asyncio
async def test_home_context_assembler_loads_property_from_home_association():

    home = Home(
        id="home-123",
        name="My Home",
        home_type="residential",
        description="Family home",
        status="active",
    )

    information = HomeInformation(
        home_id="home-123",
        country="United Kingdom",
        city="London",
        address="10 Example Road",
        postcode="SW1A 1AA",
    )

    state = HomeState(
        home_id="home-123",
        status="active",
    )

    reference = HomePropertyReference(
        home_id="home-123",
        uprn="100023456789",
    )

    property_profile = PropertyProfile(
        uprn="100023456789",
        address="10 Example Road",
        postcode="SW1A 1AA",
        property_type="house",
        bedrooms=3,
        bathrooms=2,
    )

    home_property_service = (
        FakeHomePropertyService(reference)
    )

    property_service = FakePropertyService(
        property_profile,
    )

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(home),
        information_repository=(
            FakeHomeInformationRepository(
                information
            )
        ),
        state_repository=(
            FakeHomeStateRepository(state)
        ),
        home_property_service=(
            home_property_service
        ),
        property_service=property_service,
    )

    context = await assembler.assemble(
        home_id="home-123",
        subject_id="subject-123",
    )

    assert context.property_profile is not None

    assert (
        context.property_profile.uprn
        == "100023456789"
    )

    assert (
        context.property_profile.bedrooms
        == 3
    )

    assert (
        home_property_service.home_id
        == "home-123"
    )

    assert (
        property_service.uprn
        == "100023456789"
    )

@pytest.mark.asyncio
async def test_home_context_assembler_allows_home_without_property_association():

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

    home_property_service = (
        FakeHomePropertyService(None)
    )

    property_service = FakePropertyService(
        None,
    )

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(home),
        information_repository=(
            FakeHomeInformationRepository(
                information
            )
        ),
        state_repository=(
            FakeHomeStateRepository(state)
        ),
        home_property_service=(
            home_property_service
        ),
        property_service=property_service,
    )

    context = await assembler.assemble(
        home_id="home-123",
        subject_id="subject-123",
    )

    assert context.property_profile is None
    assert (
        property_service.uprn is None
    )

@pytest.mark.asyncio
async def test_home_context_assembler_allows_missing_property_profile():

    home = Home(
        id="home-123",
        name="My Home",
        home_type="residential",
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

    reference = HomePropertyReference(
        home_id="home-123",
        uprn="100023456789",
    )

    home_property_service = (
        FakeHomePropertyService(reference)
    )

    property_service = FakePropertyService(
        None,
    )

    assembler = HomeContextAssembler(
        home_repository=FakeHomeRepository(home),
        information_repository=(
            FakeHomeInformationRepository(
                information
            )
        ),
        state_repository=(
            FakeHomeStateRepository(state)
        ),
        home_property_service=(
            home_property_service
        ),
        property_service=property_service,
    )

    context = await assembler.assemble(
        home_id="home-123",
        subject_id="subject-123",
    )

    assert context.property_profile is None

    assert (
        property_service.uprn
        == "100023456789"
    )

@pytest.mark.asyncio
async def test_home_context_includes_subject_timeline():

    timeline_service = TimelineServiceFake()

    home = Home(
        id="home-123",
        name="Test Home",
        home_type="house",
    )

    information = HomeInformation(
        home_id="home-123",
        country="Nigeria",
        city="Lagos",
        address="123 Test Street",
    )

    state = HomeState(
        home_id="home-123",
        status="active",
    )

    home_repository = FakeHomeRepository(
        home=home,
    )

    information_repository = (
        FakeHomeInformationRepository(
            information=information,
        )
    )

    state_repository = (
        FakeHomeStateRepository(
            state=state,
        )
    )

    assembler = HomeContextAssembler(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
        timeline_service=timeline_service,
    )

    context = await assembler.assemble(
        home_id="home-123",
        subject_id="subject-123",
        message="I found ants again.",
    )

    assert len(context.timeline) == 2

    assert (
        context.timeline[0].event_name
        == "message_received"
    )

    assert (
        context.timeline[1].event_name
        == "outcome_recorded"
    )

    assert (
        context.timeline[0].description
        == "I found ants in my kitchen."
    )


class HomeRepositoryFake:
    async def get(self, home_id):
        return object()


class HomeInformationRepositoryFake:
    async def get_by_home(self, home_id):
        return object()


class HomeStateRepositoryFake:
    async def get_by_home(self, home_id):
        return object()


class MaintenanceRepositoryFake:
    def __init__(self, records):
        self.records = records

    async def get_by_home(self, home_id):
        return [
            record
            for record in self.records
            if record.home_id == home_id
        ]

@pytest.mark.asyncio
async def test_home_context_assembler_includes_maintenance_records():

    existing_maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.PLANNED,
    )

    maintenance_repository = MaintenanceRepositoryFake(
        records=[
            existing_maintenance,
        ],
    )

    assembler = HomeContextAssembler(
        home_repository=HomeRepositoryFake(),
        information_repository=(
            HomeInformationRepositoryFake()
        ),
        state_repository=HomeStateRepositoryFake(),
        maintenance_repository=maintenance_repository,
    )

    context = await assembler.assemble(
        home_id="home-1",
        subject_id="household-1",
        message="I keep seeing mice.",
    )

    assert context.maintenance_records == [
        existing_maintenance,
    ]

@pytest.mark.asyncio
async def test_home_context_assembler_includes_persisted_maintenance():

    maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.PLANNED,
    )

    maintenance_repository = MaintenanceRepositoryFake(
        records=[maintenance],
    )

    assembler = HomeContextAssembler(
        home_repository=HomeRepositoryFake(),
        information_repository=HomeInformationRepositoryFake(),
        state_repository=HomeStateRepositoryFake(),
        maintenance_repository=maintenance_repository,
    )

    context = await assembler.assemble(
        subject_id="household-1",
        home_id="home-1",
        message="When is my pest inspection?",
    )

    assert context.maintenance_records == [
        maintenance,
    ]

