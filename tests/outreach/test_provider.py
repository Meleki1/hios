import pytest

from hios.capabilities.outreach.contracts import (
    OutreachRequest,
    OutreachResult,
)

from hios.capabilities.outreach.interfaces import (
    OutreachChannelProvider,
)

from hios.capabilities.outreach.models import (
    OutreachChannel,
    OutreachDeliveryStatus,
)


class FakeEmailProvider(OutreachChannelProvider):

    def __init__(self):
        self.calls: list[dict] = []

    async def send(
        self,
        *,
        request: OutreachRequest,
    ) -> OutreachResult:

        self.calls.append(
            {
                "request": request,
            }
        )

        return OutreachResult(
            status=OutreachDeliveryStatus.SENT,
            channel=OutreachChannel.EMAIL,
            recipient=request.recipient,
            message_id="fake-message-id",
        )


@pytest.mark.asyncio
async def test_email_provider_sends_outreach():

    provider = FakeEmailProvider()

    request = OutreachRequest(
        recipient="user@example.com",
        subject="Maintenance reminder",
        message="Your HVAC filter may need replacement.",
    )

    result = await provider.send(
        request=request,
    )

    assert result.status == (
        OutreachDeliveryStatus.SENT
    )

    assert result.channel == (
        OutreachChannel.EMAIL
    )

    assert result.recipient == (
        "user@example.com"
    )

    assert result.message_id == (
        "fake-message-id"
    )

    assert provider.calls == [
        {
            "request": request,
        }
    ]