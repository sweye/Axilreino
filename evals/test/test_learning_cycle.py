from evals.experiences import ExperienceStore
from evals.learning import LearningCycle
from rules import RuleStore


def test_learning_cycle_repairs_and_stores_verified_experience(tmp_path):
    solution = """
def largest_number(numbers):
    return numbers[0]
"""

    tests = """
from solution import largest_number

assert largest_number([1, 5, 3]) == 5
assert largest_number([-10, -2, -30]) == -2
assert largest_number([42]) == 42
"""

    experience_path = tmp_path / "experiences.json"
    rule_path = tmp_path / "rules.json"

    store = ExperienceStore(
        path=str(experience_path)
    )

    rule_store = RuleStore(
        path=str(rule_path)
    )

    cycle = LearningCycle(
        experience_store=store,
        rule_store=rule_store,
    )

    result = cycle.run(
        solution_code=solution,
        test_code=tests,
    )

    # The original solution must fail.
    assert result.initial_result.passed is False

    # The failure must be analyzed.
    assert result.analysis is not None
    assert result.analysis.failure_type == "assertion_failure"

    # A repair must be produced.
    assert result.repair is not None
    assert result.repair.repaired_code != solution

    # The repaired solution must pass verification.
    assert result.final_result is not None
    assert result.final_result.passed is True

    # The successful repair must become a learned experience.
    assert result.learned is True
    assert result.experience is not None
    assert result.experience["verified"] is True
    assert result.experience["result"] == "passed"

    # The experience must actually be persisted.
    assert store.count() == 1

    stored = store.get(
        result.experience["id"]
    )

    assert stored is not None
    assert stored["verified"] is True
    assert stored["original_code"] == solution
    assert stored["repaired_code"] == result.repair.repaired_code
    assert "return max(numbers)" in stored["repaired_code"]

    # The verified experience must become a reusable rule.
    assert result.rule_learned is True
    assert result.rule is not None
    assert result.rule["verified"] is True
    assert result.rule["confidence"] == 1.0
    assert "max()" in result.rule["rule"]

    # The rule must actually be persisted.
    assert rule_store.count() == 1

    stored_rule = rule_store.get(
        result.rule["id"]
    )

    assert stored_rule is not None
    assert stored_rule["verified"] is True
    assert stored_rule["evidence"] == [
        result.experience["id"]
    ]