import pytest
from hios.runtime.registry import CapabilityRegistry
from hios.runtime.types import CapabilityType
from tests.builders.capability_builder import DummyCapability


def test_register_capability():

    registry = CapabilityRegistry()

    capability = DummyCapability()

    registry.register(
        CapabilityType.KNOWLEDGE,
        capability,
    )

    assert (
        registry.resolve(
            CapabilityType.KNOWLEDGE
        )
        is capability
    )


def test_unknown_capability():

    registry = CapabilityRegistry()

    with pytest.raises(LookupError):

        registry.resolve(
            CapabilityType.KNOWLEDGE
        )