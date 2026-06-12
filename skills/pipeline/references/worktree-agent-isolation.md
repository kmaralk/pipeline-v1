# Worktree Agent Isolation

Builds on `branch-worktree-policy.md`; it does not replace it. Use this reference when a task needs autonomous execution, GitHub issue tracking, or parallel Claude/Codex workers.

## Core Model

- **Issue** stores the task, checklist, context, tests, risks, and progress.
- **Branch** protects `main` from unfinished work.
- **Worktree** gives each agent a separate folder and branch so parallel work does not collide.
- **Orchestrator** plans, assigns ownership, reviews diffs, runs integration tests, and merges one worker result at a time.
- **Worker** edits only its assigned files, runs assigned tests, reports evidence, and stops on conflicts.

## Repo-Match Guard

Run the Target Repository Guard from `branch-worktree-policy.md` first.

Before creating an issue, branch, worktree, or push, verify the current repository matches the task.

1. Read `CLAUDE.md` or project config for `routing:` if it exists.
2. Compare the task keywords and intended repo with `git remote get-url origin`.
3. If the task appears to belong to a different repo, stop and ask the user before creating a branch, worktree, or push.
4. If no routing config exists, continue and record that the guard was not applicable.

This prevents work for one product from being pushed to the wrong GitHub repository.

## GitHub Issue Policy

- `pipeline-lite`: issue optional; use only if the user supplied one or the task must survive handoff.
- `pipeline-deep`: issue recommended for medium/large tasks, autonomous execution, or work that may span sessions.
- `pipeline-hard`: issue required for autonomous or parallel execution unless explicitly skipped with a recorded reason.
- If an issue exists, use `gh-issues` to load context, link branch/worktree, update status, and write final AI session context.
- If no issue is created for deep/hard autonomous work, write `issue_skipped: <reason>` in state/report.

Minimum issue body:

```md
## Task
<what needs to change>

## Checklist
- [ ] <step>

## Acceptance
- <test or manual check>

## Affected Files
- <path/glob>

## Risks
- <risk or none>
```

## File Ownership Plan

Write this before dispatching parallel agents.

```md
## File Ownership Plan
- Orchestrator: <Claude Code | Codex | user/external reviewer>
- Worker A: branch/worktree <name>, owns <paths/globs>, tests <commands>
- Worker B: branch/worktree <name>, owns <paths/globs>, tests <commands>
- Shared files: <paths>, merge only by orchestrator
- Non-parallelizable conflicts: <paths/reasons>
```

Rules:

- Do not parallelize two workers that need the same writable files.
- Treat shared files as orchestrator-owned unless one worker gets explicit write ownership.
- Shared files are read-only for workers unless the orchestrator explicitly grants one owner.
- If ownership changes mid-task, stop and update the plan before continuing.
- Each independent write scope gets one branch/worktree.

## Worker Handoff Template

Give each worker only the context needed for its slice.

```md
You are not alone in this repo. Do not revert edits made by others.

Issue: <number or link>
Branch/worktree: <name/path>
Goal: <specific outcome>
Owns: <paths/globs the worker may edit>
Read-only context: <paths/globs the worker may inspect>
Forbidden: <paths/globs/actions>
Acceptance: <commands/manual checks>
Stop if: <conflict, missing dependency, unclear contract, test impossible>
Report: changed files, tests run, evidence, risks, follow-up needed
```

## Parallel Worktree Recipe

1. Orchestrator creates or loads the issue.
2. Orchestrator writes the File Ownership Plan.
3. Create one branch/worktree per independent worker scope.
4. Dispatch each worker with the Worker Handoff Template.
5. Workers commit only their own branch/worktree results.
6. Orchestrator reviews each worker diff separately.
7. Merge one worker branch at a time into the integration branch.
8. Run targeted tests after each merge; run the full regression set after the final merge.
9. Update the issue with final context, evidence, and residual risks.

## Integration Checklist

- Repo-Match Guard passed or was recorded as not applicable.
- Issue exists or skip reason is recorded.
- File Ownership Plan has no overlapping write scopes.
- Each worker branch/worktree has a clear goal, allowed files, tests, and stop conditions.
- Worker diffs were reviewed before merge.
- Integration branch passed targeted and full verification.
- Issue/status/report were updated before branch completion.

## Do not parallelize

Do not parallelize when:

- multiple workers must edit the same core file;
- the task has an unresolved architecture or contract decision;
- tests cannot be split by ownership;
- the cost of resolving merge conflicts is higher than serial execution;
- a worker would need broad permission to edit "anything needed".
