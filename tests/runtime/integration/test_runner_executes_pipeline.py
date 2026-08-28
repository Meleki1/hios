import pytest
from hios.runtime.process_status import ProcessStatus
from hios.runtime.process import Process
from hios.runtime.registry import CapabilityRegistry
from hios.runtime.runner import PipelineRunner
from hios.runtime.runtime import Runtime
from hios.runtime.types import CapabilityType
from tests.builders.capability_builder import DummyCapability, DummyResult, DummyRequest
from tests.runtime.conftest import TEST_PIPELINE


@pytest.mark.asyncio
async def test_runner_executes_pipeline():

    registry = CapabilityRegistry()

    registry.register(
        CapabilityType.KNOWLEDGE,
        DummyCapability(),
    )

    runtime = Runtime(registry)

    runner = PipelineRunner(runtime)

    process = Process.start(
        request=DummyRequest(),
    )

    completed = await runner.run(
        TEST_PIPELINE,
        process,
    )

    assert completed.status == ProcessStatus.COMPLETED
    assert completed.result.message == "Runtime OK"