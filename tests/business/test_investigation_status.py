from hios.domain.business.investigation.enums import InvestigationStatus


def test_status_values():
    assert InvestigationStatus.NEW.value == "NEW"
    assert InvestigationStatus.COMPLETED.value == "COMPLETED"
    