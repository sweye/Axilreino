from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Rule:
    scope: dict
    trigger: str
    rule: str
    reason: str
    evidence: list[str] = field(default_factory=list)
    confidence: float = 0.0
    verified: bool = False
    last_verified: Optional[str] = None
    regression_test: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "scope": self.scope,
            "trigger": self.trigger,
            "rule": self.rule,
            "reason": self.reason,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "verified": self.verified,
            "last_verified": self.last_verified,
            "regression_test": self.regression_test,
        }