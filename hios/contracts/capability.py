from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from hios.runtime.context import RuntimeContext


RequestT = TypeVar("RequestT")
ResultT = TypeVar("ResultT")


class Capability(
    ABC,
    Generic[RequestT, ResultT],
):
    async def execute(
        self,
        request: RequestT,
        context: RuntimeContext | None = None,
    ) -> ResultT:

        context = context or RuntimeContext()

        self.validate(request)

        await self.before_reason(
            request,
            context,
        )

        result = await self.reason(
            request,
            context,
        )

        return await self.after_reason(
            result,
            context,
        )

    def validate(
        self,
        request: RequestT,
    ) -> None:
        return

    async def before_reason(
        self,
        request: RequestT,
        context: RuntimeContext,
    ) -> None:
        """
        Hook before reasoning.
        """
        return

    async def after_reason(
        self,
        result: ResultT,
        context: RuntimeContext,
    ) -> ResultT:
        """
        Hook after reasoning.
        """
        return result

    @abstractmethod
    async def reason(
        self,
        request: RequestT,
        context: RuntimeContext,
    ) -> ResultT:
        """
        Execute this capability.
        """
        raise NotImplementedError