from tests.runtime.conftest import DummyRequest, DummyResult
from hios.contracts.capability import Capability
from hios.runtime.context import RuntimeContext


class DummyCapability(Capability[DummyRequest, DummyResult]):

    async def reason(
        self,
        request: DummyRequest,
        context: RuntimeContext,
    ) -> DummyResult:

        return DummyResult()

