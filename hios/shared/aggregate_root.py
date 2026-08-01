from __future__ import annotations

from typing import List

from pydantic import PrivateAttr

from hios.shared.entity import Entity
from hios.shared.events import DomainEvent


class AggregateRoot(Entity):
    """
    Base class for aggregate roots.

    Aggregate roots are responsible for enforcing
    business invariants and recording domain events.
    """

    _events: List[DomainEvent] = PrivateAttr(default_factory=list)

    def raise_event(self, event: DomainEvent) -> None:
        """
        Record a domain event.
        """
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        """
        Return all pending domain events.
        """
        return list(self._events)

    def clear_events(self) -> None:
        """
        Remove all recorded events.
        """
        self._events.clear()

    def evolve(self, **changes):
        """
        Return a new aggregate with the supplied state changes.
        """
        return self.model_copy(update=changes)