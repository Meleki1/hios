from hios.capabilities.learning.learner import Learner

from hios.capabilities.learning.models.lesson import Lesson
from hios.capabilities.learning.models.learning import Learning


class DefaultLearner(
    Learner,
):

    def learn(
        self,
        reflection,
    ) -> Learning:

        lessons = [
            Lesson(
                category=insight.category,
                description=insight.description,
            )
            for insight in reflection.insights
        ]

        return Learning(
            reflection=reflection,
            lessons=lessons,
            summary=reflection.summary,
            score=reflection.score,
        )