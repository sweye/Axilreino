from evals.builder import (
    BuildRequest,
    DeterministicBuilder,
)
from rules import KnowledgeContext


def test_deterministic_builder_builds_largest_number_solution():
    context = KnowledgeContext()

    request = BuildRequest(
        task="Write a function that finds the largest number in a list.",
        language="python",
        technology="python",
        knowledge=context,
    )

    builder = DeterministicBuilder()

    result = builder.build(request)

    assert "def largest_number(numbers):" in result.code
    assert "return max(numbers)" in result.code
    assert result.request is request