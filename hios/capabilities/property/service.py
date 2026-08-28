from hios.capabilities.property.models.property_profile import PropertyProfile
from hios.capabilities.property.providers.base import PropertyProvider
from hios.capabilities.property.providers.homedata_address_client import HomedataAddressClient
from hios.capabilities.property.address_service import PropertyReference


class PropertyService:

    def __init__(
        self,
        provider: PropertyProvider,
    ):
        self._provider = provider

    async def get_property(
        self,
        uprn: str,
    ) -> PropertyProfile | None:

        return await self._provider.get_property(
            uprn,
        )

    async def get_property_by_address(
        self,
        address: str,
        address_client: HomedataAddressClient,
    ) -> PropertyProfile | None:

        candidates = await address_client.search(
            address,
        )

        if len(candidates) != 1:
            return None

        uprn = candidates[0]["uprn"]

        return await self.get_property(
            str(uprn),
        )

    async def get_property_from_reference(
        self,
        reference: PropertyReference,
    ) -> PropertyProfile | None:

        return await self._provider.get_property(
            reference.uprn,
        )

    def to_characteristics(
        self,
        property_profile: PropertyProfile,
    ) -> dict[str, str]:

        characteristics: dict[str, str] = {}

        if property_profile.uprn is not None:
            characteristics["uprn"] = (
                property_profile.uprn
            )

        if property_profile.postcode is not None:
            characteristics["postcode"] = (
                property_profile.postcode
            )

        if property_profile.year_built is not None:
            characteristics["year_built"] = str(
                property_profile.year_built
            )

        if property_profile.age_band is not None:
            characteristics["age_band"] = (
                property_profile.age_band
            )

        if property_profile.property_type is not None:
            characteristics["property_type"] = (
                property_profile.property_type
            )

        if property_profile.building_type is not None:
            characteristics["building_type"] = (
                property_profile.building_type
            )

        if property_profile.construction_material is not None:
            characteristics["construction_material"] = (
                property_profile.construction_material
            )

        if property_profile.bedrooms is not None:
            characteristics["bedrooms"] = str(
                property_profile.bedrooms
            )

        if property_profile.bathrooms is not None:
            characteristics["bathrooms"] = str(
                property_profile.bathrooms
            )

        if property_profile.floor_count is not None:
            characteristics["floor_count"] = str(
                property_profile.floor_count
            )

        if property_profile.floor_area is not None:
            characteristics["floor_area"] = str(
                property_profile.floor_area
            )

        if property_profile.has_basement is not None:
            characteristics["has_basement"] = str(
                property_profile.has_basement
            )

        if property_profile.epc_rating is not None:
            characteristics["epc_rating"] = (
                property_profile.epc_rating
            )

        if property_profile.epc_efficiency is not None:
            characteristics["epc_efficiency"] = str(
                property_profile.epc_efficiency
            )

        if property_profile.latitude is not None:
            characteristics["latitude"] = str(
                property_profile.latitude
            )

        if property_profile.longitude is not None:
            characteristics["longitude"] = str(
                property_profile.longitude
            )

        return characteristics