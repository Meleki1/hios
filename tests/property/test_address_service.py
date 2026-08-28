import pytest

from hios.capabilities.property.address_service import (
    AddressResolutionService,
)


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
            },
            {
                "uprn": 100023336957,
                "address": "10A Example Road, London",
                "postcode": "SW1A 1AA",
            },
        ]


@pytest.mark.asyncio
async def test_address_service_returns_property_references():

    service = AddressResolutionService(
        client=FakeAddressClient(),
    )

    results = await service.search(
        "10 Example Road, London",
    )

    assert len(results) == 2

    assert results[0].uprn == "100023336956"

    assert results[0].address == (
        "10 Example Road, London"
    )

    assert results[0].postcode == "SW1A 1AA"