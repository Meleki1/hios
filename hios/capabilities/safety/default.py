from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)

class DefaultSafetyGuidanceGenerator:

    def generate(
        self,
        understanding: UnderstandingResult,
    ) -> list[str]:
        guidance: list[str] = []

        for hypothesis in understanding.hypotheses:

            if hypothesis.name == "Possible Rodent Activity":
                guidance.extend(
                    [
                        (
                            "Avoid handling suspected rodent "
                            "droppings or contaminated material "
                            "with bare hands."
                        ),
                        (
                            "Keep the affected area clear while "
                            "the source of the activity is being "
                            "investigated."
                        ),
                    ]
                )

            elif hypothesis.name == "Rodent Infestation":
                guidance.extend(
                    [
                        (
                            "Avoid direct contact with rodents "
                            "or suspected contaminated material."
                        ),
                        (
                            "Keep children and pets away from "
                            "areas showing signs of infestation."
                        ),
                    ]
                )

        return list(dict.fromkeys(guidance))