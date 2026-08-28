import pytest
from hios.capabilities.home.models.home import Home
from hios.capabilities.home.models.home_information import HomeInformation
from hios.capabilities.home.models.home_state import (
    HomeState,
)
from hios.capabilities.home.repositories.home_information_repository import HomeInformationRepository
from hios.capabilities.home.repositories.home_repository import HomeRepository
from hios.capabilities.home.repositories.home_state_repository import HomeStateRepository



class FakeHomeRepository(HomeRepository):

    def __init__(self):
        self.items = {}

    async def save(
        self,
        home: Home,
    ) -> Home:

        self.items[home.id] = home

        return home

    async def get(
        self,
        home_id: str,
    ) -> Home | None:

        return self.items.get(home_id)

class FakeHomeInformationRepository(
    HomeInformationRepository,
):

    def __init__(self):
        self.items = {}

    async def save(
        self,
        information: HomeInformation,
    ) -> HomeInformation:

        self.items[information.home_id] = (
            information
        )

        return information

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeInformation | None:

        return self.items.get(home_id)


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

@pytest.mark.asyncio
async def test_home_repository_saves_and_retrieves_home():

    repository = FakeHomeRepository()

    home = Home(
        name="My London Home",
        home_type="residential",
        description="Family home",
        status="active",
    )

    saved = await repository.save(home)

    result = await repository.get(
        home.id,
    )

    assert saved is home
    assert result is home

@pytest.mark.asyncio
async def test_home_information_repository_saves_and_retrieves_information():

    repository = (
        FakeHomeInformationRepository()
    )

    information = HomeInformation(
        home_id="home-1",
        country="United Kingdom",
        city="London",
        address="10 Example Road",
        postcode="SW1A 1AA",
    )

    saved = await repository.save(
        information,
    )

    result = await repository.get_by_home(
        "home-1",
    )

    assert saved is information
    assert result is information


@pytest.mark.asyncio
async def test_home_state_repository_saves_and_retrieves_state():

    repository = FakeHomeStateRepository()

    state = HomeState(
        home_id="home-1",
        status="active",
    )

    saved = await repository.save(
        state,
    )

    result = await repository.get_by_home(
        "home-1",
    )

    assert saved is state
    assert result is state

@pytest.mark.asyncio
async def test_home_repository_returns_none_for_unknown_home():

    repository = FakeHomeRepository()

    result = await repository.get(
        "does-not-exist",
    )

    assert result is None


@pytest.mark.asyncio
async def test_home_information_repository_returns_none_for_unknown_home():

    repository = (
        FakeHomeInformationRepository()
    )

    result = await repository.get_by_home(
        "does-not-exist",
    )

    assert result is None


@pytest.mark.asyncio
async def test_home_state_repository_returns_none_for_unknown_home():

    repository = FakeHomeStateRepository()

    result = await repository.get_by_home(
        "does-not-exist",
    )

    assert result is None



