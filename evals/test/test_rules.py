from rules import Rule, RuleExtractor, RuleRetriever, RuleStore


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


def test_rule_extractor_creates_rule_from_verified_experience():
    experience = {
        "id": "exp-000001",
        "scope": {
            "language": "python",
            "technology": "python",
        },
        "failure": {
            "failure_type": "assertion_failure",
            "summary": "The solution produced an unexpected result.",
            "raw_error": "AssertionError",
            "language": "python",
        },
        "original_code": """
def largest_number(numbers):
    return numbers[0]
""",
        "repaired_code": """
def largest_number(numbers):
    return max(numbers)
""",
        "result": "passed",
        "verified": True,
    }

    extractor = RuleExtractor()

    rule = extractor.extract(experience)

    assert rule is not None
    assert rule.verified is True
    assert rule.confidence == 1.0
    assert rule.scope["language"] == "python"
    assert "max()" in rule.rule
    assert "exp-000001" in rule.evidence


def test_rule_extractor_rejects_unverified_experience():
    experience = {
        "id": "exp-000002",
        "result": "passed",
        "verified": False,
        "failure": {
            "failure_type": "assertion_failure",
            "language": "python",
        },
    }

    extractor = RuleExtractor()

    rule = extractor.extract(experience)

    assert rule is None


def test_rule_retriever_finds_matching_verified_rule(tmp_path):
    store = RuleStore(
        path=str(tmp_path / "rules.json")
    )

    rule = Rule(
        scope={
            "language": "python",
            "technology": "python",
        },
        trigger="Need to find the largest value in a list.",
        rule="Use max() when the task requires the largest value.",
        reason="Returning the first element does not guarantee the largest value.",
        confidence=1.0,
        verified=True,
    )

    store.add(rule)

    retriever = RuleRetriever(store)

    matches = retriever.retrieve(
        language="python",
        technology="python",
        query="largest value",
    )

    assert len(matches) == 1
    assert matches[0]["rule"] == (
        "Use max() when the task requires the largest value."
    )


def test_rule_retriever_ignores_unverified_rules(tmp_path):
    store = RuleStore(
        path=str(tmp_path / "rules.json")
    )

    rule = Rule(
        scope={
            "language": "python",
            "technology": "python",
        },
        trigger="Need to find the largest value.",
        rule="Use max().",
        reason="max() returns the largest value.",
        confidence=0.5,
        verified=False,
    )

    store.add(rule)

    retriever = RuleRetriever(store)

    matches = retriever.retrieve(
        language="python",
        technology="python",
        query="largest value",
    )

    assert matches == []