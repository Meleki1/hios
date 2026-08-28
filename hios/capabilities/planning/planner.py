from __future__ import annotations

from abc import ABC, abstractmethod

from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.planning.models.plan import Plan


class Planner(ABC):

    @abstractmethod
    def create(
        self,
        goals: GoalResult,
    ) -> list[Plan]:
        raise NotImplementedError