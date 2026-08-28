from hios.capabilities.consent.models.consent import ConsentPurpose
from hios.core.events.base_event import BaseEvent


class ConsentGrantedEvent(BaseEvent):

    def __init__(
        self,
        consent_id: str,
        subject_id: str,
        purpose: ConsentPurpose,
    ):
        super().__init__(
            event_type="consent",
            event_name="consent_granted",
            state="granted",
            description="Consent granted",
            resource_id=consent_id,
            resource_type="consent",
            subject_id=subject_id,
        )

        self.purpose = purpose

class ConsentRevokedEvent(BaseEvent):

    def __init__(
        self,
        consent_id: str,
        subject_id: str,
        purpose: ConsentPurpose,
    ):
        super().__init__(
            event_type="consent",
            event_name="consent_revoked",
            state="revoked",
            description="Consent revoked",
            resource_id=consent_id,
            resource_type="consent",
            subject_id=subject_id,
        )

        self.purpose = purpose