from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.learning.models.learning_insight import (
    LearningInsight,
)
from hios.capabilities.learning.postgres.models.learning_insight_record import (
    LearningInsightModel,
)
from hios.capabilities.learning.learning_insight_repository import (
    LearningInsightRepository,
)


class PostgresLearningInsightRepository(
    LearningInsightRepository,
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        insight: LearningInsight,
    ) -> LearningInsight:

        model = LearningInsightModel(
            id=insight.id,
            target=insight.target,
            signal_name=insight.signal_name,
            sample_size=insight.sample_size,
            correct_count=insight.correct_count,
            incorrect_count=insight.incorrect_count,
            accuracy=insight.accuracy,
            insight=insight.insight,
        )

        self._session.add(model)

        await self._session.commit()

        await self._session.refresh(model)

        return self._to_domain(model)

    async def get_all(
        self,
    ) -> list[LearningInsight]:

        stmt = select(
            LearningInsightModel
        )

        result = await self._session.execute(
            stmt,
        )

        models = result.scalars().all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: LearningInsightModel,
    ) -> LearningInsight:

        return LearningInsight(
            id=model.id,
            target=model.target,
            signal_name=model.signal_name,
            sample_size=model.sample_size,
            correct_count=model.correct_count,
            incorrect_count=model.incorrect_count,
            accuracy=model.accuracy,
            insight=model.insight,
        )