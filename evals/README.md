# Axilreino Evaluator

The Axilreino evaluator is the verification layer for Axilreino's coding models.

Its purpose is simple:

> Generated code should be tested rather than assumed to be correct.

## Current capabilities

The first evaluator supports Python solutions.

It can:

* create an isolated temporary workspace
* execute candidate Python code
* execute tests against the candidate code
* capture stdout and stderr
* detect non-zero exit codes
* enforce execution timeouts
* return structured evaluation results

## Evaluation flow

```text
Coding Task
    ↓
Candidate Solution
    ↓
Temporary Workspace
    ↓
Execute Tests
    ↓
Capture Result
    ↓
PASS / FAIL
```

## Example

A model generates:

```python
def largest_number(numbers):
    return max(numbers)
```

The evaluator executes tests against the implementation.

If all tests pass:

```json
{
  "passed": true,
  "exit_code": 0
}
```

If the implementation fails:

```json
{
  "passed": false,
  "exit_code": 1
}
```

## Design principle

Axilreino should learn from implementations that have been verified and from failures whose causes and fixes can also be verified.

The evaluator is therefore one of the foundations of Axilreino's future training and learning system.

## Planned expansion

Future evaluators will add:

* JavaScript
* TypeScript
* package/dependency verification
* build verification
* API testing
* database testing
* browser testing
* UI interaction testing
* screenshot comparison
* security checks
* regression testing

The evaluator should eventually be able to determine whether an entire generated application actually works, rather than only whether its source code looks reasonable.
