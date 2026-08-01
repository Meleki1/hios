from tests.runtime.conftest import DummyRequest, DummyResult
from hios.contracts.capability import Capability

class DummyCapability(
    Capability[
        DummyRequest,
        DummyResult,
    ]
):

    async def execute(
        self,
        request,
        context,
    ):
        return DummyResult(
            message="Runtime OK"
        )

