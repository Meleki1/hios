from hios.capabilities.execution.models.action import Action, ActionType


class AssistantActionResponseBuilder:

    def build_photo_request(
        self,
        *,
        actions: list[Action] | None,
    ) -> str | None:

        if not actions:
            return None

        for action in actions:
 
            if action.action_type == ActionType.IMAGE_REQUEST:

                return (
                     "I'd like to understand the issue better. "
                     "Could you send me a photo of the affected area?"
                 )
        return None
