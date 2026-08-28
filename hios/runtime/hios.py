from __future__ import annotations

from hios.runtime.pipeline import Pipeline
from hios.runtime.process import Process
from hios.runtime.runner import PipelineRunner


class HIOS:

    def __init__(
        self,
        *,
        runner: PipelineRunner,
        pipeline: Pipeline,
    ) -> None:

        self._runner = runner
        self._pipeline = pipeline

    async def execute(
        self,
        request,
    ):

        process = Process.start(
            request=request,
        )

        completed = await self._runner.run(
            self._pipeline,
            process
        )

        return completed.result