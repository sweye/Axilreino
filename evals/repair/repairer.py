from dataclasses import dataclass
from typing import Optional

from evals.runner import FailureAnalysis


@dataclass
class RepairAttempt:
    original_code: str
    repaired_code: str
    analysis: FailureAnalysis
    attempt_number: int


class Repairer:
    def repair(
        self,
        code: str,
        analysis: FailureAnalysis,
        attempt_number: int = 1,
    ) -> Optional[RepairAttempt]:

        repaired_code = code

        # Deterministic repair used for testing the repair pipeline.
        # This will eventually be replaced by an AI-powered repairer.
        if analysis.failure_type == "assertion_failure":
            if "def largest_number(numbers):" in code:
                if "return numbers[0]" in code:
                    repaired_code = code.replace(
                        "return numbers[0]",
                        "return max(numbers)",
                    )

        return RepairAttempt(
            original_code=code,
            repaired_code=repaired_code,
            analysis=analysis,
            attempt_number=attempt_number,
        )