# Idea To Ship Stage Gates

Use this reference when a pipeline task starts from a raw idea, PRD/spec work, architecture uncertainty, implementation chunks, bugfix verification, or release handoff.

This must augment existing pipeline behavior; do not replace run-control, TDD, premortem, test adequacy review, source grounding, browser evidence, review lenses, or ship readiness. It is not a new pipeline mode.

## Department Labels

Name the current working role in plain language when it helps the user understand the phase:

- product strategist: clarify a raw idea;
- product manager: define what and why;
- architect: define how the system fits together;
- developer: implement a bounded chunk;
- QA/debugger: reproduce, isolate, and verify;
- release operator: prepare launch, rollback, and monitoring.

The label explains the current phase. It does not change `pipeline-lite`, `pipeline-deep`, `pipeline-hard`, `C#`, `A#`, `X`, `P`, or sticky run-control.

## Raw Idea Intake

Use this when the user gives a voice-like stream, rough concept, or unfinished product idea.

Before planning, produce:

- a short idea statement;
- what is in scope;
- what is out of scope;
- 2-3 user stories showing how someone would use it;
- up to 1-2 blocking questions, only when needed.

In autonomous `A3/A4`, do not stall on low-risk questions. Record a reasonable assumption and continue. If the idea is still too unclear to choose scope, escalate or ask the smallest blocking question.

## What-before-How PRD Gate

Use this when writing or reviewing a PRD/spec.

The PRD should answer what and why before how:

- purpose: who gets what value;
- users and scenarios;
- success metrics or observable acceptance;
- constraints: stack, budget, time, licensing, policy, existing contracts;
- rollout notes when real users or runtime are affected;
- risks and non-goals.

Implementation details belong in the PRD only as constraints or explicit decisions already accepted by the user. Do not let a PRD silently become an implementation plan.

## Minimal Architecture Pack

Use this before coding when architecture, contracts, data, or module boundaries are not already clear.

Record the minimum useful architecture:

- file or module structure;
- data model, schema, or state shape;
- API, events, auth, errors, limits, and compatibility contracts when relevant;
- tech decisions and why they fit the current constraints;
- what is intentionally not built for the MVP.

Keep it minimal. Do not copy a large architecture template when the current task only needs one contract, one module boundary, or one data decision.

## Implementation Chunk Check

The existing pipeline TDD and milestone rules remain the source of truth for implementation. Use this only as a plain-language reminder:

- work in small chunks;
- validate each chunk before the next;
- keep context to PRD/spec, architecture, relevant files, tests, and acceptance.

## Bug Fix Record

Use this for non-trivial bugs, repeated failures, or fixes that future agents may otherwise rediscover.

Record, in plain language:

- repro: how the bug showed up;
- symptom: what was wrong;
- root cause: why it happened;
- fix: what changed;
- verification: what test, command, log, browser check, or manual check proved the fix;
- regression guard: what prevents the bug from coming back;
- scope guard: what was not changed.

The final explanation should say what happened, why it happened, how it was fixed, and how the fix was verified.

For trivial typo-only fixes, keep this as a one-sentence note in the final summary instead of creating ceremony.

## Chat Summary Gate

After implementation, bugfix, skill change, prompt change, or agent-workflow change, show a user-facing summary in chat before asking branch-completion questions or ending the turn.

Use `skills/pipeline/references/report-status-evidence.md` for the full shape. If no report file was needed, still show a compact numbered block in chat with:

- pluses;
- cons or residual risks;
- security impact;
- what behavior changed;
- what stayed the same.

This gate is for visibility. It does not replace the technical report, tests, package validation, or distribution checks when those are required.
