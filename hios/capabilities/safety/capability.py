from abc import ABC

from hios.contracts.capability import Capability
from hios.runtime.context import RuntimeContext

from hios.capabilities.safety.contract.request import (
    SafetyGuidanceRequest,
)
from hios.capabilities.safety.contract.result import (
    SafetyGuidanceResult,
)


class SafetyGuidanceCapability(
    Capability[
        SafetyGuidanceRequest,
        SafetyGuidanceResult,
    ],
    ABC,
):
    pass

class DefaultSafetyGuidanceCapability(
    SafetyGuidanceCapability,
):
    def __init__(
        self,
        generator,
    ) -> None:
        self._generator = generator

    async def reason(
        self,
        request: SafetyGuidanceRequest,
        context: RuntimeContext,
    ) -> SafetyGuidanceResult:

        guidance = await self._generator.generate(
            request.understanding,
        )

        new_guidance = [
            item for item in guidance
            if item not in request.previously_communicated_guidance
        ]

        return SafetyGuidanceResult(
            guidance=new_guidance,
        )