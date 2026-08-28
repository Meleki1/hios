from hios.capabilities.outcome.models.status import OutcomeStatus

from hios.capabilities.reflection.models.insight import Insight
from hios.capabilities.reflection.models.reflection import Reflection

from hios.capabilities.reflection.reflector import Reflector


class DefaultReflector(
    Reflector,
):

    def reflect(
        self,
        outcome,
    ) -> Reflection:

        if outcome.status == OutcomeStatus.SUCCESS:

            return Reflection(
                outcome=outcome,
                insights=[
                    Insight(
                        category="success",
                        description="Execution completed successfully.",
                    )
                ],
                summary="Execution completed successfully.",
                score=1.0,
            )

        return Reflection(
            outcome=outcome,
            insights=[
                Insight(
                    category="failure",
                    description="Execution failed.",
                )
            ],
            summary="Execution failed.",
            score=0.0,
        )