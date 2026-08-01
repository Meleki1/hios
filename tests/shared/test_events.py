from hios.shared.events import DomainEvent


def test_domain_event_creation():
    event = DomainEvent(
        event_type="case.created"
    )

    assert event.event_type == "case.created"
    assert event.event_id is not None
    assert event.occurred_at is not None