from abc import ABC, abstractmethod

from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


class LearningPatternAnalyzer(ABC):

    @abstractmethod
    def analyze(
        self,
        records: list[LearningRecord],
    ) -> list[LearningPattern]:
        raise NotImplementedError