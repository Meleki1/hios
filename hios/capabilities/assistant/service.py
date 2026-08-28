from hios.capabilities.assistant.models.assistant_request import (
    HomeAssistantRequest,
)
from hios.capabilities.assistant.models.assistant_response import (
    HomeAssistantResponse,
)
from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher


class AssistantService:

    def __init__(
        self,
        graph,
        event_publisher: EventPublisher | None = None,
    ) -> None:

        self._graph = graph
        self._event_publisher = event_publisher

    async def execute(
        self,
        request: HomeAssistantRequest,
    ) -> HomeAssistantResponse:

        state = {
            "subject_id": request.subject_id,
            "home_id": request.home_id,
            "conversation_id": request.conversation_id,
            "message": request.message,
            "metadata": request.metadata,
        }

        result = await self._graph.ainvoke(
            state,
        )

        if self._event_publisher is not None:

            await self._event_publisher.publish(
                BaseEvent(
                    event_type="conversation",
                    event_name="message_received",
                    state="observed",
                    description=request.message,
                    subject_id=request.subject_id,
                    resource_id=request.conversation_id,
                    resource_type="conversation",
                )
            )

        return result["response"]