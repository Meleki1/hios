from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)
from hios.capabilities.risk.models.risk_assessment import (
    RiskAssessment,
)


class RiskSignalAdapter:

    def to_signals(
        self,
        assessment: RiskAssessment,
    ) -> list[Signal]:

        return [
            Signal(
                type=SignalType.ENVIRONMENTAL,
                source=SignalSource.PROPERTY,
                name=f"{risk.risk_type}_risk",
                value=risk.level.value,
                strength=risk.score / 100.0,
                confidence=risk.confidence,
            )
            for risk in assessment.risks
        ]