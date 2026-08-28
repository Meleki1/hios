import pytest

from hios.capabilities.property.providers.homedata import (
    HomedataProvider,
)


class FakeHomedataClient:

    async def get_property(
        self,
        uprn: str,
    ) -> dict:

        return {
            "uprn": 100023336956,
            "full_address": (
                "10 Example Road, London"
            ),
            "postcode": "SW1A 1AA",
            "construction_age_band": (
                "1890-1918"
            ),
            "property_type": "residential",
            "building_type": "terraced",
            "construction_material": "brick",
            "bedrooms": 3,
            "bathrooms": 2,
            "floor_area": 120.5,
            "epc_rating": "D",
            "epc_efficiency": 65,
        }


@pytest.mark.asyncio
async def test_homedata_provider_maps_response_to_property_profile():

    client = FakeHomedataClient()

    provider = HomedataProvider(
        client=client,
    )

    profile = await provider.get_property(
        "100023336956",
    )

    assert profile is not None

    assert profile.uprn == "100023336956"

    assert profile.address == (
        "10 Example Road, London"
    )

    assert profile.postcode == "SW1A 1AA"

    assert profile.age_band == (
        "1890-1918"
    )

    assert profile.property_type == (
        "residential"
    )

    assert profile.building_type == (
        "terraced"
    )

    assert profile.construction_material == (
        "brick"
    )

    assert profile.bedrooms == 3

    assert profile.floor_area == 120.5

    assert profile.epc_rating == "D"

    assert profile.epc_efficiency == 65