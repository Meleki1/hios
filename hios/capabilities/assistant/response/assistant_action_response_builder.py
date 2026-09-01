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
        assessment=None,
        observation=None,
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

                summary = self._describe_suspected_activity(
                    assessment=assessment,
                    observation=observation,
                )

                if summary:
                    message_parts.append(summary)

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

    def _describe_suspected_activity(
        self,
        *,
        assessment,
        observation,
    ) -> str | None:

        if assessment is not None and assessment.pest_type:

            summary = (
                f"It looks like this may be {assessment.pest_type}."
            )

            if assessment.explanation:
                summary = f"{summary} {assessment.explanation}"

            return summary

        if observation is not None and observation.description:
            return (
                "It looks like you've reported possible pest "
                f"activity: {observation.description}"
            )

        return None