from hios.intelligence.evidence.model import Evidence
from hios.intelligence.evaluators.result import EvaluationResult
from hios.intelligence.models.rule import Rule


class EvidenceFactory:

    def create(
        self,
        rule: Rule,
        evaluation: EvaluationResult,
        observations: list[str],
    ) -> Evidence:

        return Evidence(
            rule_id=rule.id,
            rule_name=rule.name,
            evaluation=evaluation,
            observations=observations,
        )