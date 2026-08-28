from hios.capabilities.consent.models.consent import (
    Consent,
    ConsentPurpose,
)
from hios.capabilities.consent.consent_service import ConsentService
from hios.core.events.consent_events import (
    ConsentGrantedEvent,
    ConsentRevokedEvent,
)
from hios.core.events.event_publisher import EventPublisher

class ConsentWorkflow:

    def __init__(
        self,
        consent_service: ConsentService,
        consent_repository,
        event_publisher: EventPublisher | None = None,
    ):
        self._consent_service = consent_service
        self._consent_repository = consent_repository
        self._event_publisher = event_publisher

    async def grant(
        self,
        subject_id: str,
        purpose: ConsentPurpose,
    ) -> Consent:
        consent = self._consent_service.grant(
            subject_id=subject_id,
            purpose=purpose,
        )

        saved_consent = await self._consent_repository.save(
            consent,
        )

        if self._event_publisher is not None:
            await self._event_publisher.publish(
                ConsentGrantedEvent(
                    consent_id=saved_consent.id,
                    subject_id=saved_consent.subject_id,
                    purpose=saved_consent.purpose,
                )
            )

        return saved_consent

    async def revoke(
        self,
        subject_id: str,
        purpose: ConsentPurpose,
    ) -> Consent | None:
        consent = await self._consent_repository.get(
            subject_id=subject_id,
            purpose=purpose,
        )

        if consent is None:
            return None

        revoked = self._consent_service.revoke(
            consent,
        )

        saved_consent = await self._consent_repository.save(
            revoked,
        )

        if self._event_publisher is not None:
            await self._event_publisher.publish(
                ConsentRevokedEvent(
                    consent_id=saved_consent.id,
                    subject_id=saved_consent.subject_id,
                    purpose=saved_consent.purpose,
                )
            )

        return saved_consent