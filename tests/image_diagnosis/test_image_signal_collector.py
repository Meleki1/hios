from datetime import datetime, timezone

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)
from hios.capabilities.image_diagnosis.services.image_signal_collector import (
    ImageSignalCollector,
)
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


def test_image_signal_collector_converts_pest_finding_to_signal():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    observed_at = datetime(
        2026,
        8,
        22,
        tzinfo=timezone.utc,
    )

    collector = ImageSignalCollector()

    signals = collector.collect(
        subject_id="household-1",
        home_id="home-1",
        diagnosis=diagnosis,
        observed_at=observed_at,
    )

    assert len(signals) == 1

    signal = signals[0]

    assert signal.type is SignalType.IMAGE
    assert signal.source is SignalSource.IMAGE

    assert signal.name == "possible_pest_evidence"
    assert signal.value == (
        "Possible rodent evidence."
    )

    assert signal.strength == 0.91
    assert signal.confidence == 0.91

    assert signal.observed_at == observed_at

    assert signal.metadata == {
        "category": "pest",
        "location": "kitchen",
        "subject_id": "household-1",
        "home_id": "home-1",
    }

def test_image_signal_collector_creates_signal_for_each_finding():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
            ImageFinding(
                category="moisture",
                description="Possible moisture damage.",
                confidence=0.76,
                location="kitchen",
            ),
        ],
        overall_confidence=0.84,
    )

    observed_at = datetime(
        2026,
        8,
        22,
        tzinfo=timezone.utc,
    )

    collector = ImageSignalCollector()

    signals = collector.collect(
        subject_id="household-1",
        home_id="home-1",
        diagnosis=diagnosis,
        observed_at=observed_at,
    )

    assert len(signals) == 2

    assert signals[0].type is SignalType.IMAGE
    assert signals[0].source is SignalSource.IMAGE
    assert signals[0].name == "possible_pest_evidence"

    assert signals[1].type is SignalType.IMAGE
    assert signals[1].source is SignalSource.IMAGE
    assert signals[1].name == "possible_moisture_evidence"

def test_image_signal_collector_returns_empty_list_for_empty_diagnosis():

    diagnosis = ImageDiagnosis(
        findings=[],
        overall_confidence=0.2,
    )

    collector = ImageSignalCollector()

    signals = collector.collect(
        subject_id="household-1",
        home_id="home-1",
        diagnosis=diagnosis,
        observed_at=datetime(
            2026,
            8,
            22,
            tzinfo=timezone.utc,
        ),
    )

    assert signals == []

def test_image_signal_collector_preserves_missing_location():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible pest evidence.",
                confidence=0.8,
            ),
        ],
        overall_confidence=0.8,
    )

    collector = ImageSignalCollector()

    signals = collector.collect(
        subject_id="household-1",
        home_id="home-1",
        diagnosis=diagnosis,
        observed_at=datetime(
            2026,
            8,
            22,
            tzinfo=timezone.utc,
        ),
    )

    assert len(signals) == 1
    assert "location" not in signals[0].metadata

def test_image_signal_collector_preserves_home_identity():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
            ),
        ],
        overall_confidence=0.91,
    )

    collector = ImageSignalCollector()

    signals = collector.collect(
        subject_id="household-42",
        home_id="home-99",
        diagnosis=diagnosis,
        observed_at=datetime(
            2026,
            8,
            22,
            tzinfo=timezone.utc,
        ),
    )

    signal = signals[0]

    assert signal.metadata["subject_id"] == "household-42"
    assert signal.metadata["home_id"] == "home-99"
