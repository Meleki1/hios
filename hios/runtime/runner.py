from __future__ import annotations

from hios.runtime.process import Process
from hios.runtime.runtime import Runtime


class PipelineRunner:
    """
    Executes a Process through its Pipeline.
    """

    def __init__(
        self,
        runtime: Runtime,
    ) -> None:
        self._runtime = runtime

    async def run(self, process: Process) -> Process:

        process = process.running()

        current = process.request

        for step in process.pipeline.steps:

            capability = self._runtime.resolve(
                step.capability
            )

            current = await capability.execute(
                request=current,
                context=process.context,
            )

        return process.complete(current)