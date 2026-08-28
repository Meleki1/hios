from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)
from hios.capabilities.intelligence.prediction_evaluator import (
    PredictionEvaluator,
)


class BasicPredictionEvaluator(PredictionEvaluator):

    async def evaluate(
        self,
        prediction: Prediction,
        outcome: Outcome,
    ) -> PredictionEvaluation:

        correct = (
            prediction.id == outcome.prediction_id
            and prediction.target == outcome.target
            and outcome.occurred is True
        )

        return PredictionEvaluation(
            prediction_id=prediction.id,
            outcome_id=outcome.id,
            correct=correct,
        )