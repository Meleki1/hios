from datetime import datetime, timezone

from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceStatus,
    MaintenanceType,
)


def test_maintenance_has_expected_defaults():

    maintenance = Maintenance(
        subject_id="subject-1",
        home_id="home-1",
        task="Boiler service",
        maintenance_type=MaintenanceType.ROUTINE,
    )

    assert maintenance.subject_id == "subject-1"
    assert maintenance.home_id == "home-1"
    assert maintenance.task == "Boiler service"

    assert (
        maintenance.maintenance_type
        == MaintenanceType.ROUTINE
    )

    assert (
        maintenance.status
        == MaintenanceStatus.PLANNED
    )

    assert maintenance.completed_at is None
    assert maintenance.evidence == []
    assert maintenance.metadata == {}


def test_maintenance_can_be_scheduled():

    scheduled_for = datetime.now(timezone.utc)

    maintenance = Maintenance(
        subject_id="subject-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.USER_REQUESTED,
        scheduled_for=scheduled_for,
    )

    assert maintenance.scheduled_for == scheduled_for


def test_maintenance_can_be_completed():

    completed_at = datetime.now(timezone.utc)

    maintenance = Maintenance(
        subject_id="subject-1",
        home_id="home-1",
        task="Gutter cleaning",
        maintenance_type=MaintenanceType.ROUTINE,
        status=MaintenanceStatus.COMPLETED,
        completed_at=completed_at,
    )

    assert (
        maintenance.status
        == MaintenanceStatus.COMPLETED
    )

    assert maintenance.completed_at == completed_at