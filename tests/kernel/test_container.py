from hios.kernel.container import ServiceContainer


class DummyService:
    pass


def test_register_and_resolve():

    container = ServiceContainer()

    service = DummyService()

    container.register(
        DummyService,
        service,
    )

    assert container.resolve(
        DummyService,
    ) is service

import pytest

from hios.kernel.container import ServiceContainer


class DummyService:
    pass


def test_unknown_service():

    container = ServiceContainer()

    with pytest.raises(LookupError):
        container.resolve(
            DummyService,
        )

def test_contains():

    container = ServiceContainer()

    service = DummyService()

    container.register(
        DummyService,
        service,
    )

    assert container.contains(
        DummyService,
    )

def test_clear():

    container = ServiceContainer()

    service = DummyService()

    container.register(
        DummyService,
        service,
    )

    container.clear()

    assert not container.contains(
        DummyService,
    )