import pytest

from hios.capabilities.outreach.channels.email import (
    EmailOutreachProvider,
    EmailTransport,
)

from hios.capabilities.outreach.contracts import (
    OutreachRequest,
)

from hios.capabilities.outreach.models import (
    OutreachChannel,
    OutreachDeliveryStatus,
)


class FailingEmailTransport(EmailTransport):

    async def send(
        self,
        *,
        recipient: str,
        subject: str,
        message: str,
    ) -> str:

        raise RuntimeError(
            "Email service unavailable."
        )

class FakeEmailTransport(EmailTransport):

    def __init__(
        self,
        *,
        message_id: str = "email-123",
    ):
        self.message_id = message_id
        self.calls: list[dict] = []

    async def send(
        self,
        *,
        recipient: str,
        subject: str,
        message: str,
    ) -> str:

        self.calls.append(
            {
                "recipient": recipient,
                "subject": subject,
                "message": message,
            }
        )

        return self.message_id


@pytest.mark.asyncio
async def test_email_provider_sends_through_transport():

    transport = FakeEmailTransport(
        message_id="email-123",
    )

    provider = EmailOutreachProvider(
        transport=transport,
    )

    request = OutreachRequest(
        recipient="user@example.com",
        subject="Maintenance reminder",
        message=(
            "Your HVAC filter may need replacement."
        ),
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

    assert result.message_id == "email-123"

    assert transport.calls == [
        {
            "recipient": "user@example.com",
            "subject": "Maintenance reminder",
            "message": (
                "Your HVAC filter may need replacement."
            ),
        }
    ]

@pytest.mark.asyncio
async def test_email_provider_returns_failed_result():

    provider = EmailOutreachProvider(
        transport=FailingEmailTransport(),
    )

    request = OutreachRequest(
        recipient="user@example.com",
        subject="Maintenance reminder",
        message="Your HVAC filter may need replacement.",
    )

    result = await provider.send(
        request=request,
    )

    assert result.status == (
        OutreachDeliveryStatus.FAILED
    )

    assert result.channel == (
        OutreachChannel.EMAIL
    )

    assert result.recipient == (
        "user@example.com"
    )

    assert result.message_id is None

    assert result.error == (
        "Email service unavailable."
    )