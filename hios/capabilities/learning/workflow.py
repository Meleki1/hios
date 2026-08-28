from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.learning.models.learning_record import LearningRecord
from hios.capabilities.learning.models.learning_insight import LearningInsight

class LearningWorkflow:

    def __init__(
        self,
        intelligence_service,
        learning_service,
        learning_repository,
    ):
        self._intelligence_service = intelligence_service
        self._learning_service = learning_service
        self._learning_repository = learning_repository

    async def process(
        self,
        prediction: Prediction,
        outcome: Outcome,
    ) -> LearningRecord:

        evaluation = await self._intelligence_service.evaluate(
            prediction=prediction,
            outcome=outcome,
        )

        learning_record = (
            await self._learning_service.learn_from_prediction(
                prediction=prediction,
                outcome=outcome,
                evaluation=evaluation,
            )
        )

        return await self._learning_repository.save(
            learning_record,
        )


class LearningInsightWorkflow:

    def __init__(
        self,
        analyzer,
        insight_generator,
        insight_repository,
    ):
        self._analyzer = analyzer
        self._insight_generator = insight_generator
        self._insight_repository = insight_repository

    async def process(
        self,
        records: list[LearningRecord],
    ) -> list[LearningInsight]:

        patterns = await self._analyzer.analyze(
            records,
        )

        insights: list[LearningInsight] = []

        for pattern in patterns:
            generated = await self._insight_generator.generate(
                pattern,
            )

            for insight in generated:
                saved = await self._insight_repository.save(
                    insight,
                )
                insights.append(saved)

        return insights