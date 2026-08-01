from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from hios.runtime.pipeline import Pipeline, PipelineStep
from hios.runtime.types import CapabilityType


class DummyRequest(CapabilityRequest):
    pass


class DummyResult(CapabilityResult):
    message: str = "Runtime OK"


TEST_PIPELINE = Pipeline(
    name="runtime",
    steps=(
        PipelineStep(
            capability=CapabilityType.KNOWLEDGE,
        ),
    ),
)