from hios.capabilities.property.providers.homedata_address_client import (
    HomedataAddressClient,
)


def test_homedata_address_client_is_an_abstract_boundary():

    assert HomedataAddressClient is not None