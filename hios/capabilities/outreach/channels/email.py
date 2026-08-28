from abc import ABC, abstractmethod
import asyncio
import smtplib
from email.message import EmailMessage
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



class EmailTransport(ABC):

    @abstractmethod
    async def send(
        self,
        *,
        recipient: str,
        subject: str,
        message: str,
    ) -> str:
        """
        Send an email and return its provider message ID.
        """
        ...





class EmailOutreachProvider(OutreachChannelProvider):

    def __init__(
        self,
        *,
        transport: EmailTransport,
    ) -> None:
        self._transport = transport

    async def send(
        self,
        *,
        request: OutreachRequest,
    ) -> OutreachResult:

        try:
            message_id = await self._transport.send(
                recipient=request.recipient,
                subject=request.subject,
                message=request.message,
            )

            return OutreachResult(
                status=OutreachDeliveryStatus.SENT,
                channel=OutreachChannel.EMAIL,
                recipient=request.recipient,
                message_id=message_id,
            )

        except Exception as exc:
            return OutreachResult(
                status=OutreachDeliveryStatus.FAILED,
                channel=OutreachChannel.EMAIL,
                recipient=request.recipient,
                error=str(exc),
            )