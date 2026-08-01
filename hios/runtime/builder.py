from __future__ import annotations

from hios.runtime.hios import HIOS
from hios.runtime.registry import CapabilityRegistry
from hios.runtime.runner import PipelineRunner
from hios.runtime.runtime import Runtime
from hios.runtime.types import CapabilityType


class HIOSBuilder:

    def __init__(self) -> None:
        self._registry = CapabilityRegistry()

    def register(
        self,
        capability: CapabilityType,
        implementation,
    ) -> "HIOSBuilder":

        self._registry.register(
            capability,
            implementation,
        )

        return self

    def build(self) -> HIOS:

        runtime = Runtime(
            registry=self._registry,
        )

        runner = PipelineRunner(
            runtime=runtime,
        )

        return HIOS(runner)