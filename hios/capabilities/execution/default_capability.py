from hios.runtime.context import RuntimeContext

from hios.capabilities.execution.capability import (
    ExecutionCapability,
)
from hios.capabilities.execution.contract import (
    ExecutionRequest,
    ExecutionResult,
)
from hios.capabilities.execution.executor import Executor
from hios.capabilities.execution.models.execution import Execution


class DefaultExecutionCapability(
    ExecutionCapability,
):

    def __init__(
        self,
        executor: Executor,
    ):

        self._executor = executor

    async def reason(
        self,
        request: ExecutionRequest,
        context: RuntimeContext,
    ) -> ExecutionResult:

        execution = Execution(
            decision=request.decision.decision,
        )

        execution = self._executor.execute(
            execution,
        )

        return ExecutionResult(
            execution=execution,
        )