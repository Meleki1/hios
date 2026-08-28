import pytest

from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceStatus,
    MaintenanceType,
)
from hios.capabilities.maintenance.postgres.maintenance_repository import (
    PostgresMaintenanceRepository,
)
from hios.capabilities.maintenance.repositories.maintenance_repository import (
    MaintenanceRepository,
)

class FakeMaintenanceRepository:

    def __init__(self, records=None):
        self.records = records or []

    async def create(self, maintenance):
        self.records.append(maintenance)
        return maintenance

    async def find_active_by_task(
        self,
        *,
        home_id,
        task,
    ):
        for record in self.records:
            if (
                record.home_id == home_id
                and record.task == task
                and record.status in (
                    MaintenanceStatus.PLANNED,
                    MaintenanceStatus.DUE,
                )
            ):
                return record

        return None

@pytest.mark.asyncio
async def test_maintenance_repository_saves_record(
    session,
):

    repository = PostgresMaintenanceRepository(
        session
    )

    maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Boiler service",
        maintenance_type=MaintenanceType.ROUTINE,
    )

    result = await repository.save(
        maintenance
    )

    assert result.id == maintenance.id
    assert result.subject_id == "household-1"
    assert result.home_id == "home-1"
    assert result.task == "Boiler service"

    assert (
        result.maintenance_type
        == MaintenanceType.ROUTINE
    )

    assert (
        result.status
        == MaintenanceStatus.PLANNED
    )

@pytest.mark.asyncio
async def test_maintenance_repository_gets_record(
    session,
):

    repository = PostgresMaintenanceRepository(
        session
    )

    maintenance = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=(
            MaintenanceType.USER_REQUESTED
        ),
    )

    await repository.save(maintenance)

    result = await repository.get(
        maintenance.id
    )

    assert result is not None
    assert result.id == maintenance.id
    assert result.task == "Pest inspection"
    assert (
        result.maintenance_type
        == MaintenanceType.USER_REQUESTED
    )

@pytest.mark.asyncio
async def test_maintenance_repository_gets_by_home(
    session,
):

    repository = PostgresMaintenanceRepository(
        session
    )

    first = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Boiler service",
        maintenance_type=MaintenanceType.ROUTINE,
    )

    second = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Gutter cleaning",
        maintenance_type=MaintenanceType.PREVENTIVE,
    )

    third = Maintenance(
        subject_id="household-1",
        home_id="home-2",
        task="Roof inspection",
        maintenance_type=MaintenanceType.ROUTINE,
    )

    await repository.save(first)
    await repository.save(second)
    await repository.save(third)

    records = await repository.get_by_home(
        "home-1"
    )

    assert len(records) == 2

    assert records[0].home_id == "home-1"
    assert records[1].home_id == "home-1"

@pytest.mark.asyncio
async def test_maintenance_repository_gets_by_subject(
    session,
):

    repository = PostgresMaintenanceRepository(
        session
    )

    first = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Boiler service",
        maintenance_type=MaintenanceType.ROUTINE,
    )

    second = Maintenance(
        subject_id="household-2",
        home_id="home-2",
        task="Roof inspection",
        maintenance_type=MaintenanceType.ROUTINE,
    )

    await repository.save(first)
    await repository.save(second)

    records = await repository.get_by_subject(
        "household-1"
    )

    assert len(records) == 1
    assert records[0].subject_id == "household-1"
    assert records[0].task == "Boiler service"

@pytest.mark.asyncio
async def test_maintenance_repository_get_returns_none(
    session,
):

    repository = PostgresMaintenanceRepository(
        session
    )

    result = await repository.get(
        "does-not-exist"
    )

    assert result is None



@pytest.mark.asyncio
async def test_repository_finds_active_maintenance_by_home_and_task():


    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.PLANNED,
    )
    repository = FakeMaintenanceRepository(
        records=[existing],
    )
    await repository.create(existing)

    result = await repository.find_active_by_task(
        home_id="home-1",
        task="Pest inspection",
    )

    assert result is existing

@pytest.mark.asyncio
async def test_repository_ignores_matching_task_on_different_home():


    existing = Maintenance(
        subject_id="household-1",
        home_id="home-2",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.PLANNED,
    )
    repository = FakeMaintenanceRepository(
        records=[existing],
    )
    await repository.create(existing)

    result = await repository.find_active_by_task(
        home_id="home-1",
        task="Pest inspection",
    )

    assert result is None

@pytest.mark.asyncio
async def test_repository_ignores_completed_maintenance():


    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.COMPLETED,
    )
    repository = FakeMaintenanceRepository(
        records=[existing],
    )
    await repository.create(existing)

    result = await repository.find_active_by_task(
        home_id="home-1",
        task="Pest inspection",
    )

    assert result is None

@pytest.mark.asyncio
async def test_repository_ignores_cancelled_maintenance():


    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.CANCELLED,
    )

    repository = FakeMaintenanceRepository(
        records=[existing],
    )

    await repository.create(existing)

    result = await repository.find_active_by_task(
        home_id="home-1",
        task="Pest inspection",
    )

    assert result is None

@pytest.mark.asyncio
async def test_repository_finds_due_maintenance():


    existing = Maintenance(
        subject_id="household-1",
        home_id="home-1",
        task="Pest inspection",
        maintenance_type=MaintenanceType.PREVENTIVE,
        status=MaintenanceStatus.DUE,
    )


    repository = FakeMaintenanceRepository(
        records=[existing],
    )

    await repository.create(existing)

    result = await repository.find_active_by_task(
        home_id="home-1",
        task="Pest inspection",
    )

    assert result is existing

@pytest.mark.asyncio
async def test_repository_returns_none_when_no_matching_maintenance_exists():

    

    repository = FakeMaintenanceRepository()

    result = await repository.find_active_by_task(
        home_id="home-1",
        task="Pest inspection",
    )

    assert result is None