from hios.capabilities.property.models.property_profile import (
    PropertyProfile,
)
from hios.capabilities.property.providers.base import (
    PropertyProvider,
)


class MockPropertyProvider(PropertyProvider):

    async def get_property(
        self,
        uprn: str,
    ) -> PropertyProfile | None:

        return PropertyProfile(
            uprn=uprn,
            address="10 Example Road, London",
            postcode="SW1A 1AA",
            year_built=1890,
            age_band="Pre-1900",
            property_type="residential",
            building_type="terraced",
            construction_material="brick",
            bedrooms=3,
            bathrooms=2,
            has_basement=True,
            epc_rating="D",
            latitude=51.5074,
            longitude=-0.1278,
        )