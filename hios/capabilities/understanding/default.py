from .resolver import HypothesisResolver
from .models.hypothesis import Hypothesis
from .resolver import HypothesisResolver
from hios.capabilities.understanding.contract import UnderstandingRequest, UnderstandingResult


from hios.capabilities.knowledge.contract import KnowledgeResult


class RuleBasedHypothesisResolver(HypothesisResolver):

    def resolve(
        self,
        knowledge: KnowledgeResult,
    ) -> list[Hypothesis]:

        hypotheses = []

        if "High confidence infestation" in knowledge.facts:
            supporting_facts = [
                "High confidence infestation",
            ]

            if "Possible rodent activity" in knowledge.facts:
                supporting_facts.append(
                    "Possible rodent activity"
                )

            hypotheses.append(
                Hypothesis(
                    id="rodent",
                    name="Rodent Infestation",
                    description=(
                        "Evidence indicates a high-confidence "
                        "rodent infestation."
                    ),
                    confidence=0.9,
                    supporting_facts=supporting_facts,
                    evidence=knowledge.evidence,
                )
            )

        elif "Possible rodent activity" in knowledge.facts:
            hypotheses.append(
                Hypothesis(
                    id="rodent",
                    name="Possible Rodent Activity",
                    description=(
                        "Evidence suggests possible rodent activity."
                    ),
                    confidence=0.7,
                    supporting_facts=[
                        "Possible rodent activity",
                    ],
                    evidence=knowledge.evidence,
                )
            )

        return hypotheses



class DefaultUnderstandingStrategy:

    def __init__(
        self,
        resolver: HypothesisResolver,
    ) -> None:

        self._resolver = resolver

    def understand(
        self,
        request: UnderstandingRequest,
    ) -> UnderstandingResult:

        hypotheses = self._resolver.resolve(
            request.knowledge,
        )

        return UnderstandingResult(
            hypotheses=hypotheses,
        )