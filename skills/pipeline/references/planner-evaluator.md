# Planner Generator Evaluator Roles

Use this reference when task risk or size justifies separating planning, implementation, and evaluation.

## Trigger

Use only when task risk or size justifies the ceremony:
- large feature;
- broad refactor;
- high-risk change;
- AI-generated implementation;
- repeated implementation quality failure.

Do not force this role split for trivial fixes, typo-only docs edits, small config changes, or low-risk single-file updates. Use normal TDD and existing review gates instead.

## Roles

The roles are separate:
- `planner`: turns the approved spec into bounded implementation slices, contracts, tests, stop conditions, and evidence;
- `generator`: implements only the approved slice and reports changed files, commands, deviations, and risks;
- `evaluator`: reviews the output against the spec, tests, contracts, and diff before acceptance.

Do not silently let one builder/model instance fill planner, generator, and evaluator roles.

## Adversarial Evaluator

The evaluator is adversarial, not polite.

Blockers first: lead with correctness, safety, contract, missing-test, and scope findings.

Each blocking finding needs reproduction evidence such as file path, diff hunk, command output, failing test, log, or trace.

## Cross-Agent Symmetry

Cross-agent symmetry means using the other strong model when available and useful:
- Codex reviews Claude output;
- Claude reviews Codex output.

The reviewer should receive the artifact and acceptance criteria, not the builder's private rationale.

Record the review result, accepted fixes, rejected nitpicks, and residual risk.

## Simplifier Pass

For large implementations, add a post-implementation simplifier/evaluator pass after tests pass.

Ask what can be:
- removed;
- simplified;
- moved to a reference;
- split into a smaller task;
- deferred.
