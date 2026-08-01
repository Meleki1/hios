from __future__ import annotations

from hios.contracts.capability import Capability
from hios.runtime.types import CapabilityType


class CapabilityRegistry:
    """
    Registry of capability implementations.
    """

    def __init__(self) -> None:
        self._capabilities: dict[
            CapabilityType,
            Capability,
        ] = {}

    def register(
        self,
        capability: CapabilityType,
        implementation: Capability,
    ) -> None:
        self._capabilities[capability] = implementation

    def resolve(
        self,
        capability: CapabilityType,
    ) -> Capability:

        try:
            return self._capabilities[capability]

        except KeyError as exc:
            raise LookupError(
                f"No implementation registered for '{capability.value}'."
            ) from exc