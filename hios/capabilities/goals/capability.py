from hios.capabilities.goals.generator import GoalGenerator
from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.goals.request import GoalRequest
from hios.capabilities.goals.contract.result import GoalResult
from hios.runtime.context import RuntimeContext
from hios.contracts.capability import Capability
from abc import ABC



class GoalCapability(
    Capability[
        GoalRequest,
        GoalResult,
    ],
    ABC,
):
    pass

class DefaultGoalCapability(GoalCapability):

    def __init__(
        self,
        generator: GoalGenerator,
    ) -> None:

        self._generator = generator

    async def reason(
        self,
        request: GoalRequest,
        context: RuntimeContext,
    ) -> GoalResult:

        goals = self._generator.generate(
            request.understanding,
        )

        return GoalResult(
            goals=goals,
        )