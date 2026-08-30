from collections.abc import Sequence

from .question import InvestigationQuestion
from .question_provider import InvestigationQuestionProvider


class DefaultInvestigationQuestionProvider(
    InvestigationQuestionProvider,
):

    def get_questions(
        self,
        *,
        hypothesis_name: str | None = None,
    ) -> Sequence[InvestigationQuestion]:

        if hypothesis_name == "Possible Rodent Activity":
            return [
                InvestigationQuestion(
                    key="rodent_droppings",
                    question=(
                        "Have you noticed droppings "
                        "or other signs around the area?"
                    ),
                    purpose=(
                        "Determine whether there is "
                        "physical evidence of rodent activity."
                    ),
                ),
                InvestigationQuestion(
                    key="rodent_odor",
                    question=(
                        "Have you noticed an unusual odor "
                        "around the area?"
                    ),
                    purpose=(
                        "Determine whether another common "
                        "sign of rodent activity is present."
                    ),
                ),
                InvestigationQuestion(
                    key="rodent_location",
                    question=(
                        "Where exactly are you noticing "
                        "the activity?"
                    ),
                    purpose=(
                        "Identify the location associated "
                        "with the suspected activity."
                    ),
                ),
            ]

        if hypothesis_name == "Rodent Infestation":
            return [
                InvestigationQuestion(
                    key="rodent_activity_extent",
                    question=(
                        "Which areas of the property "
                        "are showing signs of activity?"
                    ),
                    purpose=(
                        "Determine the extent of the "
                        "suspected infestation."
                    ),
                ),
            ]

        return [
            InvestigationQuestion(
                key="issue_location",
                question=(
                    "Where exactly are you noticing "
                    "the issue?"
                ),
                purpose=(
                    "Determine the affected location."
                ),
            ),
            InvestigationQuestion(
                key="issue_timing",
                question=(
                    "When did you first notice the issue?"
                ),
                purpose=(
                    "Determine when the issue began."
                ),
            ),
            InvestigationQuestion(
                key="issue_changes",
                question=(
                    "Has the issue changed or become "
                    "more frequent?"
                ),
                purpose=(
                    "Determine whether the issue is "
                    "changing over time."
                ),
            ),
        ]