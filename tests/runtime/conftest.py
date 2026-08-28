from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from hios.runtime.pipeline import Pipeline, PipelineStep
from hios.runtime.types import CapabilityType
from hios.intelligence.repositories.base import RuleRepository
from hios.intelligence.models.rule import Rule
from hios.runtime.context import RuntimeContext
from hios.contracts.capability import Capability

class DummyRequest(CapabilityRequest):
    pass


class DummyResult(CapabilityResult):
    message: str = "Runtime OK"


class DummyCapability(Capability[DummyRequest, DummyResult]):

    async def reason(
        self,
        request: DummyRequest,
        context: RuntimeContext,
    ) -> DummyResult:

        return DummyResult()


TEST_PIPELINE = Pipeline(
    name="runtime",
    steps=(
        PipelineStep(
            capability=CapabilityType.KNOWLEDGE,
        ),
    ),
)


class InMemoryRuleRepository(
    RuleRepository,
):

    def __init__(
        self,
        rules: list[Rule],
    ):

        self._rules = rules

    def load(
        self,
    ) -> list[Rule]:

        return self._rules