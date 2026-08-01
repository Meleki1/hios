from hios.shared.aggregate_root import AggregateRoot
from hios.shared.events import DomainEvent


class SampleAggregate(AggregateRoot):
    name: str


def test_raise_event():
    aggregate = SampleAggregate(name="Home")

    event = DomainEvent(
        event_type="created"
    )

    aggregate.raise_event(event)

    assert len(aggregate.collect_events()) == 1


def test_clear_events():
    aggregate = SampleAggregate(name="Home")

    aggregate.raise_event(
        DomainEvent(event_type="created")
    )

    aggregate.clear_events()

    assert len(aggregate.collect_events()) == 0