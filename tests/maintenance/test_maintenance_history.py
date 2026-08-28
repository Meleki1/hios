from datetime import datetime, timezone

from hios.capabilities.maintenance.intelligence.maintenance_history import (
    MaintenanceHistorySignalExtractor,
)


def test_extracts_maintenance_history_from_timeline():

    created_at = datetime.now(timezone.utc)

    timeline = [
        type(
            "TimelineEntry",
            (),
            {
                "event_name": "message_received",
                "description": "Asked about mice",
                "subject_id": "household-1",
                "resource_id": "conversation-1",
                "resource_type": "conversation",
                "created_at": created_at,
            },
        )(),
        type(
            "TimelineEntry",
            (),
            {
                "event_name": "message_received",
                "description": "Asked about damp",
                "subject_id": "household-1",
                "resource_id": "conversation-2",
                "resource_type": "conversation",
                "created_at": created_at,
            },
        )(),
    ]

    extractor = MaintenanceHistorySignalExtractor()

    signals = extractor.extract(timeline)

    assert len(signals) == 2

    assert signals[0]["description"] == "Asked about mice"
    assert signals[1]["description"] == "Asked about damp"

    assert signals[0]["subject_id"] == "household-1"
    assert signals[1]["subject_id"] == "household-1"