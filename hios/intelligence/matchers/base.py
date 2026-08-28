from abc import ABC, abstractmethod

from hios.intelligence.models.rule import Rule


class ConditionEvaluator(ABC):
    """
    Determines whether a rule applies to some input.
    """

    @abstractmethod
    def matches(
        self,
        rule: Rule,
        text: str,
    ) -> bool:
        raise NotImplementedError