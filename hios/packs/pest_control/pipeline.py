from hios.runtime.pipeline import Pipeline, PipelineStep
from hios.runtime.types import CapabilityType


PEST_CONTROL_PIPELINE = Pipeline(
    name="Pest Control",
    steps=(
        PipelineStep(
            capability=CapabilityType.PEST_CONTROL,
        ),
    ),
)