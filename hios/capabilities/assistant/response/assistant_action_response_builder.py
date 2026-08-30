from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.capabilities.execution.models.action import Action, ActionType



from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.capabilities.execution.models.action import Action, ActionType


class AssistantActionResponseBuilder:

    def build(
        self,
        *,
        actions: list[Action] | None,
        safety_guidance=None,
        conversation_id: str | None = None,
    ) -> HomeAssistantResponse | None:

        if not actions:
            return None

        guidance = []

        if safety_guidance is not None:
            guidance = safety_guidance.guidance

        for action in actions:

            if action.action_type == ActionType.IMAGE_REQUEST:

                message_parts = []

                if guidance:
                    message_parts.append(
                        "Safety guidance:\n"
                        + "\n".join(
                            f"- {item}"
                            for item in guidance
                        )
                    )

                message_parts.append(
                    "I'd like to understand the issue better. "
                    "Could you send me a photo of the affected area?"
                )

                return HomeAssistantResponse(
                    message="\n\n".join(message_parts),
                    conversation_id=conversation_id,
                    capability="image_diagnosis",
                    metadata={
                        "action_type": (
                            ActionType.IMAGE_REQUEST.value
                        ),
                        "requires_user_input": True,
                    },
                )

        return None