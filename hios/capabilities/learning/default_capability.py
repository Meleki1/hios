from hios.runtime.context import RuntimeContext

from hios.capabilities.learning.contract import (
    LearningCapability,
)
from hios.capabilities.learning.contract import (
    LearningRequest,
    LearningResult,
)
from hios.capabilities.learning.learner import (
    Learner,
)


class DefaultLearningCapability(
    LearningCapability,
):

    def __init__(
        self,
        learner: Learner,
    ):

        self._learner = learner

    async def reason(
        self,
        request: LearningRequest,
        context: RuntimeContext,
    ) -> LearningResult:

        learning = self._learner.learn(
            request.reflection.reflection,
        )

        return LearningResult(
            learning=learning,
        )