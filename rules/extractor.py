from typing import Optional

from .models import Rule


class RuleExtractor:
    def extract(self, experience: dict) -> Optional[Rule]:
        if not experience.get("verified"):
            return None

        if experience.get("result") != "passed":
            return None

        failure = experience.get("failure", {})
        failure_type = failure.get("failure_type")
        language = failure.get("language")

        if (
            failure_type == "assertion_failure"
            and language == "python"
            and "largest_number" in experience.get("original_code", "")
            and "return max(numbers)" in experience.get("repaired_code", "")
        ):
            return Rule(
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
                evidence=[
                    experience.get("id", "unknown"),
                ],
                confidence=1.0,
                verified=True,
                regression_test="largest_number([1, 5, 3]) == 5",
            )

        return None