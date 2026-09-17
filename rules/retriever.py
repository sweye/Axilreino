from typing import Optional

from .store import RuleStore


class RuleRetriever:
    def __init__(self, rule_store: RuleStore):
        self.rule_store = rule_store

    def retrieve(
        self,
        language: Optional[str] = None,
        technology: Optional[str] = None,
        query: Optional[str] = None,
    ) -> list[dict]:
        rules = self.rule_store.all()

        matches = []

        for rule in rules:
            if not rule.get("verified", False):
                continue

            scope = rule.get("scope", {})

            if language is not None:
                if scope.get("language") != language:
                    continue

            if technology is not None:
                if scope.get("technology") != technology:
                    continue

            if query is not None:
                searchable_text = " ".join(
                    [
                        rule.get("trigger", ""),
                        rule.get("rule", ""),
                        rule.get("reason", ""),
                    ]
                ).lower()

                query_words = query.lower().split()

                if not any(word in searchable_text for word in query_words):
                    continue

            matches.append(rule)

        return matches