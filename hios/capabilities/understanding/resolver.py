from abc import ABC, abstractmethod

from hios.capabilities.knowledge.contract import KnowledgeResult

from .models.hypothesis import Hypothesis


class HypothesisResolver(ABC):

    @abstractmethod
    def resolve(
        self,
        knowledge: KnowledgeResult,
    ) -> list[Hypothesis]:
        raise NotImplementedError