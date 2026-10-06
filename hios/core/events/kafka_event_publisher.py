from __future__ import annotations

import dataclasses
import json
import logging

from hios.core.events.base_event import BaseEvent

logger = logging.getLogger(__name__)


class KafkaEventPublisherAdapter:

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str = "hios.events",
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._subscribers = []
        self._producer = None

    def subscribe(self, subscriber) -> None:
        self._subscribers.append(subscriber)

    async def start(self) -> None:
        # Imported lazily so this module can be imported (and this
        # class referenced/tested) without aiokafka installed --
        # only actually *starting* it requires the dependency.
        from aiokafka import AIOKafkaProducer

        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            value_serializer=lambda value: json.dumps(
                value,
                default=str,
            ).encode("utf-8"),
        )
        await self._producer.start()

    async def stop(self) -> None:
        if self._producer is not None:
            await self._producer.stop()
            self._producer = None

    async def publish(self, event: BaseEvent) -> None:
        # In-process subscribers first, and unconditionally -- this
        # is the same delivery EventPublisher already guarantees,
        # so anything relying on it (timeline recording, outreach
        # dedup) is unaffected regardless of Kafka's health.
        for subscriber in self._subscribers:
            await subscriber.listen(event)

        if self._producer is None:
            logger.warning(
                "KafkaEventPublisherAdapter.publish() called "
                "before start() -- skipping Kafka delivery for "
                "event %s.",
                event.event_name,
            )
            return

        try:
            await self._producer.send_and_wait(
                self._topic,
                dataclasses.asdict(event),
            )
        except Exception:
            logger.exception(
                "Failed to publish event %s to Kafka topic %s -- "
                "in-process subscribers still ran normally.",
                event.event_name,
                self._topic,
            )
