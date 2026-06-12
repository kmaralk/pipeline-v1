# Run-Control Inheritance

Use this when review, testing, implementation, resume, or handoff discovers work that was not in the accepted task scope.

## Sticky Invariant

Default direction is defer-by-default. Do not silently expand scope just because the work was discovered during an autonomous run.

- Accepted blocking discovered work inherits the current `run_control`.
- Do not downgrade an accepted child task from the parent `run_control`, even if the child looks like lite work.
- New feature work requires explicit user acceptance as part of the current run or a new pipeline.
- `pre-existing`, `unrelated`, and `out of scope` are evidence labels, not completion excuses.

## Pre-Existing Bug Accountability

When a discovered issue already existed before the current edits, classify impact before deferring it.

- If it blocks required verification, changed behavior, data safety, security, or honest acceptance of the current task, fix it in the current run and inherit the parent `run_control`.
- If it is real but non-blocking, record evidence, residual risk, and a follow-up location instead of hiding it behind "pre-existing".
- If it is genuinely unrelated scope or a new feature, defer it with a concrete reason and keep the current task's acceptance statement honest.

Do not use "pre-existing", "unrelated", "out of scope", or "needs refactor" as a standalone reason to finish while required checks still fail.

## Discovered-Task Gate

1. Classify the discovered work:
   - `blocking_current_acceptance`: prevents closing the current accepted goal.
   - `non_blocking_bug`: real issue, but current goal can close honestly without it.
   - `new_feature_or_scope`: new behavior, UX, integration, architecture, or product scope.
2. Check the current `run_control`. If it is missing, stop before handoff or execution; missing `run_control` is a blocker. On a resumed state.json or context pack where `run_control` is missing or empty, the receiver MUST re-ask the user via the Run Control Choices menu. Do not silently inherit the `C4 A3` / `codex_heavy_claude_guardrails` legacy default — the silent fallback was removed because it consistently produced the wrong autonomy for resumed legacy runs.
3. Decide:
   - `blocking_current_acceptance` -> fix inside the current run and inherit the parent `run_control`.
   - `non_blocking_bug` -> record in deferred decisions/backlog unless explicitly accepted into scope.
   - `new_feature_or_scope` -> defer or start a new pipeline unless the user explicitly accepts it into the current run.
4. If the issue is called `pre-existing`, `unrelated`, or `out of scope`, include the impact classification and evidence before relying on that label.
5. Log the decision in the task brief, state, report, or deferred decisions.

## Handoff Requirement

Every Codex, worker, oracle, or resume context pack MUST include `run_control`, plus the normalized fields when available:

```json
{
  "run_control": "C4 A3",
  "collaboration_profile": "codex_heavy_claude_guardrails",
  "autonomy": "full_autonomous",
  "cross_check_initial": false,
  "premortem_plan_review": "auto | forced | skipped"
}
```

If the context pack omits `run_control`, the receiver asks for it or reconstructs it from state before execution. Do not guess `C1 A1` or reroute the child task from scratch.

## Examples

| Discovered work | Decision |
| --- | --- |
| Heavy run `C4 A3`; review finds a regression that blocks acceptance | Accept as blocking, fix in current run, child inherits `C4 A3`. |
| Heavy run `C4 A3`; review finds unrelated copy typo | Record/defer unless explicitly accepted; if accepted, do not downgrade run-control. |
| Lite run; user says "also add this new feature" mid-fix | Treat as new scope; defer or start a new pipeline unless explicitly accepted. |
