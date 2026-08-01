from hios.domain.business.investigation.blocker import (
    InvestigationBlocker,
)


def test_blocker():
    blocker = InvestigationBlocker(
        reason="Need clearer image."
    )

    assert blocker.reason == "Need clearer image."