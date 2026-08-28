from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.postgres.models.outcome import OutcomeRecord



class OutcomeRepository(ABC):

    @abstractmethod
    async def save(
        self,
        outcome: Outcome,
    ) -> Outcome:
        raise NotImplementedError

    @abstractmethod
    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> Outcome | None:
        raise NotImplementedError



class PostgresOutcomeRepository(OutcomeRepository):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def save(
        self,
        outcome: Outcome,
    ) -> Outcome:

        record = OutcomeRecord(
            id=outcome.id,
            prediction_id=outcome.prediction_id,
            subject_id=outcome.subject_id,
            target=outcome.target,
            occurred=outcome.occurred,
            observed_at=outcome.observed_at,
            details=outcome.details,
        )

        self._session.add(record)

        await self._session.commit()

        await self._session.refresh(record)

        return self._to_domain(record)

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> Outcome | None:

        stmt = (
            select(OutcomeRecord)
            .where(
                OutcomeRecord.prediction_id
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
        record: OutcomeRecord,
    ) -> Outcome:

        return Outcome(
            id=record.id,
            prediction_id=record.prediction_id,
            subject_id=record.subject_id,
            target=record.target,
            occurred=record.occurred,
            observed_at=record.observed_at,
            details=record.details,
        )