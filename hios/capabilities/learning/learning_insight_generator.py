from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)
from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)


class LearningInsightGenerator:

    def generate(
        self,
        patterns: list[LearningPattern],
    ) -> list[LearningInsight]:

        insights: list[LearningInsight] = []

        for pattern in patterns:

            for (
                signal_name,
                performance,
            ) in pattern.signal_performance.items():

                insights.append(
                    LearningInsight(
                        target=pattern.target,
                        signal_name=signal_name,
                        sample_size=performance.sample_size,
                        correct_count=performance.correct_count,
                        incorrect_count=performance.incorrect_count,
                        accuracy=performance.accuracy,
                        insight=(
                            f"The signal {signal_name} "
                            f"was associated with {pattern.target} "
                            f"being correct "
                            f"{performance.accuracy:.1%} of the time."
                        ),
                    )
                )

        return insights