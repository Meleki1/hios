from __future__ import annotations

from hios.contracts.capability import Capability
from hios.runtime.registry import CapabilityRegistry
from hios.runtime.types import CapabilityType


class Runtime:
    """
    Provides access to registered capabilities.

    The Runtime is intentionally small. It does not execute
    capabilities or orchestrate pipelines. Those responsibilities
    belong to the PipelineRunner.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
    ) -> None:
        self._registry = registry

    def resolve(
        self,
        capability: CapabilityType,
    ) -> Capability:
        """
        Resolve a capability implementation.
        """
        return self._registry.resolve(capability)