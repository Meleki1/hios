from hios.capabilities.risk.models.risk_assessment import (
    RiskAssessment,
)
from hios.capabilities.risk.models.risk_score import (
    RiskLevel,
    RiskScore,
)
from hios.capabilities.risk.risk_signal_adapter import (
    RiskSignalAdapter,
)
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


def test_risk_signal_adapter_converts_risk_assessment():

    assessment = RiskAssessment(
        risks=[
            RiskScore(
                risk_type="flood",
                score=70.0,
                level=RiskLevel.HIGH,
                confidence=0.9,
            ),
            RiskScore(
                risk_type="pest",
                score=40.0,
                level=RiskLevel.MEDIUM,
                confidence=1.0,
            ),
        ],
    )

    adapter = RiskSignalAdapter()

    signals = adapter.to_signals(
        assessment,
    )

    assert len(signals) == 2

    flood_signal = signals[0]

    assert flood_signal.type == (
        SignalType.ENVIRONMENTAL
    )

    assert flood_signal.source == (
        SignalSource.PROPERTY
    )

    assert flood_signal.name == "flood_risk"
    assert flood_signal.value == "high"
    assert flood_signal.strength == 0.7
    assert flood_signal.confidence == 0.9

    pest_signal = signals[1]

    assert pest_signal.name == "pest_risk"
    assert pest_signal.value == "medium"
    assert pest_signal.strength == 0.4