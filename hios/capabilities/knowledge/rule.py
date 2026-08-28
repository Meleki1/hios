from hios.capabilities.knowledge.contract import (
    KnowledgeRequest,
    KnowledgeResult,
)
from hios.contracts.knowledge import KnowledgeCapability
from hios.intelligence.evaluators.base import ConditionEvaluator
from hios.intelligence.repositories.base import RuleRepository
from hios.runtime.context import RuntimeContext
from hios.intelligence.evidence.model import Evidence
from hios.intelligence.evidence.factory import EvidenceFactory


class RuleKnowledgeCapability(KnowledgeCapability):

    def __init__(
        self,
        repository: RuleRepository,
        evaluator: ConditionEvaluator,
        evidence_factory: EvidenceFactory,
    ) -> None:

        self._repository = repository
        self._evaluator = evaluator
        self._evidence_factory = evidence_factory

    async def reason(
        self,
        request: KnowledgeRequest,
        context: RuntimeContext,
    ) -> KnowledgeResult:
        rules = self._repository.load()

        facts: set[str] = set()
        evidence: list[Evidence] = []

        knowledge_input = request.observation

        if request.evidence:
            knowledge_input += "\n" + "\n".join(
                request.evidence
            )

        for rule in rules:
            if not rule.enabled:
                continue

            print("\n=== RULE EVALUATION ===")
            print("rule:", rule.name)
            print("condition:", rule.condition)
            print("knowledge_input:", knowledge_input)

            evaluation = self._evaluator.evaluate(
                rule.condition,
                knowledge_input,
            )
            print("matched:", evaluation.matched)
            print("evaluation:", evaluation)
            
            if evaluation.matched:
                facts.update(rule.facts)

                evidence.append(
                    self._evidence_factory.create(
                        rule=rule,
                        evaluation=evaluation,
                        observations=[
                            request.observation,
                            *request.evidence,
                        ],
                    )
                )
        print("\n=== FINAL FACTS ===")
        print(sorted(facts))

        print("\n=== FINAL EVIDENCE COUNT ===")
        print(len(evidence))
        
        return KnowledgeResult(
            facts=sorted(facts),
            evidence=evidence,
        )
        
            