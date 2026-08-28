from hios.capabilities.maintenance.intelligence.maintenance_pattern_detector import (
    MaintenancePatternDetector,
)


def test_detects_repeated_pest_pattern():

    signals = [
        {
            "description": "Asked about mice",
        },
        {
            "description": "Asked about wasps",
        },
        {
            "description": "Requested pest inspection",
        },
    ]

    detector = MaintenancePatternDetector()

    patterns = detector.detect(signals)

    assert len(patterns) == 1

    pattern = patterns[0]

    assert pattern.category == "pest"
    assert pattern.occurrences == 3

    assert pattern.descriptions == [
        "Asked about mice",
        "Asked about wasps",
        "Requested pest inspection",
    ]

    assert pattern.confidence == 1.0


def test_ignores_unrelated_history():

    signals = [
        {
            "description": "Bought a new sofa",
        },
        {
            "description": "Asked about energy prices",
        },
    ]

    detector = MaintenancePatternDetector()

    patterns = detector.detect(signals)

    assert patterns == []
