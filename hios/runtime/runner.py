from __future__ import annotations

from hios.runtime.process import Process
from hios.runtime.runtime import Runtime
from hios.runtime.trace_entry import TraceEntry
from hios.runtime.pipeline import Pipeline


class PipelineRunner:

    def __init__(
        self,
        runtime: Runtime,
    ) -> None:
        self._runtime = runtime

    async def run(
        self,
        pipeline: Pipeline,
        process: Process,
    ) -> Process:

        process = process.running()

        for hook in pipeline.before_hooks:
            await hook.execute(process)
        
        current = process.request

        for step in pipeline.steps:

            capability = self._runtime.resolve(
                step.capability
            )

            result = await capability.execute(
                request=current,
                context=process.context,
            )

            process.trace.append(
                TraceEntry(
                    capability=step.capability,
                    request=current,
                    result=result,
                )
            )

            current = result

        process = process.complete(current)

        for hook in pipeline.after_hooks:
            await hook.execute(process)

        return process.complete(current)