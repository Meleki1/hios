from hios.core.audit.audit_service import AuditService
from hios.core.audit.models.audit_record import AuditRecord
from hios.core.events.base_event import BaseEvent


class AuditListener:

    def __init__(
        self,
        audit_service: AuditService,
    ):
        self._audit_service = audit_service

    async def listen(
        self,
        event: BaseEvent,
    ) -> None:

        audit_record = AuditRecord(
            event_type=event.event_type,
            event_name=event.event_name,
            state=event.state,
            description=event.description,
            subject_id=event.subject_id,
            resource_id=event.resource_id,
            resource_type=event.resource_type,
            occurred_at=event.created_at,
        )

        await self._audit_service.record(
            audit_record,
        )