from __future__ import annotations

from abc import ABC, abstractmethod

from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.memory.investigation.question import (
    InvestigationQuestion,
)


class Planner(ABC):

    @abstractmethod
    def create(
        self,
        goals: GoalResult,
        investigation_question: InvestigationQuestion | None = None
    ) -> list[Plan]:
        raise NotImplementedError