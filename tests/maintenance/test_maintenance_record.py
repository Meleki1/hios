from sqlalchemy import inspect

from hios.capabilities.maintenance.postgres.models.maintenance_record import (
    MaintenanceRecord,
)


def test_maintenance_record_has_expected_table():
    assert MaintenanceRecord.__tablename__ == (
        "maintenance_records"
    )


def test_maintenance_record_has_expected_columns():
    columns = {
        column.name
        for column in inspect(
            MaintenanceRecord
        ).columns
    }

    expected_columns = {
        "id",
        "subject_id",
        "home_id",
        "task",
        "maintenance_type",
        "status",
        "scheduled_for",
        "completed_at",
        "created_at",
        "evidence",
        "metadata",
    }

    assert columns == expected_columns