from hios.runtime.runtime import Runtime
from hios.runtime.registry import CapabilityRegistry
from hios.runtime.types import CapabilityType

from tests.builders.capability_builder import DummyCapability


def test_runtime_resolves_capability():

    registry = CapabilityRegistry()

    capability = DummyCapability()

    registry.register(
        CapabilityType.KNOWLEDGE,
        capability,
    )

    runtime = Runtime(registry)

    assert (
        runtime.resolve(
            CapabilityType.KNOWLEDGE
        )
        is capability
    )