import pytest
from hios.capabilities.home.services.home_service import (
    HomeService,
)

from hios.capabilities.home.events.home_created import (
    HomeCreatedEvent,
)
from hios.capabilities.home.schemas.home_creation import (
    CreateHomeRequest,
    HomeInformationInput,
)
from hios.capabilities.timeline.listeners.timeline_listener import TimelineListener

from hios.core.events.base_event import BaseEvent

from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.repositories.home_information_repository import (
    HomeInformationRepository,
)
from hios.core.events.event_publisher import EventPublisher

from hios.capabilities.home.models.home import Home
from hios.capabilities.home.models.home_information import (
    HomeInformation,
)
from hios.capabilities.home.models.home_state import (
    HomeState,
)

from hios.capabilities.home.repositories.home_repository import (
    HomeRepository,
)
from hios.capabilities.home.repositories.home_information_repository import (
    HomeInformationRepository,
)
from hios.capabilities.home.repositories.home_state_repository import (
    HomeStateRepository,
)

from hios.capabilities.home.schemas.home_creation import (
    CreateHomeRequest,
    HomeInformationInput,
)

from hios.capabilities.home.services.home_service import (
    HomeService,
)

from hios.capabilities.home.schemas.home_creation import (
    CreateHomeRequest,
    HomeInformationInput,
)
from hios.capabilities.home.events.home_created import (
    HomeCreatedEvent,
)

class FakeHomeStateRepository(
    HomeStateRepository,
):

    def __init__(self):
        self.items = {}

    async def save(
        self,
        state: HomeState,
    ) -> HomeState:

        self.items[state.home_id] = state

        return state

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeState | None:

        return self.items.get(home_id)



class FakeHomeRepository(HomeRepository):

    def __init__(self):
        self.saved = None

    async def save(
        self,
        home: Home,
    ) -> Home:

        self.saved = home

        return home

    async def get(
        self,
        home_id: str,
    ) -> Home | None:

        if self.saved is None:
            return None

        if self.saved.id == home_id:
            return self.saved

        return None

class FakeHomeInformationRepository(
    HomeInformationRepository,
):

    def __init__(self):
        self.saved = None

    async def save(
        self,
        information: HomeInformation,
    ) -> HomeInformation:

        self.saved = information

        return information

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeInformation | None:

        if self.saved is None:
            return None

        if self.saved.home_id == home_id:
            return self.saved

        return None

class FakeTimelineService:

    def __init__(self):
        self.recorded = []

    async def record(self, entry):

        self.recorded.append(entry)

        return entry

@pytest.mark.asyncio
async def test_home_created_event_is_recorded_in_timeline():

    timeline_service = FakeTimelineService()

    listener = TimelineListener(
        service=timeline_service,
    )

    event = HomeCreatedEvent(
        home_id="home-123",
        subject_id="subject-1",
    )

    await listener.listen(event)

    assert len(
        timeline_service.recorded
    ) == 1

    entry = (
        timeline_service.recorded[0]
    )

    assert entry.subject_id == (
        "subject-1"
    )

    assert entry.resource_id == (
        "home-123"
    )

    assert entry.resource_type == (
        "home"
    )

    assert entry.event_type == (
        "home"
    )

    assert entry.event_name == (
        "home_created"
    )

    assert entry.state == (
        "created"
    )

    assert entry.description == (
        "Home created successfully"
    )

    assert entry.created_at is not None

@pytest.mark.asyncio
async def test_home_creation_records_timeline_event():

    home_repository = FakeHomeRepository()
    information_repository = (
        FakeHomeInformationRepository()
    )
    state_repository = FakeHomeStateRepository()

    timeline_service = FakeTimelineService()

    timeline_listener = TimelineListener(
        service=timeline_service,
    )

    publisher = EventPublisher()

    publisher.subscribe(
        timeline_listener,
    )

    home_service = HomeService(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
        event_publisher=publisher,
    )

    request = CreateHomeRequest(
        name="My London Home",
        home_type="residential",
        description="Family home",
        information=HomeInformationInput(
            country="United Kingdom",
            city="London",
            address="10 Example Road",
            postcode="SW1A 1AA",
        ),
    )

    home = await home_service.create(
        subject_id="subject-1",
        request=request,
    )

    assert len(timeline_service.recorded) == 1

    entry = timeline_service.recorded[0]

    assert entry.subject_id == "subject-1"
    assert entry.resource_id == home.id
    assert entry.resource_type == "home"

    assert entry.event_type == "home"
    assert entry.event_name == "home_created"
    assert entry.state == "created"
    assert entry.description == (
        "Home created successfully"
    )