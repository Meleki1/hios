from typing import TypedDict

from hios.capabilities.property.address_service import (
    PropertyReference,
)
from hios.capabilities.property.models.property_profile import (
    PropertyProfile,
)


class PropertyState(TypedDict, total=False):

    address: str

    property_reference: PropertyReference

    property_profile: PropertyProfile

    property_characteristics: dict[str, str]