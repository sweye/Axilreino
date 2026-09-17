from dataclasses import dataclass
from typing import Protocol

from rules import KnowledgeContext


@dataclass
class BuildRequest:
    task: str
    language: str
    technology: str
    knowledge: KnowledgeContext


@dataclass
class BuildResult:
    code: str
    request: BuildRequest


class Builder(Protocol):
    def build(self, request: BuildRequest) -> BuildResult:
        ...


class DeterministicBuilder:
    """
    Temporary builder used to verify the orchestration architecture.

    This will eventually be replaced by an actual coding model.
    """

    def build(self, request: BuildRequest) -> BuildResult:
        if (
            request.language == "python"
            and "largest" in request.task.lower()
            and "list" in request.task.lower()
        ):
            code = """
def largest_number(numbers):
    return max(numbers)
""".strip()

            return BuildResult(
                code=code,
                request=request,
            )

        raise ValueError(
            "DeterministicBuilder does not support this task."
        )