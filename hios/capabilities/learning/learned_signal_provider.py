from abc import ABC, abstractmethod

from hios.capabilities.learning.models.signal_performance import (
    SignalPerformance,
)


class LearnedSignalProvider(ABC):

    @abstractmethod
    async def get_signal_performance(
        self,
        target: str,
        signal_name: str,
    ) -> SignalPerformance | None:
        raise NotImplementedError