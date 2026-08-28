from hios.runtime.context import RuntimeContext

from hios.capabilities.planning.capability import PlanningCapability
from hios.capabilities.planning.contract import (
    PlanRequest,
    PlanResult,
)
from hios.capabilities.planning.planner import Planner


class DefaultPlanningCapability(
    PlanningCapability,
):

    def __init__(
        self,
        planner: Planner,
    ):

        self._planner = planner

    async def reason(
        self,
        request: PlanRequest,
        context: RuntimeContext,
    ) -> PlanResult:

        plans = self._planner.create(
            request.goals,
        )

        return PlanResult(
            plans=plans,
        )