from datetime import datetime

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class ImageSignalCollector:

    def collect(
        self,
        *,
        subject_id: str,
        home_id: str,
        diagnosis: ImageDiagnosis,
        observed_at: datetime,
    ) -> list[Signal]:

        signals: list[Signal] = []

        for finding in diagnosis.findings:
            metadata = {
                "category": finding.category,
                "subject_id": subject_id,
                "home_id": home_id,
            }

            if finding.location is not None:
                metadata["location"] = finding.location

            signals.append(
                Signal(
                    type=SignalType.IMAGE,
                    source=SignalSource.IMAGE,
                    name=self._build_signal_name(
                        finding.category,
                    ),
                    value=finding.description,
                    strength=finding.confidence,
                    confidence=finding.confidence,
                    observed_at=observed_at,
                    metadata=metadata,
                )
            )

        return signals

    @staticmethod
    def _build_signal_name(
        category: str,
    ) -> str:
        return f"possible_{category}_evidence"