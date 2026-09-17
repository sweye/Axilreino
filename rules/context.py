from dataclasses import dataclass, field


@dataclass
class KnowledgeContext:
    rules: list[dict] = field(default_factory=list)

    def add_rule(self, rule: dict) -> None:
        if rule.get("verified", False):
            self.rules.append(rule)

    def is_empty(self) -> bool:
        return len(self.rules) == 0

    def to_dict(self) -> dict:
        return {
            "rules": self.rules,
        }

    def to_prompt(self) -> str:
        if self.is_empty():
            return "No verified guidance is available."

        sections = ["Known verified guidance:"]

        for rule in self.rules:
            scope = rule.get("scope", {})
            language = scope.get("language", "unknown")

            sections.append(
                f"\n[{language}]"
            )

            sections.append(
                f"Rule: {rule.get('rule', '')}"
            )

            sections.append(
                f"Reason: {rule.get('reason', '')}"
            )

            evidence = rule.get("evidence", [])

            if evidence:
                sections.append(
                    f"Evidence: {', '.join(evidence)}"
                )

            sections.append(
                f"Verified: {'yes' if rule.get('verified') else 'no'}"
            )

        return "\n".join(sections)