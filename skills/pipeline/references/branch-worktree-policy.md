# Branch And Worktree Policy

Use this reference in Phase 0 before editing repository files.

## Safety Invariants

- Always run `git status --short --branch` first.
- Run the Target Repository Guard before branch, worktree, issue, or push work.
- Run the Repo-Match Guard before creating a branch, worktree, issue, or push when project `routing:` config exists.
- Never commit unknown user changes blindly.
- Never push `main` or `master` without an explicit user command.
- Never run destructive git actions such as reset, force checkout, force push, or branch deletion without explicit confirmation.
- Default: repository file edits happen on a feature branch.

## Decision Tree

1. **Read-only or planning only**
   - No branch or worktree is needed.
   - Do not create commits for analysis-only work.

2. **Already on a clean feature branch**
   - Continue on that branch if it matches the task.
   - If the branch name clearly belongs to another task, ask before reusing it.

3. **Target Repository Guard**
   - The target repository is the product or project repository named by the user's task.
   - The skill package repository is only the target repository when the requested work is to edit pipeline skills, references, tests, packaging, or docs.
   - Run `git rev-parse --show-toplevel` and confirm the repository root is the target project for the user task.
   - Compare `git remote get-url origin` with the intended GitHub repository when a remote exists.
   - Never create a task branch in the pipeline package or skill repository unless the task is editing pipeline itself.
   - If the task belongs to another product repo, stop before branch creation and switch to that repo.
   - branch, worktree, issue, and push happen in the target project repository, not in the skill package repo that happens to contain the instructions.
   - Do not create a branch in the current repo merely because it is where the pipeline instructions were loaded from.

4. **Repo-Match Guard**
   - If `CLAUDE.md` or project config contains `routing:`, compare the current `origin` remote with the repo implied by the task.
   - Compare the current `origin` remote with the intended GitHub repo before creating a branch, worktree, issue, or push.
   - If the task appears to belong elsewhere, stop and ask the user before creating a branch, worktree, or push.
   - If routing config is absent, continue and record the guard as not applicable for deep/hard work.

5. **On `main` or `master` and file edits are needed**
   - Create a feature branch before editing.
   - Do not edit repository files directly on `main` or `master` unless the user explicitly says to do that exact thing.

6. **Tiny docs/test-only change**
   - Create or reuse a feature branch.
   - Remote feature-branch push may be deferred only for tiny docs/test-only changes when the repo is clean, the change is low risk, and the user did not request remote backup.
   - If remote push is deferred, record residual risk in the report or final answer: branch exists locally but is not backed up remotely yet.

7. **Normal code, behavior, config, packaging, or multi-file change**
   - Create a feature branch.
   - Push the feature branch early when handoff, review, CI, or remote backup is expected.

8. **Use a worktree when isolation matters**
   - Use a worktree when the current working tree has unrelated dirty worktree changes, multiple agents need parallel write scopes, the task is high-risk, broad, or long-running work, or switching branches would disturb user work.
   - Assign one branch/worktree per independent write scope.
   - For autonomous or parallel work, also read `worktree-agent-isolation.md`.

9. **Blocked or ambiguous state**
   - Ask the user before continuing when there are unknown uncommitted changes, branch ownership is unclear, git remotes are missing, push fails, or the task would require editing directly on `main`.

## Mode Defaults

- `pipeline-lite`: feature branch by default; worktree only for dirty worktree, parallel agents, or risky scope. Tiny docs/test-only changes may defer remote push with residual risk recorded.
- `pipeline-deep`: feature branch required; prefer early remote push. Use worktree for broad work, dirty trees, or parallel execution.
- `pipeline-hard`: feature branch or worktree required; early remote push is expected unless the user explicitly chooses local-only execution.

## What This Does Not Change

- Branch completion still uses `superpowers:finishing-a-development-branch`.
- Dirty worktree protection remains mandatory.
- Destructive actions still require explicit confirmation.
- `origin/main` is not pushed without the user's explicit command.
