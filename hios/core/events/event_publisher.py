from hios.core.events.base_event import BaseEvent


class EventPublisher:

    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber) -> None:
        self._subscribers.append(
            subscriber
        )

    async def publish(
        self,
        event: BaseEvent,
    ) -> None:

        for subscriber in self._subscribers:
            await subscriber.listen(event)