# Test Adequacy Review

Use this reference when tests are written, changed, deleted, weakened, or used as proof for behavior-changing work. The goal is to catch tests that are green but weak: over-mocked, tautological, happy-path-only, implementation-coupled, or too vague to guard the intended regression.

the human operator is not expected to review test code like an engineer. Human-visible progress is not enough evidence that tests are adequate.

## When TAR Is Mandatory

Run Test Adequacy Review when any condition is true:
- tests were added, edited, deleted, skipped, quarantined, broadened, or snapshot-heavy;
- a bugfix claims regression coverage;
- behavior, public contracts, auth, billing, persistence, migrations, concurrency, or error handling changed;
- implementation was AI-generated and accepted by another agent or model;
- execution is Codex-heavy, `full_autonomous`, or `overnight`;
- existing tests pass, but coverage of the actual risk is unclear.

For `guided_autonomous` (Guided autonomous), TAR is risk-triggered by the same conditions above. Do not treat the human operator's presence as a test-quality review unless he explicitly reviews the test strategy with engineering detail.

Skip TAR only for docs-only, comments-only, formatting-only, or non-behavioral config changes when tests were not changed. Record a one-line skip reason.

## TAR Checklist

The TAR checklist is a minimum floor, not a closed list. Add task-specific test risks when the change involves auth, billing, migrations, browser UI, concurrency, data loss, permissions, performance, observability, rollout, or other domain-critical behavior. Do not force irrelevant extras onto small low-risk work.

1. **Behavior, not implementation** - assertions target observable output, state, contract, or effect, not private call structure.
2. **Failure proof** - evidence that tests fail for the intended bug or missing behavior, or a focused explanation when a RED run is impossible.
3. **Edge and negative coverage** - important boundary, error, rejection, and empty-state paths are covered or explicitly deferred.
4. **Mock honesty** - mocks sit only at true external boundaries; the system under test is not mocked away.
5. **Assertion strength** - assertions use specific values, shapes, errors, or state changes; not only truthy/not-empty/called-once.
6. **Independence** - tests pass in isolation and do not depend on leaked fixture state or run order.
7. **Intent in name** - the test name states the invariant, regression, or contract it protects.
8. **Lazy implementation check** - a hardcoded or no-op implementation would not pass the important tests.

Never delete a failing test only to make the pipeline pass. If a test is wrong, prove it is wrong and preserve the intended behavior in a corrected test.

## TAR Verdict

Record a `TAR verdict` in the report, review pack, Codex final reply, or morning handoff. Allowed values are `adequate | adequate_with_gaps | inadequate`:

```text
TAR verdict: adequate | adequate_with_gaps | inadequate
Evidence:
- RED/failure proof:
- Checklist gaps:
- Accepted/deferred gaps:
- Blocking fixes:
```

`adequate_with_gaps` may proceed only when gaps are low-risk, named, and deferred with residual risk. `inadequate` blocks completion until tests are improved or the user explicitly accepts the risk.
