from hios.runtime.pipeline import Pipeline, PipelineStep
from hios.runtime.types import CapabilityType

TEST_PIPELINE = Pipeline(
    name="test",
    steps=(
        PipelineStep(CapabilityType.KNOWLEDGE),
    ),
)