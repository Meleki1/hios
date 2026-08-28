import pytest
from hios.capabilities.home.schemas.home_creation import CreateHomeRequest
from hios.core.events.event_publisher import EventPublisher
from hios.capabilities.home.events.home_created import (
    HomeCreatedEvent,
)

class FakeSubscriber:

    def __init__(self):
        self.events = []

    async def listen(self, event):
        self.events.append(event)

@pytest.mark.asyncio
async def test_home_created_event_contains_home_id():

    home_id = "home-123"

    event = HomeCreatedEvent(
        home_id=home_id,
        subject_id="user-1"
    )
    assert event.subject_id == "user-1"
    assert event.resource_id == home_id
    assert event.event_type == "home"
    assert event.event_name == "home_created"
    assert event.state == "created"
    assert event.description == (
        "Home created successfully"
    )

@pytest.mark.asyncio
async def test_home_created_event_is_published():

    publisher = EventPublisher()
    subscriber = FakeSubscriber()

    publisher.subscribe(subscriber)

    event = HomeCreatedEvent(
        home_id="home-123",
        subject_id="user-1"
    )

    await publisher.publish(event)
    assert event.subject_id == "user-1"
    assert len(subscriber.events) == 1
    assert subscriber.events[0] is event

def test_home_created_event_contains_home_information():

    event = HomeCreatedEvent(
        home_id="home-123",
        subject_id="user-1"
    )
    assert event.subject_id == "user-1"
    assert event.resource_id == "home-123"
    assert event.state == "created"
    assert event.event_type == "home"

    assert event.event_name == (
        "home_created"
    )

    

   
    

    
    assert event.resource_id == "home-123"
    assert event.resource_type == "home"