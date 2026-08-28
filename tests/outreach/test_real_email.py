import os

import pytest

from hios.capabilities.outreach.contracts import OutreachRequest
from hios.capabilities.outreach.models import OutreachChannel
from hios.capabilities.outreach.models import OutreachDeliveryStatus
from hios.runtime.context import RuntimeContext
from hios.capabilities.outreach.factory import build_outreach_capability
from hios.core.config import get_settings


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_email_delivery():
    settings = get_settings()

    recipient = settings.hios_test_email

    capability = build_outreach_capability(
        settings,
    )

    result = await capability.reason(
        OutreachRequest(
            recipient=recipient,
            subject="HIOS Outreach Integration Test",
            message=(
                "This is a real email sent by the "
                "HIOS outreach capability."
            ),
            channel=OutreachChannel.EMAIL,
        ),
        RuntimeContext(),
    )

    print("\n=== REAL EMAIL OUTREACH ===")
    print("status:", result.status)
    print("channel:", result.channel)
    print("recipient:", result.recipient)
    print("message_id:", result.message_id)
    print("error:", result.error)

    assert result.status == OutreachDeliveryStatus.SENT, (
        f"Email delivery failed: {result.error}"
    )

    assert result.recipient == recipient
    assert result.message_id is not None