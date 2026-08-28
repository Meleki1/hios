from pydantic import Field

from hios.contracts.results import CapabilityResult

from hios.capabilities.goals.models.goal import Goal


class GoalResult(CapabilityResult):

    goals: list[Goal] = Field(
        default_factory=list,
    )