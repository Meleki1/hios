from hios.capabilities.execution.models.status import (
    ExecutionStatus,
)


def test_pending():

    assert (
        ExecutionStatus.PENDING
        == "pending"
    )


def test_running():

    assert (
        ExecutionStatus.RUNNING
        == "running"
    )


def test_success():

    assert (
        ExecutionStatus.SUCCESS
        == "success"
    )


def test_failed():

    assert (
        ExecutionStatus.FAILED
        == "failed"
    )


def test_cancelled():

    assert (
        ExecutionStatus.CANCELLED
        == "cancelled"
    )


def test_all_statuses_unique():

    statuses = list(
        ExecutionStatus
    )

    assert len(statuses) == len(set(statuses))