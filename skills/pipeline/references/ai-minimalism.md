# AI Minimalism Guardrails

Use this when implementation, review, or skill work could let an AI agent generate more code or context than the task needs. It augments the selected pipeline mode; it does not replace TDD, source grounding, review, browser evidence, or run-control rules.

## Triggers

Read this reference when:

- the task writes or reviews AI-generated code;
- the implementation could spread across files not named by the scope;
- the agent is about to build custom logic for common infrastructure;
- a green test run leaves a broad, noisy, or hard-to-review diff;
- the task adds or changes AGENTS, CLAUDE, SKILL, prompt, or context rules.

Skip this for typo-only edits, pure formatting, generated files that must match an external schema, or mechanical sync after an already-reviewed source change.

## Minimal Diff Packet

Before writing code or handing work to another agent, name:

- smallest acceptable user-visible or test-visible change;
- files likely to change and files intentionally out of scope;
- existing helper, pattern, or contract to follow;
- tests or runtime checks that prove the small change works;
- explicit non-goals, especially surrounding cleanup, opportunistic refactors, and nice-to-have behavior.

If the packet cannot be written without guessing, return to planning, source grounding, or a focused user question instead of letting the implementation choose silently.

## Reuse-Before-Build

Before custom code for auth, caching, parsing, scheduling, retries, state machines, crypto/security, UI primitives, data fetching, validation, serialization, or integrations:

1. Search local code for an existing helper, project pattern, or dependency wrapper.
2. Check the local dependency manifest or lockfile for a mature library already available.
3. If a new external library is considered, use Source Grounding and respect local dependency/security policy before adding it.
4. If custom code still wins, record the reason: no local helper, dependency would be larger/riskier, behavior is project-specific, or adding a dependency is out of scope.

Do not install a package just to avoid small local code. The question is whether reuse reduces lines, review burden, and long-term support risk for this task.

## Post-Green Simplify Pass

After targeted tests pass and before review/reporting, scan the diff once for removable AI bloat:

- delete unused abstractions, options, state, comments, and speculative error handling;
- replace duplicate or custom code with existing helpers when that does not expand scope;
- shrink tests that overfit implementation details while preserving behavior coverage;
- split or defer changes that make review larger than the accepted scope.

If simplification changes behavior, add or update tests first and re-run the relevant verification. Record kept, removed, moved, and deferred items when the diff is medium/risky or AI-generated.

## Context Rule Audit

For every new or changed context rule, ask what concrete failure or repeated problem this rule prevents. Prefer evidence from a recent session, eval scenario, incident, or known safety boundary.

If no current failure, risk, or eval scenario justifies it, reject the rule, move it to a progressive reference, or add an eval first. Do not weaken hard safety rules for secrets, destructive actions, user data, dependency security, or test deletion only because they have not fired recently.

## Review Burden Budget

When a diff is broad or AI-generated, the review pack should explain why the diff is not larger than necessary. If the reviewer must inspect unrelated behavior to trust the change, split the work, defer cleanup, or return to the Minimal Diff Packet.
