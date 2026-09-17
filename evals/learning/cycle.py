from dataclasses import dataclass
from typing import Optional

from evals.experiences import ExperienceStore
from evals.repair import RepairAttempt, Repairer
from evals.runner import (
    EvaluationResult,
    FailureAnalysis,
    FailureAnalyzer,
    PythonEvaluator,
)
from rules import RuleExtractor, RuleStore


@dataclass
class LearningCycleResult:
    initial_result: EvaluationResult
    analysis: Optional[FailureAnalysis]
    repair: Optional[RepairAttempt]
    final_result: Optional[EvaluationResult]
    experience: Optional[dict]
    rule: Optional[dict]

    @property
    def learned(self) -> bool:
        return self.experience is not None

    @property
    def rule_learned(self) -> bool:
        return self.rule is not None


class LearningCycle:
    def __init__(
        self,
        evaluator: Optional[PythonEvaluator] = None,
        analyzer: Optional[FailureAnalyzer] = None,
        repairer: Optional[Repairer] = None,
        experience_store: Optional[ExperienceStore] = None,
        rule_extractor: Optional[RuleExtractor] = None,
        rule_store: Optional[RuleStore] = None,
    ):
        self.evaluator = evaluator or PythonEvaluator()
        self.analyzer = analyzer or FailureAnalyzer()
        self.repairer = repairer or Repairer()
        self.experience_store = experience_store or ExperienceStore()
        self.rule_extractor = rule_extractor or RuleExtractor()
        self.rule_store = rule_store or RuleStore()

    def run(
        self,
        solution_code: str,
        test_code: str,
    ) -> LearningCycleResult:

        initial_result = self.evaluator.evaluate(
            solution_code,
            test_code,
        )

        if initial_result.passed:
            return LearningCycleResult(
                initial_result=initial_result,
                analysis=None,
                repair=None,
                final_result=initial_result,
                experience=None,
                rule=None,
            )

        analysis = self.analyzer.analyze(initial_result)

        if analysis is None:
            return LearningCycleResult(
                initial_result=initial_result,
                analysis=None,
                repair=None,
                final_result=None,
                experience=None,
                rule=None,
            )

        repair = self.repairer.repair(
            code=solution_code,
            analysis=analysis,
            attempt_number=1,
        )

        if repair is None:
            return LearningCycleResult(
                initial_result=initial_result,
                analysis=analysis,
                repair=None,
                final_result=None,
                experience=None,
                rule=None,
            )

        if repair.repaired_code == solution_code:
            return LearningCycleResult(
                initial_result=initial_result,
                analysis=analysis,
                repair=repair,
                final_result=None,
                experience=None,
                rule=None,
            )

        final_result = self.evaluator.evaluate(
            repair.repaired_code,
            test_code,
        )

        if not final_result.passed:
            return LearningCycleResult(
                initial_result=initial_result,
                analysis=analysis,
                repair=repair,
                final_result=final_result,
                experience=None,
                rule=None,
            )

        experience = self.experience_store.add(
            {
                "scope": {
                    "language": analysis.language,
                    "technology": analysis.language,
                },
                "failure": analysis.to_dict(),
                "original_code": solution_code,
                "repaired_code": repair.repaired_code,
                "result": "passed",
                "verified": True,
                "verification": {
                    "initial_exit_code": initial_result.exit_code,
                    "final_exit_code": final_result.exit_code,
                    "duration_seconds": final_result.duration_seconds,
                },
            }
        )

        rule = self.rule_extractor.extract(experience)

        stored_rule = None

        if rule is not None:
            stored_rule = self.rule_store.add(rule)

        return LearningCycleResult(
            initial_result=initial_result,
            analysis=analysis,
            repair=repair,
            final_result=final_result,
            experience=experience,
            rule=stored_rule,
        )