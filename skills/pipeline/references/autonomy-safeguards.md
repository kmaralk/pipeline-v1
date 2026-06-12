# Autonomy Safeguards

Use this reference before autonomous execution, Codex batches, or parallel workers.

## Autonomous Backup Gate

Before guided_autonomous, full_autonomous, overnight, Codex-batched, or subagent-driven execution, create a recoverable checkpoint.

Minimum checklist:
- run `git status --short --branch` and confirm all dirty files are understood;
- do not include unknown user changes in a backup commit;
- create or verify a feature branch/worktree per `branch-worktree-policy.md`;
- push the feature branch early when remote backup is available, or record why local-only is accepted;
- record the backup ref in state/report: branch name, commit hash if created, and remote push status.

If a backup checkpoint cannot be created, do not enter unattended execution. Use interactive/guided work or stop for the user decision.

## Pre-Autonomy Context Freeze And Compact Gate

Before full_autonomous, overnight, Codex-batched, or subagent-driven execution, freeze the useful context into durable artifacts before any compact/fresh-session handoff.

Minimum checklist:
- write the durable task brief with goal, MVP scope, explicit deferrals, contracts, and acceptance checks;
- record open questions with `blocking | answered | deferred` status;
- record file ownership, allowed/forbidden files, verification commands, stop conditions, and backup ref;
- update state/report with current phase, completed work, changed files, and latest test results;
- if context is long or stale, propose compact/fresh context only after the artifacts above exist.

Only then compact. Do not compact in the middle of a failing-test/fix loop or between a worker result and its verification.

## Codex Progress Watchdog

Use this after launching any async/background Codex run: plugin task, MCP task that returns a job handle, direct `codex exec` in background, Codex-heavy batch, or overnight Codex execution.

Do not wait passively for a long Codex run. Immediately after launch:
- record the route, pid/job id if available, stdout/stderr/result paths, prompt path, cwd, start time, and next check time;
- check within 1 minute whether Codex actually started by reading status/result/logs or the process state;
- Estimate the expected Codex runtime before launch and set the steady-state watchdog cadence:
  - up to 20 minutes: check every 5 minutes;
  - 20 minutes to 2 hours: check every 10 minutes;
  - longer than 2 hours or overnight: check every 20 minutes, unless the night protocol or a project-specific cap is stricter;
- each check must look for: completed result, failed before useful work, blocked, waiting for input, or stuck with no useful progress;
- if Codex did not start, failed before useful work, or is blocked, waiting for input, or stuck, stop waiting and make an orchestrator decision: restart with a corrected route/prompt, fall back, split the batch, or ask the user.

For direct CLI background runs, inspect the process plus explicit stdout/stderr logs. For plugin runs, use the plugin status/result command. For MCP/job-handle routes, use the returned status/result channel. Record each watchdog check in state/report before launching another long Codex job.

## Independent Parallel Execution Default

When the platform and governing instructions allow subagents, prefer parallel subagents for independent milestones. Immediate blocking work stays local; only sidecar or independent implementation slices should be delegated.

Use the default only when all are true:
- the plan has enough independent work to justify coordination overhead;
- the next local step is not blocked on the delegated result;
- no shared write targets exist between workers;
- contracts, owner files, verification, and stop conditions are written before dispatch;
- `worktree-agent-isolation.md` has been applied when work may overlap, run long, or touch broad files.

Do not parallelize just because the task feels large. If independence is unclear, run serial TDD or ask for a narrower split.

## Unattended Attempt Budget Stop Rule

Only for `full_autonomous` or `overnight` execution in `pipeline-deep` or `pipeline-hard`, attempts >= 3 means the milestone is no longer safe to keep burning tokens on.

Procedure:
1. Stop fixing that milestone.
2. mark the milestone `failed` or `blocked` in state/report and store the short `last_error`.
3. Record what was tried, why it failed, and the next options: retry with user guidance, skip, decompose, or abort.
4. continue with independent unaffected milestones only when they do not depend on the failed contract, schema, file, or behavior.
5. Leave a morning-review note for the user with the blocked milestone, evidence, and recommended next action.

Interactive and guided-autonomous runs should stop and ask instead of silently skipping after the third failed attempt.

## Retry vs Attempt-Budget Precedence (F-042)

The shared retry discipline at `shared.md §Retry Discipline` says "Third failure: STOP completely" while this file's attempt-budget rule says "after attempts >= 3, continue with independent unaffected milestones". Both are correct in their scope; the precedence is:

- **Interactive and guided-autonomous runs (A1, A2):** the shared retry rule wins. Third failure STOPs completely and asks the user, regardless of milestone independence. Do not silently advance to another milestone.
- **Full-autonomous and overnight runs (A3, A4):** this file's attempt-budget rule wins for milestone-local independence — the failed milestone is marked `failed`/`blocked` and the run continues with independent unaffected milestones; the global stop only fires if all remaining milestones depend on the failed one, or if the user pre-approved continuation, or if a non-retryable invariant was violated.

The user may pre-approve "continue past third failure on independent milestones" explicitly; without that pre-approval the interactive/guided rule's global stop applies.
