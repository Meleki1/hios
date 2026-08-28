from abc import ABC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)
from hios.capabilities.learning.learning_repository import (
    LearningRepository,
)
from hios.capabilities.learning.postgres.models.learning_record import (
    LearningRecordModel,
)


class PostgresLearningRepository(
    LearningRepository,
):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def get_all(
        self,
    ) -> list[LearningRecord]:

        stmt = select(LearningRecordModel)

        result = await self._session.execute(
            stmt,
        )

        models = result.scalars().all()

        return [
            self._to_domain(model)
            for model in models
        ]
        
    async def save(
        self,
        record: LearningRecord,
    ) -> LearningRecord:

        model = LearningRecordModel(
            id=record.id,
            prediction_id=record.prediction_id,
            outcome_id=record.outcome_id,
            evaluation_id=record.evaluation_id,
            target=record.target,
            correct=record.correct,
            signal_names=record.signal_names,
            signal_values=record.signal_values,
            signal_strengths=record.signal_strengths,
            signal_confidences=record.signal_confidences,
            intent_score=record.intent_score,
            prediction_confidence=(
                record.prediction_confidence
            ),
            lesson=record.lesson,
        )

        self._session.add(model)

        await self._session.commit()

        await self._session.refresh(model)

        return self._to_domain(model)

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> LearningRecord | None:

        stmt = (
            select(LearningRecordModel)
            .where(
                LearningRecordModel.prediction_id
                == prediction_id,
            )
        )

        result = await self._session.execute(
            stmt,
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: LearningRecordModel,
    ) -> LearningRecord:

        return LearningRecord(
            id=model.id,
            prediction_id=model.prediction_id,
            outcome_id=model.outcome_id,
            evaluation_id=model.evaluation_id,
            target=model.target,
            correct=model.correct,
            signal_names=model.signal_names,
            signal_values=model.signal_values,
            signal_strengths=model.signal_strengths,
            signal_confidences=model.signal_confidences,
            intent_score=model.intent_score,
            prediction_confidence=(
                model.prediction_confidence
            ),
            lesson=model.lesson,
        )