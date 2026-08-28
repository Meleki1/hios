from hios.shared.base import HIOSModel
from hios.intelligence.evaluators.result import EvaluationResult


class Evidence(HIOSModel):

    rule_id: str

    rule_name: str

    evaluation: EvaluationResult

    observations: list[str]