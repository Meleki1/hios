from dataclasses import dataclass

from hios.capabilities.property.providers.homedata_address_client import (
    HomedataAddressClient,
)


@dataclass(frozen=True)
class PropertyReference:
    uprn: str
    address: str
    postcode: str | None = None


class AddressResolutionService:

    def __init__(
        self,
        client: HomedataAddressClient,
    ):
        self._client = client

    async def search(
        self,
        query: str,
    ) -> list[PropertyReference]:

        results = await self._client.search(
            query,
        )

        return [
            PropertyReference(
                uprn=str(result["uprn"]),
                address=result.get(
                    "address",
                    "",
                ),
                postcode=result.get(
                    "postcode",
                ),
            )
            for result in results
            if result.get("uprn") is not None
        ]