from hios.intelligence.evaluators.result import EvaluationResult
from hios.intelligence.conditions.condition import Condition
from hios.intelligence.evidence.model import Evidence
from hios.intelligence.conditions.operator import ConditionOperator
from hios.intelligence.evaluators.rule import RuleEvaluator

"""def test_create_evaluation_result():

    result = EvaluationResult(
        matched=True,
        confidence=1.0,
        matched_operands=["droppings"],
        unmatched_operands=[],
    )

    assert result.matched
    assert result.confidence == 1.0

def test_partial_match():

    result = EvaluationResult(
        matched=False,
        confidence=0.5,
        matched_operands=["droppings"],
        unmatched_operands=["scratching"],
    )

    assert result.confidence == 0.5
    assert result.matched_operands == ["droppings"]
    assert result.unmatched_operands == ["scratching"]

def test_no_match():

    result = EvaluationResult(
        matched=False,
        confidence=0.0,
        matched_operands=[],
        unmatched_operands=["droppings"],
    )

    assert not result.matched

def test_create_evidence():

    evaluation = EvaluationResult(
        matched=True,
        confidence=1.0,
        matched_operands=[
            "droppings",
        ],
        unmatched_operands=[],
    )

    evidence = Evidence(
        rule_id="rodent",
        rule_name="Rodent Evidence",
        evaluation=evaluation,
        observations=[
            "Droppings found.",
        ],
    )

    assert evidence.rule_id == "rodent"
    assert evidence.rule_name == "Rodent Evidence"
    assert evidence.evaluation == evaluation
    assert evidence.observations == [
        "Droppings found.",
    ]"""

def test_any_condition_matches():

    evaluator = RuleEvaluator()

    condition = Condition(
        operator=ConditionOperator.ANY,
        operands=[
            "droppings",
            "odor",
        ],
    )

    result = evaluator.evaluate(
        condition,
        "Droppings were found.",
    )

    assert result.matched
    assert result.score == 1.0
    assert result.matched_operands == [
        "droppings",
    ]
    assert result.unmatched_operands == [
        "odor",
    ]

def test_all_condition_matches():

    evaluator = RuleEvaluator()

    condition = Condition(
        operator=ConditionOperator.ALL,
        operands=[
            "droppings",
            "scratching",
        ],
    )

    result = evaluator.evaluate(
        condition,
        "Droppings and scratching detected.",
    )

    assert result.matched
    assert result.score == 1.0
    assert sorted(result.matched_operands) == [
        "droppings",
        "scratching",
    ]
    assert result.unmatched_operands == []

def test_all_condition_fails():

    evaluator = RuleEvaluator()

    condition = Condition(
        operator=ConditionOperator.ALL,
        operands=[
            "droppings",
            "scratching",
        ],
    )

    result = evaluator.evaluate(
        condition,
        "Droppings detected.",
    )

    assert not result.matched
    assert result.score == 0.5
    assert result.matched_operands == [
        "droppings",
    ]
    assert result.unmatched_operands == [
        "scratching",
    ]

def test_not_condition():

    evaluator = RuleEvaluator()

    condition = Condition(
        operator=ConditionOperator.NOT,
        operands=[
            "poison",
        ],
    )

    result = evaluator.evaluate(
        condition,
        "Droppings detected.",
    )

    assert result.matched
    assert result.score == 1.0

def test_nested_condition():

    evaluator = RuleEvaluator()

    condition = Condition(
        operator=ConditionOperator.ANY,
        operands=[
            Condition(
                operator=ConditionOperator.ALL,
                operands=[
                    "droppings",
                    "scratching",
                ],
            ),
            "odor",
        ],
    )

    result = evaluator.evaluate(
        condition,
        "Droppings and scratching detected.",
    )

    assert result.matched