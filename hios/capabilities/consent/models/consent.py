from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ConsentPurpose(str, Enum):
    PREDICTION = "prediction"
    TIMELINE = "timeline"
    PERSONALIZATION = "personalization"
    BUSINESS_SHARING = "business_sharing"


@dataclass
class Consent:
    id: str
    subject_id: str
    purpose: ConsentPurpose
    granted: bool
    granted_at: datetime | None = None
    revoked_at: datetime | None = None