from datetime import timezone
from hios.capabilities.timeline.models.timeline_entry import TimelineEntry

def test_timeline_entry_creates_with_required_fields():

    entry = TimelineEntry(
        subject_id="household-1",
        event_type="prediction",
        event_name="prediction_created",
        state="created",
        description="Prediction created",
        resource_id="prediction-1",
        resource_type="prediction",
    )

    assert entry.subject_id == "household-1"
    assert entry.event_type == "prediction"
    assert entry.event_name == "prediction_created"
    assert entry.state == "created"
    assert entry.description == "Prediction created"
    assert entry.resource_id == "prediction-1"
    assert entry.resource_type == "prediction"
    assert entry.created_at is not None
    assert entry.created_at.tzinfo == timezone.utc

def test_timeline_entry_allows_missing_resource():

    entry = TimelineEntry(
        subject_id="household-1",
        event_type="system",
        event_name="system_started",
        state="created",
        description="System started",
    )

    assert entry.resource_id is None
    assert entry.resource_type is None