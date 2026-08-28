from hios.runtime.context import RuntimeContext

from hios.capabilities.reflection.contract import (
    ReflectionCapability,
)
from hios.capabilities.reflection.contract import (
    ReflectionRequest,
    ReflectionResult,
)
from hios.capabilities.reflection.reflector import (
    Reflector,
)


class DefaultReflectionCapability(
    ReflectionCapability,
):

    def __init__(
        self,
        reflector: Reflector,
    ):

        self._reflector = reflector

    async def reason(
        self,
        request: ReflectionRequest,
        context: RuntimeContext,
    ) -> ReflectionResult:

        reflection = self._reflector.reflect(
            request.outcome.outcome,
        )

        return ReflectionResult(
            reflection=reflection,
        )