from hios.capabilities.outreach.contracts import (
    OutreachRequest,
    OutreachResult,
)

from hios.capabilities.outreach.interfaces import (
    OutreachChannelProvider,
)

from hios.capabilities.outreach.models import (
    OutreachChannel,
)

from hios.contracts.capability import Capability
from hios.runtime.context import RuntimeContext


class DefaultOutreachCapability(Capability):

    def __init__(
        self,
        *,
        email_provider: OutreachChannelProvider,
    ) -> None:
        self._email_provider = email_provider

    async def reason(
        self,
        request: OutreachRequest,
        context: RuntimeContext,
    ) -> OutreachResult:

        if request.channel == OutreachChannel.EMAIL:
            return await self._email_provider.send(
                request=request,
            )

        raise ValueError(
            f"Unsupported outreach channel: "
            f"{request.channel}"
        )