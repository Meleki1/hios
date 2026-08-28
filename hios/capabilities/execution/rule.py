from hios.capabilities.execution.contract import (
    ExecutionCapability,
    ExecutionRequest,
    ExecutionResult,
)


class RuleExecutionCapability(
    ExecutionCapability,
):

    async def reason(
        self,
        request: ExecutionRequest,
        context,
    ) -> ExecutionResult:

        recommendations = request.decision.recommendations

        priority = request.decision.priority

        response = (
            f"Priority: {priority}. "
            f"Recommended actions: {' '.join(recommendations)}"
        )

        return ExecutionResult(
            response=response,
        )