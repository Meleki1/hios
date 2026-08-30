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

        guidance = self._generator.generate(
            request.understanding,
        )

        previous_guidance = context.working_memory.get(
            "safety.communicated",
            [],
        )

        new_guidance = [
            item
            for item in guidance
            if item not in previous_guidance
        ]

        context.working_memory.put(
            "safety.communicated",
            list(
                dict.fromkeys(
                    previous_guidance + guidance
                )
            ),
        )

        return SafetyGuidanceResult(
            guidance=new_guidance,
        )