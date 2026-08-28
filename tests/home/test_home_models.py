import pytest

from hios.capabilities.home.models.home import Home
from hios.capabilities.home.models.home_status import HomeStatus
from hios.capabilities.home.models.home_type import HomeType
from hios.capabilities.home.models.home_information import HomeInformation
from hios.capabilities.home.models.home_state import HomeState



def test_home_can_be_created():

    home = Home(
        name="My London Home",
        home_type=HomeType.RESIDENTIAL,
        description="Family home",
        status=HomeStatus.ACTIVE,
    )

    assert home.id is not None
    assert home.name == "My London Home"
    assert home.home_type == HomeType.RESIDENTIAL
    assert home.description == "Family home"
    assert home.status == HomeStatus.ACTIVE




def test_home_information_can_be_created():

    information = HomeInformation(
        home_id="home-1",
        country="United Kingdom",
        city="London",
        address="10 Example Road",
        postcode="SW1A 1AA",
    )

    assert information.id is not None
    assert information.home_id == "home-1"
    assert information.country == "United Kingdom"
    assert information.city == "London"
    assert information.address == "10 Example Road"
    assert information.postcode == "SW1A 1AA"




def test_home_state_defaults_to_active():

    state = HomeState(
        home_id="home-1",
    )

    assert state.id is not None
    assert state.home_id == "home-1"
    assert state.status == "active"


def test_home_supports_optional_fields():

    home = Home(
        name="My Home",
        home_type=HomeType.RESIDENTIAL,
    )

    information = HomeInformation(
        home_id=home.id,
        country="United Kingdom",
        city="London",
        address="10 Example Road",
    )

    assert home.description is None
    assert information.postcode is None


def test_home_types():

    assert HomeType.RESIDENTIAL.value == "residential"
    assert HomeType.COMMERCIAL.value == "commercial"
    assert HomeType.INDUSTRIAL.value == "industrial"
    assert HomeType.VACATION.value == "vacation"
    assert HomeType.OFFICE.value == "office"
    assert HomeType.SMART_HOME.value == "smart_home"


def test_home_statuses():

    assert HomeStatus.ACTIVE.value == "active"
    assert HomeStatus.ARCHIVED.value == "archived"
    assert HomeStatus.PENDING.value == "pending"