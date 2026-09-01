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
  "interaction_type": "<one of the allowed interaction types>",
  "explicit_intents": []
}

Interaction types:

- new_request
  The user is introducing a new home-related request,
  problem, observation, or task.

- follow_up
  The user is continuing an existing home-related request
  by adding new information or asking for clarification
  about the active issue.

- conversation_reference
  The user is asking about, referring to, or requesting
  information from something previously said in the
  conversation.

- general_question
  The user is greeting, making casual conversation, or
  asking
  a general question that does not introduce or continue
  a home-related request.

Important classification rules:

- A greeting such as "Hello", "Hi", "Hey", or "Good morning"
  is always general_question.
- A short conversational message with no request or
  home-related issue is general_question.
- Do not classify a message as new_request merely because
  it is a new user message.
- new_request requires an actual new request, problem,
  observation, or task.

Allowed intents:

- asked_for_price
- requested_treatment
- reported_active_problem
- return_visits
- price_comparisons
- contractor_searches

Examples:

User: "Hello"
Output:
{
  "interaction_type": "general_question",
  "explicit_intents": []
}

User: "Hi, how are you?"
Output:
{
  "interaction_type": "general_question",
  "explicit_intents": []
}

User: "I saw scratching in my kitchen"
Output:
{
  "interaction_type": "new_request",
  "explicit_intents": ["reported_active_problem"]
}

User: "I also found droppings"
Output:
{
  "interaction_type": "follow_up",
  "explicit_intents": ["reported_active_problem"]
}

User: "Where did I say I saw scratching?"
Output:
{
  "interaction_type": "conversation_reference",
  "explicit_intents": []
}

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

            if message.type == "ai":
                role = "Assistant"

            lines.append(
                f"{role}: {message.content}"
            )

        return "\n".join(lines)