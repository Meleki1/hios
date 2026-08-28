from hios.capabilities.property.address_service import AddressResolutionService
from hios.capabilities.property.graph.state import PropertyState
from hios.capabilities.property.graph.state import PropertyState
from hios.capabilities.property.service import PropertyService



async def resolve_property(
    state: PropertyState,
    address_service: AddressResolutionService,
) -> dict:

    address = state["address"]

    candidates = await address_service.search(
        address,
    )

    if len(candidates) != 1:
        return {
            "property_reference": None,
        }

    return {
        "property_reference": candidates[0],
    }



async def enrich_property(
    state: PropertyState,
    property_service: PropertyService,
) -> dict:

    reference = state.get(
        "property_reference"
    )

    if reference is None:
        return {
            "property_profile": None,
        }

    profile = await property_service.get_property_from_reference(
        reference,
    )

    return {
        "property_profile": profile,
    }