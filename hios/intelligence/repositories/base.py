from abc import ABC, abstractmethod

from hios.intelligence.models.rule import Rule


class RuleRepository(ABC):
    """
    Loads intelligence rules.
    """

    @abstractmethod
    def load(self) -> list[Rule]:
        """
        Load all available rules.
        """
        raise NotImplementedError