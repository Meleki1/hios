from sqlalchemy import select

from hios.core.audit.models.audit_record import AuditRecord
from hios.core.audit.postgres.models.audit_record import AuditRecord as AuditRecordModel


class PostgresAuditRepository:

    def __init__(self, session):
        self._session = session

    async def save(
        self,
        audit_record: AuditRecord,
    ) -> AuditRecord:
        record = AuditRecordModel(
            id=audit_record.id,
            event_type=audit_record.event_type,
            event_name=audit_record.event_name,
            state=audit_record.state,
            description=audit_record.description,
            subject_id=audit_record.subject_id,
            resource_id=audit_record.resource_id,
            resource_type=audit_record.resource_type,
            occurred_at=audit_record.occurred_at,
            details=audit_record.details,
        )

        self._session.add(record)

        await self._session.commit()

        return audit_record

    async def get_by_id(
        self,
        audit_id: str,
    ) -> AuditRecord | None:

        result = await self._session.execute(
            select(AuditRecordModel).where(
                AuditRecordModel.id == audit_id,
            )
        )

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return AuditRecord(
            id=record.id,
            event_type=record.event_type,
            event_name=record.event_name,
            state=record.state,
            description=record.description,
            subject_id=record.subject_id,
            resource_id=record.resource_id,
            resource_type=record.resource_type,
            occurred_at=record.occurred_at,
            details=record.details,
        )

    async def get_all(self) -> list[AuditRecord]:

        result = await self._session.execute(
            select(AuditRecordModel)
        )

        records = result.scalars().all()

        return [
            AuditRecord(
                id=record.id,
                event_type=record.event_type,
                event_name=record.event_name,
                state=record.state,
                description=record.description,
                subject_id=record.subject_id,
                resource_id=record.resource_id,
                resource_type=record.resource_type,
                occurred_at=record.occurred_at,
                details=record.details,
            )
            for record in records
        ]

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[AuditRecord]:

        result = await self._session.execute(
            select(AuditRecordModel).where(
                AuditRecordModel.subject_id == subject_id,
            )
        )

        records = result.scalars().all()

        return [
            AuditRecord(
                id=record.id,
                event_type=record.event_type,
                event_name=record.event_name,
                state=record.state,
                description=record.description,
                subject_id=record.subject_id,
                resource_id=record.resource_id,
                resource_type=record.resource_type,
                occurred_at=record.occurred_at,
                details=record.details,
            )
            for record in records
        ]

    async def get_by_resource(
        self,
        resource_id: str,
    ) -> list[AuditRecord]:

        result = await self._session.execute(
            select(AuditRecordModel).where(
                AuditRecordModel.resource_id == resource_id,
            )
        )

        records = result.scalars().all()

        return [
            AuditRecord(
                id=record.id,
                event_type=record.event_type,
                event_name=record.event_name,
                state=record.state,
                description=record.description,
                subject_id=record.subject_id,
                resource_id=record.resource_id,
                resource_type=record.resource_type,
                occurred_at=record.occurred_at,
                details=record.details,
            )
            for record in records
        ]