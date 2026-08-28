import pytest
from hios.capabilities.property.models.property_profile import PropertyProfile
from hios.capabilities.property.service import PropertyService
from hios.capabilities.property.providers.mock import MockPropertyProvider
from hios.capabilities.property.service import PropertyService
from hios.capabilities.property.address_service import PropertyReference


class FakePropertyProvider:

    async def get_property(
        self,
        uprn: str,
    ) -> PropertyProfile | None:

        return PropertyProfile(
            uprn=uprn,
            address="10 Example Road, London",
            postcode="SW1A 1AA",
            year_built=1890,
            building_type="terraced",
            epc_rating="D",
        )


@pytest.mark.asyncio
async def test_property_service_delegates_to_provider():

    provider = FakePropertyProvider()

    service = PropertyService(
        provider=provider,
    )

    result = await service.get_property(
        "100023456789",
    )

    assert result is not None

    assert result.address == (
        "10 Example Road, London"
    )

    assert result.uprn == "100023456789"
    assert result.year_built == 1890
    assert result.building_type == "terraced"
    assert result.epc_rating == "D"


def test_property_service_converts_profile_to_characteristics():

    provider = FakePropertyProvider()

    service = PropertyService(
        provider=provider,
    )

    profile = PropertyProfile(
        uprn="100023456789",
        address="10 Example Road, London",
        postcode="SW1A 1AA",
        year_built=1890,
        building_type="terraced",
        has_basement=True,
        epc_rating="D",
        bedrooms=3,
    )

    characteristics = service.to_characteristics(
        profile,
    )

    assert characteristics == {
        "uprn": "100023456789",
        "postcode": "SW1A 1AA",
        "year_built": "1890",
        "building_type": "terraced",
        "bedrooms": "3",
        "has_basement": "True",
        "epc_rating": "D",
    }

@pytest.mark.asyncio
async def test_property_service_can_use_mock_provider():

    provider = MockPropertyProvider()

    service = PropertyService(
        provider=provider,
    )

    profile = await service.get_property(
        "100023456789",
    )

    assert profile is not None
    assert profile.address == (
        "10 Example Road, London"
    )
    assert profile.uprn == "100023456789"
    assert profile.year_built == 1890
    assert profile.building_type == "terraced"
    assert profile.has_basement is True
    assert profile.epc_rating == "D"

@pytest.mark.asyncio
async def test_property_service_gets_property_from_reference():

    provider = MockPropertyProvider()

    service = PropertyService(
        provider=provider,
    )

    reference = PropertyReference(
        uprn="100023456789",
        address="10 Example Road, London",
        postcode="SW1A 1AA",
    )

    profile = await service.get_property_from_reference(
        reference,
    )

    assert profile is not None
    assert profile.uprn == "100023456789"