from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)
from hios.capabilities.intelligence.postgres.models.prediction_evaluation import (
    PredictionEvaluationRecord,
)

from hios.capabilities.intelligence.prediction_evaluation_repository import PredictionEvaluationRepository


class PostgresPredictionEvaluationRepository(PredictionEvaluationRepository):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        evaluation: PredictionEvaluation,
    ) -> PredictionEvaluation:

        record = PredictionEvaluationRecord(
            id=evaluation.id,
            prediction_id=evaluation.prediction_id,
            outcome_id=evaluation.outcome_id,
            correct=evaluation.correct,
            details=evaluation.details,
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> PredictionEvaluation | None:

        stmt = (
            select(PredictionEvaluationRecord)
            .where(
                PredictionEvaluationRecord.prediction_id
                == prediction_id,
            )
        )

        result = await self._session.execute(
            stmt,
        )

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return self._to_domain(record)

    @staticmethod
    def _to_domain(
        record: PredictionEvaluationRecord,
    ) -> PredictionEvaluation:

        return PredictionEvaluation(
            id=record.id,
            prediction_id=record.prediction_id,
            outcome_id=record.outcome_id,
            correct=record.correct,
            details=record.details,
        )