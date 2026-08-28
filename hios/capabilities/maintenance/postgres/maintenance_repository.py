from sqlalchemy import select

from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceStatus,
    MaintenanceType,
)
from hios.capabilities.maintenance.postgres.models.maintenance_record import (
    MaintenanceRecord,
)
from hios.capabilities.maintenance.repositories.maintenance_repository import (
    MaintenanceRepository,
)


class PostgresMaintenanceRepository(MaintenanceRepository):

    def __init__(self, session):
        self._session = session

    async def save(
        self,
        maintenance: Maintenance,
    ) -> Maintenance:

        record = MaintenanceRecord(
            id=maintenance.id,
            subject_id=maintenance.subject_id,
            home_id=maintenance.home_id,
            task=maintenance.task,
            maintenance_type=maintenance.maintenance_type.value,
            status=maintenance.status.value,
            scheduled_for=maintenance.scheduled_for,
            completed_at=maintenance.completed_at,
            created_at=maintenance.created_at,
            evidence=maintenance.evidence,
            extra_data=maintenance.metadata,
        )

        self._session.add(record)

        await self._session.commit()

        return maintenance

    async def get(
        self,
        maintenance_id: str,
    ) -> Maintenance | None:

        result = await self._session.execute(
            select(MaintenanceRecord).where(
                MaintenanceRecord.id == maintenance_id
            )
        )

        record = result.scalar_one_or_none()

        if record is None:
            return None

        return self._to_domain(record)

    async def get_all(
        self,
    ) -> list[Maintenance]:

        result = await self._session.execute(
            select(MaintenanceRecord)
        )

        records = result.scalars().all()

        return [
            self._to_domain(record)
            for record in records
        ]

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[Maintenance]:

        result = await self._session.execute(
            select(MaintenanceRecord).where(
                MaintenanceRecord.subject_id
                == subject_id
            )
        )

        records = result.scalars().all()

        return [
            self._to_domain(record)
            for record in records
        ]

    async def get_by_home(
        self,
        home_id: str,
    ) -> list[Maintenance]:

        result = await self._session.execute(
            select(MaintenanceRecord).where(
                MaintenanceRecord.home_id
                == home_id
            )
        )

        records = result.scalars().all()

        return [
            self._to_domain(record)
            for record in records
        ]

    @staticmethod
    def _to_domain(
        record: MaintenanceRecord,
    ) -> Maintenance:

        return Maintenance(
            id=record.id,
            subject_id=record.subject_id,
            home_id=record.home_id,
            task=record.task,
            maintenance_type=MaintenanceType(
                record.maintenance_type
            ),
            status=MaintenanceStatus(
                record.status
            ),
            scheduled_for=record.scheduled_for,
            completed_at=record.completed_at,
            created_at=record.created_at,
            evidence=record.evidence,
            metadata=record.extra_data,
        )