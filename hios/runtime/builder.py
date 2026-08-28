from __future__ import annotations

from hios.runtime.hios import HIOS
from hios.runtime.registry import CapabilityRegistry
from hios.runtime.runner import PipelineRunner
from hios.runtime.runtime import Runtime 
from hios.kernel.container import ServiceContainer

class HIOSBuilder:

    def __init__(self):

        self._container = ServiceContainer()
        self._registry = CapabilityRegistry()
        self._pipeline = None


    def register(
        self,
        capability,
        implementation,
    ) -> "HIOSBuilder":

        self._registry.register(
            capability,
            implementation,
        )

        return self

    def pipeline(
        self,
        pipeline,
    ) -> "HIOSBuilder":

        self._pipeline = pipeline

        return self

    def container(
        self,
        container: ServiceContainer,
    ) -> "HIOSBuilder":

        self._container = container

        return self


    def build(self) -> HIOS:

        if self._pipeline is None:
                raise ValueError("A pipeline must be configured before building HIOS.")

        runtime = Runtime(self._registry)

        runner = PipelineRunner(runtime)

        return HIOS(
            runner=runner,
            pipeline=self._pipeline,
        )