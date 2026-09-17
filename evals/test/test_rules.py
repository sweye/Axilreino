from rules import Rule, RuleStore


def test_rule_can_be_created():
    rule = Rule(
        scope={
            "language": "python",
            "technology": "python",
        },
        trigger="Need to find the largest value in a list.",
        rule="Use max() when the task requires the largest value.",
        reason="Returning the first element does not guarantee the largest value.",
        evidence=[
            "python-largest-number-001",
        ],
        confidence=1.0,
        verified=True,
        regression_test="largest_number([1, 5, 3]) == 5",
    )

    data = rule.to_dict()

    assert data["scope"]["language"] == "python"
    assert data["rule"] == (
        "Use max() when the task requires the largest value."
    )
    assert data["verified"] is True
    assert data["confidence"] == 1.0


def test_rule_store_starts_empty(tmp_path):
    store = RuleStore(
        path=str(tmp_path / "rules.json")
    )

    assert store.count() == 0
    assert store.all() == []


def test_rule_store_adds_rule(tmp_path):
    store = RuleStore(
        path=str(tmp_path / "rules.json")
    )

    rule = Rule(
        scope={
            "language": "python",
        },
        trigger="Need the largest value.",
        rule="Use max().",
        reason="max() returns the largest value.",
        confidence=1.0,
        verified=True,
    )

    created = store.add(rule)

    assert created["id"] == "rule-000001"
    assert created["verified"] is True
    assert store.count() == 1


def test_rule_store_retrieves_rule(tmp_path):
    store = RuleStore(
        path=str(tmp_path / "rules.json")
    )

    rule = Rule(
        scope={
            "language": "python",
        },
        trigger="Need the largest value.",
        rule="Use max().",
        reason="max() returns the largest value.",
        confidence=1.0,
        verified=True,
    )

    created = store.add(rule)

    retrieved = store.get(created["id"])

    assert retrieved is not None
    assert retrieved["id"] == created["id"]
    assert retrieved["rule"] == "Use max()."


def test_rule_store_persists_rules(tmp_path):
    path = str(tmp_path / "rules.json")

    store = RuleStore(path=path)

    rule = Rule(
        scope={
            "language": "python",
        },
        trigger="Need the largest value.",
        rule="Use max().",
        reason="max() returns the largest value.",
        confidence=1.0,
        verified=True,
    )

    store.add(rule)

    new_store = RuleStore(path=path)

    assert new_store.count() == 1
    assert new_store.all()[0]["verified"] is True