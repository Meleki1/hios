import pytest

from hios.runtime.pipeline import Pipeline, PipelineStep
from hios.runtime.process import Process
from hios.runtime.registry import CapabilityRegistry
from hios.runtime.runner import PipelineRunner
from hios.runtime.runtime import Runtime
from hios.runtime.types import CapabilityType

from tests.runtime.conftest import DummyCapability, DummyRequest

class RecordingHook:

    def __init__(self):
        self.called = False
        self.status = None
        self.result = None

    async def execute(
        self,
        process,
    ):
        self.called = True
        self.status = process.status
        self.result = process.result

        """before = RecordingHook()
        after = RecordingHook()

        pipeline = Pipeline(
            name="runtime",
            steps=(
                PipelineStep(
                    capability=CapabilityType.KNOWLEDGE,
                ),
            ),
            before_hooks=(before,),
            after_hooks=(after,),
        )
        assert before.called is True
        assert after.called is True"""

@pytest.mark.asyncio
async def test_runner_executes_before_and_after_hooks():

    registry = CapabilityRegistry()

    registry.register(
        CapabilityType.KNOWLEDGE,
        DummyCapability(),
    )

    runtime = Runtime(registry)
    runner = PipelineRunner(runtime)

    before = RecordingHook()
    after = RecordingHook()

    pipeline = Pipeline(
        name="runtime-hooks",
        steps=(
            PipelineStep(
                capability=CapabilityType.KNOWLEDGE,
            ),
        ),
        before_hooks=(before,),
        after_hooks=(after,),
    )

    process = Process.start(
        request=DummyRequest(),
    )

    completed = await runner.run(
        pipeline,
        process,
    )

    assert completed.status.value == "COMPLETED"

    assert before.called is True
    assert after.called is True

    assert before.status.value == "RUNNING"

    assert after.status.value == "COMPLETED"
    assert after.result is not None
    assert after.result.message