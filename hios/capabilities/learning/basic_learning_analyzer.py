from collections import defaultdict

from hios.capabilities.learning.learning_analyzer import LearningAnalyzer
from hios.capabilities.learning.models.learning_pattern import (
    LearningPattern,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)
from hios.capabilities.learning.models.signal_performance import (
    SignalPerformance,
)


class BasicLearningAnalyzer(LearningAnalyzer):

    async def analyze(
        self,
        records: list[LearningRecord],
    ) -> list[LearningPattern]:

        grouped: dict[
            str,
            list[LearningRecord],
        ] = defaultdict(list)

        for record in records:
            grouped[record.target].append(record)

        patterns: list[LearningPattern] = []

        for target, target_records in grouped.items():

            sample_size = len(target_records)

            correct_count = sum(
                1
                for record in target_records
                if record.correct
            )

            incorrect_count = (
                sample_size - correct_count
            )

            accuracy = (
                correct_count / sample_size
                if sample_size > 0
                else 0.0
            )

            signal_performance = (
                self._analyze_signals(
                    target_records,
                )
            )

            patterns.append(
                LearningPattern(
                    target=target,
                    sample_size=sample_size,
                    correct_count=correct_count,
                    incorrect_count=incorrect_count,
                    accuracy=accuracy,
                    lesson=(
                        f"Predictions for {target} "
                        f"were correct "
                        f"{accuracy:.1%} of the time."
                    ),
                    signal_performance=(
                        signal_performance
                    ),
                )
            )

        return patterns

    @staticmethod
    def _analyze_signals(
        records: list[LearningRecord],
    ) -> dict[str, SignalPerformance]:

        grouped: dict[
            str,
            list[LearningRecord],
        ] = defaultdict(list)

        for record in records:
            for signal_name in record.signal_names:
                grouped[signal_name].append(record)

        performance: dict[
            str,
            SignalPerformance,
        ] = {}

        for signal_name, signal_records in grouped.items():

            sample_size = len(signal_records)

            correct_count = sum(
                1
                for record in signal_records
                if record.correct
            )

            incorrect_count = (
                sample_size - correct_count
            )

            accuracy = (
                correct_count / sample_size
                if sample_size > 0
                else 0.0
            )

            performance[signal_name] = (
                SignalPerformance(
                    sample_size=sample_size,
                    correct_count=correct_count,
                    incorrect_count=incorrect_count,
                    accuracy=accuracy,
                )
            )

        return performance