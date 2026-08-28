from abc import ABC, abstractmethod

from hios.capabilities.understanding.contract import UnderstandingResult

from .models.goal import Goal


class GoalGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        understanding: UnderstandingResult,
    ) -> list[Goal]:
        raise NotImplementedError