from dataclasses import dataclass
from typing import Optional

from .models import EvaluationResult


@dataclass
class FailureAnalysis:
    failure_type: str
    summary: str
    raw_error: str
    language: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "failure_type": self.failure_type,
            "summary": self.summary,
            "raw_error": self.raw_error,
            "language": self.language,
        }


class FailureAnalyzer:
    def analyze(self, result: EvaluationResult) -> Optional[FailureAnalysis]:
        if result.passed:
            return None

        error = result.stderr or result.error or ""

        if "AssertionError" in error:
            failure_type = "assertion_failure"
            summary = "The solution produced an unexpected result."

        elif "SyntaxError" in error:
            failure_type = "syntax_error"
            summary = "The solution contains invalid Python syntax."

        elif "ModuleNotFoundError" in error:
            failure_type = "missing_module"
            summary = "The solution attempted to import a module that was unavailable."

        elif "NameError" in error:
            failure_type = "undefined_name"
            summary = "The solution referenced a name that was not defined."

        elif "TypeError" in error:
            failure_type = "type_error"
            summary = "The solution used an incompatible type or function operation."

        elif "Evaluation timed out." in (result.error or ""):
            failure_type = "timeout"
            summary = "The solution did not finish within the allowed execution time."

        else:
            failure_type = "unknown"
            summary = "The solution failed for an unclassified reason."

        return FailureAnalysis(
            failure_type=failure_type,
            summary=summary,
            raw_error=error,
            language=result.metadata.get("language"),
        )