from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestT = TypeVar("RequestT")
ResultT = TypeVar("ResultT")


class Capability(ABC, Generic[RequestT, ResultT]):
    """
    Base contract for every capability in HIOS.
    """

    @abstractmethod
    async def execute(
        self,
        request: RequestT,
    ) -> ResultT:
        """
        Execute the capability.
        """
        raise NotImplementedError