from evals.runner import PythonEvaluator


def test_correct_solution_passes():
    solution = """
def largest_number(numbers):
    return max(numbers)
"""

    tests = """
from solution import largest_number

assert largest_number([1, 5, 3]) == 5
assert largest_number([-10, -2, -30]) == -2
assert largest_number([42]) == 42

print("3 tests passed")
"""

    evaluator = PythonEvaluator()

    result = evaluator.evaluate(solution, tests)

    assert result.passed is True
    assert result.exit_code == 0


def test_incorrect_solution_fails():
    solution = """
def largest_number(numbers):
    return numbers[0]
"""

    tests = """
from solution import largest_number

assert largest_number([1, 5, 3]) == 5
assert largest_number([-10, -2, -30]) == -2

print("tests passed")
"""

    evaluator = PythonEvaluator()

    result = evaluator.evaluate(solution, tests)

    assert result.passed is False
    assert result.exit_code != 0
