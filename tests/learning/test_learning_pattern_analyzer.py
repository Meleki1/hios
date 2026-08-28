import pytest
from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)
from hios.capabilities.learning.learning_pattern_analyzer import (
    LearningPatternAnalyzer,
)


class FakeLearningPatternAnalyzer(
    LearningPatternAnalyzer,
):

    def analyze(
        self,
        records,
    ) -> list[LearningPattern]:

        return []


def test_learning_pattern_analyzer_returns_patterns():

    analyzer = FakeLearningPatternAnalyzer()

    result = analyzer.analyze([])

    assert isinstance(result, list)
    assert result == []