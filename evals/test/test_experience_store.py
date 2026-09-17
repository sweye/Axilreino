from evals.experiences import ExperienceStore


def test_store_starts_empty(tmp_path):
    store = ExperienceStore(
        path=str(tmp_path / "experiences.json")
    )

    assert store.count() == 0
    assert store.all() == []


def test_store_adds_experience(tmp_path):
    store = ExperienceStore(
        path=str(tmp_path / "experiences.json")
    )

    experience = store.add(
        {
            "scope": {
                "language": "python",
                "technology": "python",
            },
            "failure": {
                "type": "assertion_failure",
                "summary": "The solution produced an unexpected result.",
            },
            "original_code": "return numbers[0]",
            "repaired_code": "return max(numbers)",
            "result": "passed",
            "verified": True,
        }
    )

    assert experience["id"] == "exp-000001"
    assert experience["verified"] is True
    assert store.count() == 1


def test_store_retrieves_experience(tmp_path):
    store = ExperienceStore(
        path=str(tmp_path / "experiences.json")
    )

    created = store.add(
        {
            "scope": {
                "language": "python",
                "technology": "python",
            },
            "failure": {
                "type": "assertion_failure",
            },
            "original_code": "return numbers[0]",
            "repaired_code": "return max(numbers)",
            "result": "passed",
            "verified": True,
        }
    )

    retrieved = store.get(created["id"])

    assert retrieved is not None
    assert retrieved["id"] == created["id"]
    assert retrieved["repaired_code"] == "return max(numbers)"


def test_store_persists_experience(tmp_path):
    path = str(tmp_path / "experiences.json")

    store = ExperienceStore(path=path)

    store.add(
        {
            "scope": {
                "language": "python",
            },
            "result": "passed",
            "verified": True,
        }
    )

    # Create a new store using the same file.
    new_store = ExperienceStore(path=path)

    assert new_store.count() == 1
    assert new_store.all()[0]["verified"] is True