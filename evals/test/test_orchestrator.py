from evals import DeterministicBuilder, Orchestrator
from rules import Rule, RuleRetriever, RuleStore


def test_orchestrator_retrieves_knowledge_builds_and_evaluates(tmp_path):
    rule_store = RuleStore(
        path=str(tmp_path / "rules.json")
    )

    rule_store.add(
        Rule(
            scope={
                "language": "python",
                "technology": "python",
            },
            trigger="Need to find the largest value in a list.",
            rule="Use max() when the task requires the largest value.",
            reason=(
                "Returning the first element does not guarantee "
                "the largest value."
            ),
            evidence=["exp-000001"],
            confidence=1.0,
            verified=True,
        )
    )

    retriever = RuleRetriever(rule_store)

    orchestrator = Orchestrator(
        builder=DeterministicBuilder(),
        rule_retriever=retriever,
    )

    tests = """
from solution import largest_number

assert largest_number([1, 5, 3]) == 5
assert largest_number([-10, -2, -30]) == -2
assert largest_number([42]) == 42
"""

    result = orchestrator.run(
        task="Write a function that finds the largest number in a list.",
        language="python",
        technology="python",
        test_code=tests,
    )

    assert result.evaluation.passed is True

    assert len(result.knowledge.rules) == 1

    assert "Use max()" in result.knowledge.to_prompt()

    assert "return max(numbers)" in result.build.code