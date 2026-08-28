from hios.capabilities.consent.models.consent import Consent
from hios.capabilities.consent.models.consent import (
    Consent,
    ConsentPurpose,
)
from sqlalchemy import select
from hios.capabilities.consent.postgres.models.consent_record import ConsentRecord


class PostgresConsentRepository:

    def __init__(self, session):
        self._session = session

    async def save(
        self,
        consent: Consent,
    ) -> Consent:
        from hios.capabilities.consent.postgres.models.consent_record import (
            ConsentRecord,
        )

        record = ConsentRecord(
            id=consent.id,
            subject_id=consent.subject_id,
            purpose=consent.purpose,
            granted=consent.granted,
            granted_at=consent.granted_at,
            revoked_at=consent.revoked_at,
        )

        self._session.add(record)

        await self._session.commit()

        return consent

    async def get_all(self) -> list[Consent]:
        from sqlalchemy import select

        from hios.capabilities.consent.postgres.models.consent_record import (
            ConsentRecord,
        )

        result = await self._session.execute(
            select(ConsentRecord)
        )

        records = result.scalars().all()

        return [
            Consent(
                id=record.id,
                subject_id=record.subject_id,
                purpose=record.purpose,
                granted=record.granted,
                granted_at=record.granted_at,
                revoked_at=record.revoked_at,
            )
            for record in records
        ]


    async def get(
        self,
        subject_id: str,
        purpose: ConsentPurpose,
    ) -> Consent | None:
        

        result = await self._session.execute(
            select(ConsentRecord).where(
                ConsentRecord.subject_id == subject_id,
                ConsentRecord.purpose == purpose,
            )
        )

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return Consent(
            id=record.id,
            subject_id=record.subject_id,
            purpose=record.purpose,
            granted=record.granted,
            granted_at=record.granted_at,
            revoked_at=record.revoked_at,
        )

