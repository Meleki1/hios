from hios.capabilities.assistant.graph.state import (
    HomeAssistantState,
)
from hios.capabilities.assistant.llm.contract import (
    AssistantLLM,
)
from hios.capabilities.assistant.models.interaction_understanding import (
    InteractionUnderstanding,
)
import json
from pydantic import BaseModel


class InteractionUnderstandingOutput(BaseModel):
    explicit_intents: list[str]

class AssistantInteractionUnderstandingService:

    ALLOWED_INTENTS = {
        "asked_for_price",
        "requested_treatment",
        "reported_active_problem",
        "return_visits",
        "price_comparisons",
        "contractor_searches",
    }

    def __init__(
        self,
        *,
        llm: AssistantLLM,
    ) -> None:
        self._llm = llm

    async def understand(
        self,
        *,
        state: HomeAssistantState,
    ) -> InteractionUnderstanding:

        system_prompt = """
You are the interaction understanding component
of HIOS.

Analyze the user's message and identify only explicit
user intents.

Return a JSON object with this exact structure:

{
    "explicit_intents": []
}

Allowed intents:

- asked_for_price
- requested_treatment
- reported_active_problem
- return_visits
- price_comparisons
- contractor_searches

Rules:

- Only include intents explicitly expressed or clearly
  requested by the user.
- Do not invent facts.
- Do not infer an intent merely because it is possible.
- Do not include intents outside the allowed list.
- Return only valid JSON.
"""

        user_prompt = f"""
User message:

{state["message"]}
"""

        raw = await self._llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return self._parse_output(raw)

    def _parse_output(
            self,
            raw: str,
        ) -> InteractionUnderstanding:

            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Assistant LLM returned invalid JSON."
                ) from exc

            parsed = InteractionUnderstandingOutput.model_validate(
                data,
            )

            intents = [
                intent
                for intent in parsed.explicit_intents
                if intent in self.ALLOWED_INTENTS
            ]

            return InteractionUnderstanding(
                explicit_intents=intents,
            )
        