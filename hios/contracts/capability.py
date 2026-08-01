from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from hios.runtime.context import RuntimeContext

RequestT = TypeVar("RequestT")
ResultT = TypeVar("ResultT")


class Capability(
    ABC,
    Generic[RequestT, ResultT],
):

    @abstractmethod
    async def execute(
        self,
        request: RequestT,
        context: RuntimeContext,
    ) -> ResultT:
        """
        Execute this capability.
        """
        raise NotImplementedError