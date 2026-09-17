from evals.runner import FailureAnalyzer, PythonEvaluator
from evals.repair import Repairer


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


def test_failure_analyzer():
    solution = """
def largest_number(numbers):
    return numbers[0]
"""

    tests = """
from solution import largest_number

assert largest_number([1, 5, 3]) == 5
"""

    evaluator = PythonEvaluator()
    result = evaluator.evaluate(solution, tests)

    analyzer = FailureAnalyzer()
    analysis = analyzer.analyze(result)

    assert analysis is not None
    assert analysis.failure_type == "assertion_failure"
    assert analysis.language == "python"


def test_repair_attempt():
    solution = """
def largest_number(numbers):
    return numbers[0]
"""

    tests = """
from solution import largest_number

assert largest_number([1, 5, 3]) == 5
"""

    evaluator = PythonEvaluator()

    # First attempt
    result = evaluator.evaluate(solution, tests)

    assert result.passed is False

    # Analyze the failure
    analyzer = FailureAnalyzer()
    analysis = analyzer.analyze(result)

    assert analysis is not None

    # Create a repair attempt
    repairer = Repairer()
    repair = repairer.repair(
        code=solution,
        analysis=analysis,
        attempt_number=1,
    )

    assert repair is not None
    assert repair.original_code == solution
    assert repair.attempt_number == 1


def test_repair_can_produce_working_code():
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

    evaluator = PythonEvaluator()

    # First attempt fails
    result = evaluator.evaluate(solution, tests)

    assert result.passed is False

    # Analyze failure
    analyzer = FailureAnalyzer()
    analysis = analyzer.analyze(result)

    assert analysis is not None

    # Repair
    repairer = Repairer()

    repair = repairer.repair(
        code=solution,
        analysis=analysis,
        attempt_number=1,
    )

    assert repair is not None
    assert repair.repaired_code != solution

    # Verify repaired code
    repaired_result = evaluator.evaluate(
        repair.repaired_code,
        tests,
    )

    assert repaired_result.passed is True