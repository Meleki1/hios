from hios.capabilities.outreach.contracts import (
    OutreachRequest,
    OutreachResult,
)

from hios.capabilities.outreach.models import (
    OutreachChannel,
    OutreachDeliveryStatus,
)


def test_outreach_request_defaults_to_email():
    request = OutreachRequest(
        recipient="user@example.com",
        subject="Maintenance reminder",
        message="Your HVAC filter may need replacement.",
    )

    assert request.recipient == "user@example.com"
    assert request.subject == "Maintenance reminder"
    assert request.message == (
        "Your HVAC filter may need replacement."
    )
    assert request.channel == OutreachChannel.EMAIL


def test_outreach_request_accepts_explicit_channel():
    request = OutreachRequest(
        recipient="user@example.com",
        subject="Maintenance reminder",
        message="Your HVAC filter may need replacement.",
        channel=OutreachChannel.EMAIL,
    )

    assert request.channel == OutreachChannel.EMAIL


def test_outreach_result_represents_success():
    result = OutreachResult(
        status=OutreachDeliveryStatus.SENT,
        channel=OutreachChannel.EMAIL,
        recipient="user@example.com",
        message_id="message-123",
    )

    assert result.status == OutreachDeliveryStatus.SENT
    assert result.channel == OutreachChannel.EMAIL
    assert result.recipient == "user@example.com"
    assert result.message_id == "message-123"
    assert result.error is None


def test_outreach_result_represents_failure():
    result = OutreachResult(
        status=OutreachDeliveryStatus.FAILED,
        channel=OutreachChannel.EMAIL,
        recipient="user@example.com",
        error="Provider unavailable.",
    )

    assert result.status == OutreachDeliveryStatus.FAILED
    assert result.channel == OutreachChannel.EMAIL
    assert result.recipient == "user@example.com"
    assert result.message_id is None
    assert result.error == "Provider unavailable."