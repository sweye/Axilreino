import json
from pathlib import Path
from typing import Optional


class ExperienceStore:
    def __init__(self, path: str = ".axilreino/experiences.json"):
        self.path = Path(path)

    def _load(self) -> list[dict]:
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save(self, experiences: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(
                experiences,
                file,
                indent=2,
            )

    def add(self, experience: dict) -> dict:
        experiences = self._load()

        experience = dict(experience)

        if "id" not in experience:
            experience["id"] = f"exp-{len(experiences) + 1:06d}"

        experiences.append(experience)
        self._save(experiences)

        return experience

    def get(self, experience_id: str) -> Optional[dict]:
        experiences = self._load()

        for experience in experiences:
            if experience.get("id") == experience_id:
                return experience

        return None

    def all(self) -> list[dict]:
        return self._load()

    def count(self) -> int:
        return len(self._load())