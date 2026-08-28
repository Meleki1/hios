from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.prediction_engine import (
    PredictionEngine,
)


class BasicPredictionEngine(PredictionEngine):

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score: IntentScore,
    ) -> Prediction:

        return Prediction(
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
            probability=None,
            confidence=intent_score.confidence,
            evidence=[
                signal.value
                for signal in intent_score.signals
            ],
        )