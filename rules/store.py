import json
from pathlib import Path
from typing import Optional

from .models import Rule


class RuleStore:
    def __init__(self, path: str = ".axilreino/rules.json"):
        self.path = Path(path)

    def _load(self) -> list[dict]:
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save(self, rules: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(
                rules,
                file,
                indent=2,
            )

    def add(self, rule: Rule) -> dict:
        rules = self._load()

        rule_data = rule.to_dict()

        if "id" not in rule_data:
            rule_data["id"] = f"rule-{len(rules) + 1:06d}"

        rules.append(rule_data)
        self._save(rules)

        return rule_data

    def get(self, rule_id: str) -> Optional[dict]:
        rules = self._load()

        for rule in rules:
            if rule.get("id") == rule_id:
                return rule

        return None

    def all(self) -> list[dict]:
        return self._load()

    def count(self) -> int:
        return len(self._load())