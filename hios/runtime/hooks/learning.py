from hios.runtime.hooks.base import PipelineHook
from hios.runtime.process import Process


class LearningHook(
    PipelineHook,
):

    async def execute(
        self,
        process: Process
    ) -> None:

        for entry in process.trace.entries:

            print(
                entry.capability,
            )