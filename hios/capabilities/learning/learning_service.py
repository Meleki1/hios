from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)


class LearningService:

    async def learn_from_prediction(
        self,
        prediction: Prediction,
        outcome: Outcome,
        evaluation: PredictionEvaluation,
    ) -> LearningRecord:

        signals = (
            prediction.intent_score.signals
        )

        lesson = (
            "Prediction was correct."
            if evaluation.correct
            else "Prediction was incorrect."
        )

        return LearningRecord(
            prediction_id=prediction.id,
            outcome_id=outcome.id,
            evaluation_id=evaluation.id,
            target=prediction.target,
            correct=evaluation.correct,
            signal_names=[
                signal.name
                for signal in signals
            ],
            signal_values=[
                signal.value
                for signal in signals
            ],
            signal_strengths=[
                signal.strength
                for signal in signals
            ],
            signal_confidences=[
                signal.confidence
                for signal in signals
            ],
            intent_score=(
                prediction.intent_score.score
            ),
            prediction_confidence=(
                prediction.confidence
            ),
            lesson=lesson,
        )