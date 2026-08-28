from __future__ import annotations

from abc import ABC, abstractmethod

from hios.intelligence.conditions.condition import Condition
from hios.intelligence.evaluators.result import EvaluationResult


class ConditionEvaluator(ABC):

    @abstractmethod
    def evaluate(
        self,
        condition: Condition,
        observation: str,
    ) -> EvaluationResult:
        raise NotImplementedError