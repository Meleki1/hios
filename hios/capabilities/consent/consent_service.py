from datetime import datetime, timezone
from uuid import uuid4

from hios.capabilities.consent.models.consent import (
    Consent,
    ConsentPurpose,
)


class ConsentService:

    def grant(
        self,
        subject_id: str,
        purpose: ConsentPurpose,
    ) -> Consent:
        return Consent(
            id=str(uuid4()),
            subject_id=subject_id,
            purpose=purpose,
            granted=True,
            granted_at=datetime.now(timezone.utc),
        )

    def revoke(
        self,
        consent: Consent,
    ) -> Consent:
        consent.granted = False
        consent.revoked_at = datetime.now(timezone.utc)

        return consent