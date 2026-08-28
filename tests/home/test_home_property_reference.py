import pytest
from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)
from pydantic import ValidationError

from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)


def test_home_property_reference_links_home_to_property():

    reference = HomePropertyReference(
        home_id="home-123",
        uprn="100023456789",
    )

    assert reference.id is not None
    assert reference.home_id == "home-123"
    assert reference.uprn == "100023456789"




def test_home_property_reference_requires_home_id():

    with pytest.raises(ValidationError):

        HomePropertyReference(
            uprn="100023456789",
        )


def test_home_property_reference_requires_uprn():

    with pytest.raises(ValidationError):

        HomePropertyReference(
            home_id="home-123",
        )


def test_home_property_reference_generates_unique_ids():

    first = HomePropertyReference(
        home_id="home-123",
        uprn="100023456789",
    )

    second = HomePropertyReference(
        home_id="home-456",
        uprn="100098765432",
    )

    assert first.id != second.id