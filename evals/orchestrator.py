from dataclasses import dataclass

from evals.builder import BuildRequest, BuildResult, Builder
from evals.runner import EvaluationResult, PythonEvaluator
from rules import KnowledgeContext, RuleRetriever


@dataclass
class OrchestrationResult:
    build: BuildResult
    evaluation: EvaluationResult
    knowledge: KnowledgeContext


class Orchestrator:
    def __init__(
        self,
        builder: Builder,
        rule_retriever: RuleRetriever,
        evaluator: PythonEvaluator | None = None,
    ):
        self.builder = builder
        self.rule_retriever = rule_retriever
        self.evaluator = evaluator or PythonEvaluator()

    def run(
        self,
        task: str,
        language: str,
        technology: str,
        test_code: str,
    ) -> OrchestrationResult:

        rules = self.rule_retriever.retrieve(
            language=language,
            technology=technology,
            query=task,
        )

        knowledge = KnowledgeContext()

        for rule in rules:
            knowledge.add_rule(rule)

        request = BuildRequest(
            task=task,
            language=language,
            technology=technology,
            knowledge=knowledge,
        )

        build = self.builder.build(request)

        evaluation = self.evaluator.evaluate(
            solution_code=build.code,
            test_code=test_code,
        )

        return OrchestrationResult(
            build=build,
            evaluation=evaluation,
            knowledge=knowledge,
        )