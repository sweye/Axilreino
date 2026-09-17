import json
import subprocess
import tempfile
import time
from pathlib import Path

from .models import EvaluationResult


class PythonEvaluator:
    def __init__(self, timeout_seconds: int = 10):
        self.timeout_seconds = timeout_seconds

    def evaluate(
        self,
        solution_code: str,
        test_code: str,
    ) -> EvaluationResult:

        with tempfile.TemporaryDirectory(prefix="axilreino_eval_") as temp_dir:
            workspace = Path(temp_dir)

            solution_file = workspace / "solution.py"
            test_file = workspace / "test_solution.py"

            solution_file.write_text(solution_code, encoding="utf-8")
            test_file.write_text(test_code, encoding="utf-8")

            start = time.perf_counter()

            try:
                process = subprocess.run(
                    ["python", str(test_file)],
                    cwd=workspace,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                )

                duration = time.perf_counter() - start

                passed = process.returncode == 0

                return EvaluationResult(
                    passed=passed,
                    exit_code=process.returncode,
                    stdout=process.stdout,
                    stderr=process.stderr,
                    duration_seconds=duration,
                    error=None if passed else process.stderr,
                    metadata={
                        "language": "python",
                        "evaluator": "PythonEvaluator",
                    },
                )

            except subprocess.TimeoutExpired as exc:
                duration = time.perf_counter() - start

                return EvaluationResult(
                    passed=False,
                    exit_code=-1,
                    stdout=exc.stdout or "",
                    stderr=exc.stderr or "",
                    duration_seconds=duration,
                    error="Evaluation timed out.",
                    metadata={
                        "language": "python",
                        "evaluator": "PythonEvaluator",
                    },
                )
