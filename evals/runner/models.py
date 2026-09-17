from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EvaluationResult:
    passed: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    error: Optional[str] = None
    tests_passed: Optional[int] = None
    tests_failed: Optional[int] = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_seconds": self.duration_seconds,
            "error": self.error,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "metadata": self.metadata,
        }
