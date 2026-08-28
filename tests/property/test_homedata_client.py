from hios.capabilities.property.providers.homedata_client import (
    HomedataClient,
)


def test_homedata_client_is_an_abstract_boundary():

    assert HomedataClient is not None