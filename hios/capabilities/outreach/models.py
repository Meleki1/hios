from enum import Enum


class OutreachChannel(str, Enum):
    EMAIL = "email"


class OutreachDeliveryStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"