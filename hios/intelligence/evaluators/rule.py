from hios.intelligence.conditions.condition import Condition
from hios.intelligence.conditions.operator import ConditionOperator
from hios.intelligence.evaluators.base import ConditionEvaluator
from hios.intelligence.evaluators.result import EvaluationResult

class RuleEvaluator(ConditionEvaluator):


    """
Evaluates declarative rule conditions recursively.

Supports:

- ANY
- ALL
- NOT
- Nested conditions

Produces an EvaluationResult describing
whether the rule matched, its score,
and which operands matched.
"""

    def evaluate(
        self,
        condition: Condition,
        text: str,
    ) -> EvaluationResult:

        text = text.lower()

        match condition.operator:

            case ConditionOperator.ANY:

                results = [
                    self._evaluate_operand(
                        operand,
                        text,
                    )
                    for operand in condition.operands
                ]

                matched = any(r.matched for r in results)

                score = 1.0 if matched else 0.0

                matched_operands, unmatched_operands = self._merge_results(
                    results,
                )

                return self._result(
                    matched,
                    score,
                    matched_operands,
                    unmatched_operands,
                )

            case ConditionOperator.ALL:

                results = [
                    self._evaluate_operand(
                        operand,
                        text,
                    )
                    for operand in condition.operands
                ]

                matched = all(
                    result.matched
                    for result in results
                )

                
                matched_operands, unmatched_operands = self._merge_results(results)


                score = self._score_all(
                    matched_operands,
                    unmatched_operands,
                )

                return self._result(
                    matched,
                    score,
                    matched_operands,
                    unmatched_operands,
                )


            case ConditionOperator.NOT:

                result = self._evaluate_operand(
                    condition.operands[0],
                    text,
                )

                matched = not result.matched

                score = 1.0 if matched else 0.0

                return self._result(
                    matched,
                    score,
                    matched_operands=result.unmatched_operands,
                    unmatched_operands=result.matched_operands,
                )

        

    def _evaluate_operand(
        self,
        operand,
        text: str,
    ) -> EvaluationResult:

        if isinstance(operand, str):

            matched = operand.lower() in text

            return self._result(
                matched,
                1.0 if matched else 0.0,
                [operand] if matched else [],
                [] if matched else [operand],
            )

        return self.evaluate(
            operand,
            text,
        )

    def _result(
        self,
        matched: bool,
        score: float,
        matched_operands: list[str],
        unmatched_operands: list[str],
    ) -> EvaluationResult:

        return EvaluationResult(
            matched=matched,
            score=score,
            matched_operands=matched_operands,
            unmatched_operands=unmatched_operands,
        )

    def _merge_results(
        self,
        results: list[EvaluationResult],
    ) -> tuple[list[str], list[str]]:

        matched = [
            operand
            for result in results
            for operand in result.matched_operands
        ]

        unmatched = [
            operand
            for result in results
            for operand in result.unmatched_operands
        ]

        return matched, unmatched

    def _score_all(
        self,
        matched: list[str],
        unmatched: list[str],
    ) -> float:
        total = len(matched) + len(unmatched)
        return len(matched) / total if total else 0.0
