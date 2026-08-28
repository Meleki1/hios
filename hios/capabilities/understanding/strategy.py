from abc import ABC, abstractmethod

from .contract import UnderstandingRequest, UnderstandingResult



class UnderstandingStrategy(ABC):

    @abstractmethod
    def understand(
        self,
        request: UnderstandingRequest,
    ) -> UnderstandingResult:
        raise NotImplementedError