import json

from pydantic import ValidationError

from hios.capabilities.assistant.models.assistant_domain import (
    AssistantDomain,
)
from hios.capabilities.assistant.models.interaction_routing import (
    InteractionRoutingRequest,
    InteractionRoutingResult,
)
from hios.capabilities.assistant.router.interaction_router import (
    InteractionRouter,
)
from hios.capabilities.assistant.llm.contract import AssistantLLM


class DefaultInteractionRouter(
    InteractionRouter,
):

    def __init__(
        self,
        *,
        llm: AssistantLLM,
    ) -> None:
        self._llm = llm

    async def route(
        self,
        request: InteractionRoutingRequest,
    ) -> InteractionRoutingResult:

        system_prompt = """
You are the HIOS interaction router.

Your only responsibility is to determine which HIOS
domain should handle the user's current interaction.

Available domains:

- conversation
- home
- pest_control
- unsupported

Routing rules:

1. Choose exactly one domain.
2. Classify based on the meaning and purpose of the
   user's interaction, not exact keywords.
3. Reports of possible pest evidence belong to
   pest_control even when the user does not name
   the pest.
4. Examples of pest evidence include scratching,
   droppings, gnaw marks, unusual pest-related odors,
   nests, insects, or sightings.
5. A home problem that is not specifically pest-related
   belongs to home.
6. Casual conversation belongs to conversation.
7. Requests outside HIOS capabilities belong to
   unsupported.
8. If an image is present, use that fact when deciding
   the domain.
9. Previous domain context may be used to understand
   short follow-up messages.
10. Do not solve the user's problem.
11. Do not provide advice.
12. Return ONLY valid JSON.

Required JSON format:

{
  "domain": "conversation | home | pest_control | unsupported",
  "confidence": 0.0,
  "reason": "brief explanation"
}
"""

        user_prompt = f"""
Current user message:
{request.message}

Image present:
{request.has_image}

Previous domain:
{request.previous_domain}
"""

        raw = await self._llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        try:
            data = json.loads(raw)

            result = InteractionRoutingResult.model_validate(
                data
            )

            return result

        except (
            json.JSONDecodeError,
            ValidationError,
            TypeError,
        ):
            return InteractionRoutingResult(
                domain=AssistantDomain.CONVERSATION,
                confidence=0.0,
                reason="Routing model returned an invalid result.",
            )