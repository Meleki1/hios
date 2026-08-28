from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.postgres.models.prediction import (
    PredictionRecord,
)


class PostgresPredictionRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        prediction: Prediction,
    ) -> Prediction:

        record = PredictionRecord(
            id=prediction.id,
            subject_id=prediction.subject_id,
            target=prediction.target,
            horizon_days=prediction.horizon_days,
            probability=prediction.probability,
            confidence=prediction.confidence,
            evidence=prediction.evidence,
            intent_score=prediction.intent_score.model_dump(
                mode="json",
            ),
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    async def get_by_id(
        self,
        prediction_id: str,
    ) -> Prediction | None:

        stmt = (
            select(PredictionRecord)
            .where(
                PredictionRecord.id == prediction_id,
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
        record: PredictionRecord,
    ) -> Prediction:

        from hios.capabilities.intelligence.models.intent_score import (
            IntentScore,
        )

        return Prediction(
            id=record.id,
            subject_id=record.subject_id,
            target=record.target,
            horizon_days=record.horizon_days,
            probability=record.probability,
            confidence=record.confidence,
            evidence=record.evidence,
            intent_score=IntentScore.model_validate(
                record.intent_score,
            ),
        )