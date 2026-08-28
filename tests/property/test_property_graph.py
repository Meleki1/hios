import pytest

from hios.capabilities.property.address_service import AddressResolutionService

from hios.capabilities.property.graph.nodes import resolve_property
from hios.capabilities.property.models.property_profile import PropertyProfile
from hios.capabilities.property.graph.state import PropertyState
from hios.capabilities.property.service import PropertyService
from hios.capabilities.property.graph.nodes import enrich_property
from hios.capabilities.property.address_service import PropertyReference
from hios.capabilities.property.graph.workflow import build_property_graph
 

class FakeAddressClient:

    async def search(
        self,
        query: str,
    ) -> list[dict]:

        return [
            {
                "uprn": 100023336956,
                "address": "10 Example Road, London",
                "postcode": "SW1A 1AA",
            }
        ]

class FakePropertyProvider:

    async def get_property(
        self,
        uprn: str,
    ):
        return PropertyProfile(
            uprn=uprn,
            address="10 Example Road, London",
            postcode="SW1A 1AA",
            year_built=1890,
            building_type="terraced",
            epc_rating="D",
        )


@pytest.mark.asyncio
async def test_resolve_property_node():

    address_service = AddressResolutionService(
        client=FakeAddressClient(),
    )

    state: PropertyState = {
        "address": "10 Example Road, London",
    }

    result = await resolve_property(
        state=state,
        address_service=address_service,
    )

    reference = result["property_reference"]

    assert reference.uprn == "100023336956"

    assert reference.address == (
        "10 Example Road, London"
    )

    assert reference.postcode == "SW1A 1AA"

@pytest.mark.asyncio
async def test_enrich_property_node():

    property_service = PropertyService(
        provider=FakePropertyProvider(),
    )

    reference = PropertyReference(
        uprn="100023336956",
        address="10 Example Road, London",
        postcode="SW1A 1AA",
    )

    state: PropertyState = {
        "address": "10 Example Road, London",
        "property_reference": reference,
    }

    result = await enrich_property(
        state=state,
        property_service=property_service,
    )

    profile = result["property_profile"]

    assert profile is not None

    assert profile.uprn == (
        "100023336956"
    )

    assert profile.address == (
        "10 Example Road, London"
    )

    assert profile.year_built == 1890

    assert profile.building_type == (
        "terraced"
    )

    assert profile.epc_rating == "D"


@pytest.mark.asyncio
async def test_property_graph_resolves_and_enriches_property():

    address_service = AddressResolutionService(
        client=FakeAddressClient(),
    )

    property_service = PropertyService(
        provider=FakePropertyProvider(),
    )

    graph = build_property_graph(
        address_service=address_service,
        property_service=property_service,
    )

    result = await graph.ainvoke(
        {
            "address": "10 Example Road, London",
        }
    )

    assert result["property_reference"].uprn == (
        "100023336956"
    )

    assert result["property_profile"].uprn == (
        "100023336956"
    )

    assert result["property_profile"].address == (
        "10 Example Road, London"
    )