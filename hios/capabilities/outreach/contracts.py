from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from hios.capabilities.outreach.models import (
    OutreachChannel,
    OutreachDeliveryStatus,
)


class OutreachRequest(CapabilityRequest):
    recipient: str
    subject: str
    message: str
    channel: OutreachChannel = OutreachChannel.EMAIL


class OutreachResult(CapabilityResult):
    status: OutreachDeliveryStatus
    channel: OutreachChannel
    recipient: str
    message_id: str | None = None
    error: str | None = None