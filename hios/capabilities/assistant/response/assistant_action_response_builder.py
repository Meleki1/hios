from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.capabilities.execution.models.action import Action, ActionType



class AssistantActionResponseBuilder:
    def build(
        self,
        *,
        actions: list[Action] | None,
        conversation_id: str | None = None,
    ) -> HomeAssistantResponse | None:

        if not actions:
            return None

        for action in actions:
            if action.action_type == ActionType.IMAGE_REQUEST:
                return HomeAssistantResponse(
                    message=(
                        "I'd like to understand the issue better. "
                        "Could you send me a photo of the affected area?"
                    ),
                    conversation_id=conversation_id,
                    capability="image_diagnosis",
                    metadata={
                        "action_type": ActionType.IMAGE_REQUEST.value,
                        "requires_user_input": True,
                    },
                )

        return None