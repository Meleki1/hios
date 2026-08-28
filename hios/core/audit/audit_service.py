from hios.core.audit.models.audit_record import AuditRecord


class AuditService:

    def __init__(
        self,
        audit_repository,
    ):
        self._audit_repository = audit_repository

    async def record(
        self,
        audit_record: AuditRecord,
    ) -> AuditRecord:

        return await self._audit_repository.save(
            audit_record,
        )

    async def get_by_id(
        self,
        audit_id: str,
    ) -> AuditRecord | None:

        return await self._audit_repository.get_by_id(
            audit_id,
        )

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[AuditRecord]:

        return await self._audit_repository.get_by_subject(
            subject_id,
        )

    async def get_by_resource(
        self,
        resource_id: str,
    ) -> list[AuditRecord]:

        return await self._audit_repository.get_by_resource(
            resource_id,
        )