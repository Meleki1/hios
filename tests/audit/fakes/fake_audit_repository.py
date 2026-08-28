from hios.core.audit.models.audit_record import AuditRecord


class FakeAuditRepository:

    def __init__(self):
        self.records: list[AuditRecord] = []

    async def save(
        self,
        audit_record: AuditRecord,
    ) -> AuditRecord:
        self.records.append(audit_record)
        return audit_record

    async def get_by_id(
        self,
        audit_id: str,
    ) -> AuditRecord | None:

        for record in self.records:
            if record.id == audit_id:
                return record

        return None

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[AuditRecord]:

        return [
            record
            for record in self.records
            if record.subject_id == subject_id
        ]

    async def get_by_resource(
        self,
        resource_id: str,
    ) -> list[AuditRecord]:

        return [
            record
            for record in self.records
            if record.resource_id == resource_id
        ]