from abc import ABC, abstractmethod

from hios.capabilities.planning.contract import PlanResult
from hios.capabilities.decision.models.decision import Decision


class DecisionSelector(
    ABC,
):

    @abstractmethod
    def select(
        self,
        plans: PlanResult,
    ) -> Decision | None:

        raise NotImplementedError