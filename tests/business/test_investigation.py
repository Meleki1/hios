"""from hios.domain.business.investigation.models import InvestigationStatus
from hios.domain.business.investigation.models import Investigation

def test_start_investigation():
    investigation = Investigation.start()

    assert investigation.status == InvestigationStatus.NEW


def test_record_observation_changes_status():
    investigation = Investigation.start()

    updated = investigation.record_observation(
        make_observation()
    )

    assert updated.status == InvestigationStatus.ACTIVE

    assert len(updated.observations) == 1


def test_request_information():
    investigation = Investigation.start()

    updated = investigation.request_information(
        "Need clearer image"
    )

    assert (
        updated.status
        == InvestigationStatus.WAITING_FOR_INFORMATION
    )

    assert updated.blocker is not None

def test_complete():
    investigation = (
        Investigation.start()
        .record_observation(
            make_observation()
        )
    )

    completed = investigation.complete()

    assert (
        completed.status
        == InvestigationStatus.COMPLETED
    )

"""