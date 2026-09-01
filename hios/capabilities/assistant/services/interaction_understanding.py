import json

from hios.capabilities.assistant.graph.state import (
    HomeAssistantState,
)
from hios.capabilities.assistant.llm.contract import (
    AssistantLLM,
)
from hios.capabilities.assistant.models.interaction_understanding import (
    InteractionUnderstanding,
    InteractionUnderstandingOutput
)
from langchain_core.messages import BaseMessage



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

Analyze the current user message in the context of
the conversation history.

Return a JSON object with exactly this structure:

{
  "interaction_type": "new_request",
  "explicit_intents": []
}

Interaction types:

- new_request
  The user is introducing a new request, problem,
  or observation.

- follow_up
  The user is continuing or adding information to
  an existing request.

- conversation_reference
  The user is asking about, referring to, or requesting
  information from something previously said in the
  conversation.

- general_question
  The user is asking a general question that does not
  represent a new home-related request.

Allowed intents:

- asked_for_price
- requested_treatment
- reported_active_problem
- return_visits
- price_comparisons
- contractor_searches

Rules:

- Use the conversation history to understand references
  such as "what did I say", "earlier", "that problem",
  "what did you recommend", etc.
- Do not treat words appearing in a conversation-reference
  question as a new observation.
- Only include intents explicitly expressed or clearly
  requested by the current user message.
- Do not extract intents from previous messages.
- Do not invent facts.
- Do not infer an intent merely because it is possible.
- Do not include intents outside the allowed list.
- Return only valid JSON.
"""

        user_prompt = f"""
Conversation history:

{self._format_conversation_history(
    state.get("messages", [])
)}

Current user message:

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
            interaction_type=parsed.interaction_type,
            explicit_intents=intents,
        )

    def _format_conversation_history(
        self,
        messages: list[BaseMessage],
    ) -> str:

        previous_messages = messages[:-1]

        if not previous_messages:
            return "(No previous conversation.)"

        lines = []

        for message in previous_messages:
            role = "User"

            if message.type == "assistant":
                role = "Assistant"

            lines.append(
                f"{role}: {message.content}"
            )

        return "\n".join(lines)