import pytest

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

class FakeEventPublisher:

    def __init__(self):
        self.events = []

    async def publish(self, event):
        self.events.append(event)

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


class FakeHomeStateRepository(
    HomeStateRepository,
):

    def __init__(self):
        self.saved = None

    async def save(
        self,
        state: HomeState,
    ) -> HomeState:

        self.saved = state

        return state

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeState | None:

        if self.saved is None:
            return None

        if self.saved.home_id == home_id:
            return self.saved

        return None

    
@pytest.mark.asyncio
async def test_home_service_creates_home_and_related_records():

    home_repository = FakeHomeRepository()

    information_repository = (
        FakeHomeInformationRepository()
    )

    state_repository = FakeHomeStateRepository()

    service = HomeService(
        home_repository=home_repository,
        information_repository=(
            information_repository
        ),
        state_repository=state_repository,
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

    result = await service.create(
        subject_id="subject-1",
        request=request,
    )

    assert result is home_repository.saved

    assert result.name == (
        "My London Home"
    )

    assert result.home_type == (
        "residential"
    )

    assert result.description == (
        "Family home"
    )

    assert information_repository.saved is not None

    assert information_repository.saved.home_id == (
        result.id
    )

    assert information_repository.saved.address == (
        "10 Example Road"
    )

    assert information_repository.saved.postcode == (
        "SW1A 1AA"
    )

    assert state_repository.saved is not None

    assert state_repository.saved.home_id == (
        result.id
    )

    assert state_repository.saved.status == (
        "active"
    )

@pytest.mark.asyncio
async def test_home_service_links_related_records_to_created_home():

    home_repository = FakeHomeRepository()

    information_repository = (
        FakeHomeInformationRepository()
    )

    state_repository = FakeHomeStateRepository()

    service = HomeService(
        home_repository=home_repository,
        information_repository=(
            information_repository
        ),
        state_repository=state_repository,
    )

    request = CreateHomeRequest(
        name="Test Home",
        home_type="residential",
        information=HomeInformationInput(
            country="United Kingdom",
            city="London",
            address="20 Test Road",
        ),
    )

    home = await service.create(
        subject_id="subject-1",
        request=request,
    )

    assert (
        information_repository.saved.home_id
        == home.id
    )

    assert (
        state_repository.saved.home_id
        == home.id
    )


@pytest.mark.asyncio
async def test_home_service_allows_optional_description_and_postcode():

    home_repository = FakeHomeRepository()

    information_repository = (
        FakeHomeInformationRepository()
    )

    state_repository = FakeHomeStateRepository()

    service = HomeService(
        home_repository=home_repository,
        information_repository=(
            information_repository
        ),
        state_repository=state_repository,
    )

    request = CreateHomeRequest(
        name="Simple Home",
        home_type="residential",
        information=HomeInformationInput(
            country="United Kingdom",
            city="London",
            address="30 Test Road",
        ),
    )

    home = await service.create(
        subject_id="subject-1",
        request=request,
    )

    assert home.description is None

    assert (
        information_repository.saved.postcode
        is None
    )


@pytest.mark.asyncio
async def test_home_service_creates_home_and_related_records():

    home_repository = FakeHomeRepository()

    information_repository = (
        FakeHomeInformationRepository()
    )

    state_repository = FakeHomeStateRepository()

    service = HomeService(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
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

    result = await service.create(
        subject_id="subject-1",
        request=request,
    )

    assert result is home_repository.saved

    assert result.name == "My London Home"
    assert result.home_type == "residential"
    assert result.description == "Family home"

    assert information_repository.saved is not None

    assert information_repository.saved.home_id == result.id
    assert information_repository.saved.address == "10 Example Road"
    assert information_repository.saved.postcode == "SW1A 1AA"

    assert state_repository.saved is not None

    assert state_repository.saved.home_id == result.id
    assert state_repository.saved.status == "active"


@pytest.mark.asyncio
async def test_home_service_rejects_empty_home_name():

    home_repository = FakeHomeRepository()
    information_repository = (
        FakeHomeInformationRepository()
    )
    state_repository = FakeHomeStateRepository()

    service = HomeService(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
    )

    request = CreateHomeRequest(
        name="   ",
        home_type="residential",
        information=HomeInformationInput(
            country="United Kingdom",
            city="London",
            address="10 Example Road",
        ),
    )

    with pytest.raises(ValueError, match="Home name"):
        await service.create(
            subject_id="subject-1",
            request=request,
        )

    assert home_repository.saved is None
    assert information_repository.saved is None
    assert state_repository.saved is None

@pytest.mark.asyncio
async def test_home_service_rejects_invalid_home_type():

    home_repository = FakeHomeRepository()
    information_repository = (
        FakeHomeInformationRepository()
    )
    state_repository = FakeHomeStateRepository()

    service = HomeService(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
    )

    request = CreateHomeRequest(
        name="My Home",
        home_type="spaceship",
        information=HomeInformationInput(
            country="United Kingdom",
            city="London",
            address="10 Example Road",
        ),
    )

    with pytest.raises(
        ValueError,
        match="Invalid home type",
    ):
        await service.create(
            subject_id="subject-1",
            request=request,
        )

    assert home_repository.saved is None
    assert information_repository.saved is None
    assert state_repository.saved is None

@pytest.mark.asyncio
async def test_home_service_accepts_valid_home_type():

    home_repository = FakeHomeRepository()
    information_repository = (
        FakeHomeInformationRepository()
    )
    state_repository = FakeHomeStateRepository()

    service = HomeService(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
    )

    request = CreateHomeRequest(
        name="My Office",
        home_type="office",
        information=HomeInformationInput(
            country="United Kingdom",
            city="London",
            address="10 Example Road",
        ),
    )

    result = await service.create(
        subject_id="subject-1",
        request=request,
    )

    assert result.home_type == "office"


@pytest.mark.asyncio
async def test_home_service_publishes_home_created_event():

    home_repository = FakeHomeRepository()

    information_repository = (
        FakeHomeInformationRepository()
    )

    state_repository = FakeHomeStateRepository()

    publisher = FakeEventPublisher()

    service = HomeService(
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

    result = await service.create(
        subject_id="subject-1",
        request=request,
    )

    assert len(publisher.events) == 1

    event = publisher.events[0]

    assert isinstance(
        event,
        HomeCreatedEvent,
    )

    assert event.resource_id == result.id
    assert event.event_type == "home"
    assert event.event_name == "home_created"
    assert event.state == "created"

@pytest.mark.asyncio
async def test_home_service_persists_home_information_and_state():

    home_repository = FakeHomeRepository()

    information_repository = (
        FakeHomeInformationRepository()
    )

    state_repository = (
        FakeHomeStateRepository()
    )

    service = HomeService(
        home_repository=home_repository,
        information_repository=information_repository,
        state_repository=state_repository,
    )

    request = CreateHomeRequest(
        name="Integration Home",
        home_type="residential",
        description="A test home",
        information=HomeInformationInput(
            country="United Kingdom",
            city="London",
            address="10 Test Road",
            postcode="SW1A 1AA",
        ),
    )

    home = await service.create(
        subject_id="subject-1",
        request=request,
    )

    assert home is not None

    assert home_repository.saved is not None
    assert information_repository.saved is not None
    assert state_repository.saved is not None

    assert home_repository.saved.id == home.id

    information = (
        information_repository.saved
    )

    state = state_repository.saved

    assert information.home_id == home.id
    assert state.home_id == home.id