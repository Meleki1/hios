from __future__ import annotations

from hios.runtime.process import Process
from hios.runtime.runner import PipelineRunner


class HIOS:
   
    def __init__(self, runner: PipelineRunner) -> None:
        self._runner = runner

    async def run(
        self,
        process: Process,
    ) -> Process:

        return await self._runner.run(process)