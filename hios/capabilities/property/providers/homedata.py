from typing import Any

from hios.capabilities.property.models.property_profile import (
    PropertyProfile,
)
from hios.capabilities.property.providers.base import (
    PropertyProvider,
)
from hios.capabilities.property.providers.homedata_client import (
    HomedataClient,
)


class HomedataProvider(PropertyProvider):

    def __init__(
        self,
        client: HomedataClient,
    ):
        self._client = client

    async def get_property(
        self,
        uprn: str,
    ) -> PropertyProfile | None:

        data = await self._client.get_property(
            uprn,
        )

        if not data:
            return None

        return self._to_property_profile(data)

    def _to_property_profile(
        self,
        data: dict[str, Any],
    ) -> PropertyProfile:

        return PropertyProfile(
            uprn=str(data["uprn"])
            if data.get("uprn") is not None
            else None,

            address=data.get(
                "full_address",
                "",
            ),

            postcode=data.get(
                "postcode",
            ),

            age_band=data.get(
                "construction_age_band",
            ),

            property_type=data.get(
                "property_type",
            ),

            building_type=data.get(
                "building_type",
            ),

            construction_material=data.get(
                "construction_material",
            ),

            bedrooms=data.get(
                "bedrooms",
            ),

            bathrooms=data.get(
                "bathrooms",
            ),

            floor_area=data.get(
                "floor_area",
            ),

            epc_rating=data.get(
                "epc_rating",
            ),

            epc_efficiency=data.get(
                "epc_efficiency",
            ),

            metadata=data,
        )