from abc import ABC, abstractmethod

from hios.capabilities.outreach.contracts import (
    OutreachRequest,
    OutreachResult,
)


class OutreachChannelProvider(ABC):

    @abstractmethod
    async def send(
        self,
        *,
        request: OutreachRequest,
    ) -> OutreachResult:
        ...