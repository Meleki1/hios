from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.postgres.models.prediction import (
    PredictionRecord,
)
from hios.capabilities.intelligence.postgres.models.outcome import (
    OutcomeRecord,
)
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
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
            created_at=prediction.created_at,
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

    async def list_due_for_feedback(
        self,
        as_of: datetime | None = None,
    ) -> list[Prediction]:
        """
        Predictions whose horizon_days window has elapsed and that
        have no recorded Outcome yet -- i.e. due for the "did this
        actually happen?" feedback check-in (see
        PredictionFeedbackService and the intelligence-pipeline-
        wiring-audit project doc's prediction feedback loop
        section).

        The "no outcome yet" half is a straightforward anti-join.
        The "horizon has elapsed" half deliberately isn't pushed
        into the SQL as `created_at + horizon_days days <= as_of`:
        that arithmetic is dialect-specific (interval syntax differs
        across Postgres/SQLite/etc, and this couldn't be exercised
        against a real database in the environment this was written
        in), and the candidate set -- predictions with no outcome at
        all -- is naturally small and self-limiting in practice
        (every check-in sent should eventually produce an outcome
        that removes its prediction from this set), so filtering the
        elapsed-horizon condition in Python is both safer and just
        as correct.
        """

        as_of = as_of or datetime.now(timezone.utc)

        stmt = select(PredictionRecord).where(
            ~PredictionRecord.id.in_(
                select(OutcomeRecord.prediction_id),
            ),
        )

        result = await self._session.execute(stmt)

        due = []

        for record in result.scalars().all():

            created_at = record.created_at

            if created_at.tzinfo is None:
                created_at = created_at.replace(
                    tzinfo=timezone.utc,
                )

            horizon_elapsed_at = created_at + timedelta(
                days=record.horizon_days,
            )

            if horizon_elapsed_at <= as_of:
                due.append(self._to_domain(record))

        return due


    @staticmethod
    def _to_domain(
        record: PredictionRecord,
    ) -> Prediction:

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
            created_at=(
                record.created_at
                or datetime.now(timezone.utc)
            ),
        )