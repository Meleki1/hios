from hios.capabilities.property.models.property_profile import (
    PropertyProfile,
)


def test_property_profile_can_be_created():

    property_profile = PropertyProfile(
        uprn="100023456789",
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
    )

    assert property_profile.uprn == "100023456789"
    assert property_profile.year_built == 1890
    assert property_profile.building_type == "terraced"
    assert property_profile.has_basement is True
    assert property_profile.epc_rating == "D"