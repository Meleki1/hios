import pytest

from hios.capabilities.outreach.contracts import (
    OutreachRequest,
)

from hios.capabilities.outreach.default_capability import (
    DefaultOutreachCapability,
)

from hios.capabilities.outreach.models import (
    OutreachChannel,
    OutreachDeliveryStatus,
)

from hios.runtime.context import RuntimeContext
from hios.capabilities.outreach.channels.email import (
    EmailTransport, EmailOutreachProvider
)
import pytest

from hios.capabilities.outreach.default_capability import (
    DefaultOutreachCapability,
)
from hios.capabilities.outreach.contracts import OutreachResult
from hios.core.config import Settings
from hios.capabilities.outreach.factory import build_outreach_capability



class FakeEmailTransport(EmailTransport):

    def __init__(self):
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

        return "fake-message-123"

class FakeEmailProvider:

    def __init__(self):
        self.calls: list[dict] = []

    async def send(
        self,
        *,
        request: OutreachRequest,
    ):
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
async def test_outreach_capability_delegates_to_email_provider():

    provider = FakeEmailProvider()

    capability = DefaultOutreachCapability(
        email_provider=provider,
    )

    request = OutreachRequest(
        recipient="user@example.com",
        subject="Maintenance reminder",
        message=(
            "Your HVAC filter may need replacement."
        ),
        channel=OutreachChannel.EMAIL,
    )

    result = await capability.reason(
        request,
        RuntimeContext(),
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

@pytest.mark.asyncio
async def test_email_outreach_end_to_end():

    # ---------------------------------------------------------
    # TRANSPORT
    # ---------------------------------------------------------

    transport = FakeEmailTransport()

    # ---------------------------------------------------------
    # EMAIL PROVIDER
    # ---------------------------------------------------------

    provider = EmailOutreachProvider(
        transport=transport,
    )

    # ---------------------------------------------------------
    # OUTREACH CAPABILITY
    # ---------------------------------------------------------

    capability = DefaultOutreachCapability(
        email_provider=provider,
    )

    # ---------------------------------------------------------
    # REQUEST
    # ---------------------------------------------------------

    request = OutreachRequest(
        recipient="test@example.com",
        subject="Seasonal Pest Alert",
        message=(
            "Mosquito activity may increase during "
            "the rainy season. Check for standing "
            "water around your home."
        ),
        channel=OutreachChannel.EMAIL,
    )

    # ---------------------------------------------------------
    # EXECUTE
    # ---------------------------------------------------------

    result = await capability.reason(
        request,
        RuntimeContext(),
    )

    # ---------------------------------------------------------
    # DEBUG
    # ---------------------------------------------------------

    print("\n=== OUTREACH RESULT ===")
    print(result)

    print("\n=== EMAIL TRANSPORT CALLS ===")
    print(transport.calls)

    # ---------------------------------------------------------
    # RESULT ASSERTIONS
    # ---------------------------------------------------------

    assert result.status == (
        OutreachDeliveryStatus.SENT
    )

    assert result.channel == (
        OutreachChannel.EMAIL
    )

    assert result.recipient == (
        "test@example.com"
    )

    assert result.message_id == (
        "fake-message-123"
    )

    assert result.error is None

    # ---------------------------------------------------------
    # TRANSPORT ASSERTIONS
    # ---------------------------------------------------------

    assert transport.calls == [
        {
            "recipient": "test@example.com",
            "subject": "Seasonal Pest Alert",
            "message": (
                "Mosquito activity may increase during "
                "the rainy season. Check for standing "
                "water around your home."
            ),
        }
    ]

def test_build_outreach_capability():
    settings = Settings(
        database_url="postgresql://test",
        openai_api_key="test",
        email_host="smtp.example.com",
        email_port=587,
        email_username="test@example.com",
        email_password="password",
        email_from="test@example.com",
    )

    capability = build_outreach_capability(settings)

    assert isinstance(
        capability,
        DefaultOutreachCapability,
    )