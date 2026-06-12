---
name: pipeline-lite
description: "Use when doing small/medium clear local work; skill/active-copy edits; AI-output regression; bad-plan repair; repeated tool failures; producer/consumer handoff; or frontend/UI browser evidence. Use pipeline-deep when product, UX, contract, research, or architecture uncertainty grows."
---

# Pipeline Lite

Fast path for well-bounded engineering work. Keep safeguards explicit, but cheap enough for small tasks.

Discovered tasks and run-control inheritance: read `skills/pipeline/references/run-control-inheritance.md` before accepting or handing off work found during review, testing, implementation, or resume. Do not downgrade accepted child work from the parent `run_control`. Do not silently implement discovered new features.

Premortem plan review: read `skills/pipeline/references/premortem-plan-review.md` before accepting a risky plan or handing work to an autonomous/Codex-heavy executor. For lite, run it only for medium/high-risk, behavior-changing, multi-file, contract, migration, user-facing, or unclear work; run it before Phase 3 Execute. Skip it for trivial docs, typo, or obvious one-file fixes.

## Immediate Clean-Context Small-Local Gate

If a small local bugfix request has no repository path, file path, or test path, do not search broad filesystem or repository candidates. Do not run `find`, `git status`, `rg`, or inspect `/tmp` to guess the repository.

For routing or eval answers, the first sentence must include `Skip Code Routing Map`; answer `Skip Code Routing Map`, then name targeted `rg`, nearby code/tests, and focused regression/verification; ask for the exact repo/path only if implementation is required.

Safety override: for cookies/localStorage/sessionStorage/auth headers/tokens, public bodies/logs/transcripts/env/browser network, runtime `done`, cross-repo/external-state DONE, speculative blockers, scan-at-sink, or third-party repo intake, handle the safety packet before the small-local shortcut.

Use this response shape: `Skip Code Routing Map. Нужен точный путь к repo/file/test.` Then: targeted `rg`, nearby code/tests, focused regression/verification.

## First Response Failure Packets

Canonical wording, trigger table, and minimum fields: read `skills/pipeline/references/first-response-packets.md` before composing the first response when any trigger below appears (F-020 dedup executed 2026-06-09).

Include the relevant first response packets before implementation steps when a trigger appears:

- Browser evidence packet — user-facing frontend/UI/page/form/browser-route/user-journey work.
- Plan repair packet — a draft, prompt, or plan is structurally wrong.
- Premortem plan review packet — medium/high-risk plans, behavior changes, multi-file work, contract/migration/user-facing changes, or Codex-heavy/autonomous execution.
- Skill-change eval packet — non-trivial skill, prompt, routing, model, or agent-workflow changes.
- Code Routing Map packet — existing large, old, or cross-cutting codebase, or stale docs/specs conflicting with code.
- Tool failure recipe packet — repeated command or tool syntax/env/context failures.
- Trace evidence packet — AI prompt/output regressions.
- Contract handoff packet — producer/consumer surfaces split.
- Review evidence packet — large or risky AI-generated implementation reviews.
- Durable task brief packet — agent execution from chat.
- Questions ledger packet — open questions persisting past a phase boundary.
- Context budget packet — noisy tool requests.

## Fresh Baseline Batch-Fix Rules

Read `skills/pipeline/references/discipline-rules.md` §Fresh Baseline Batch-Fix Rules and apply each rule in the first response when its trigger appears (dedup executed 2026-06-09).

## Final Polish Rules

Read `skills/pipeline/references/discipline-rules.md` §Final Polish Rules before reviews, agent dispatch, and final summaries (dedup executed 2026-06-09).

## When to Use

Use when:
- A bugfix, refactor, or small feature is already understandable from local code and docs
- The task affects one local area or a few tightly related files
- Requirements are mostly stable
- External research is unnecessary or only a minor blocker

Do not use when:
- The task starts from a raw idea
- UX, contracts, architecture, or product behavior are unclear
- Multiple subsystems or external dependencies must be researched first

If those appear during execution, escalate to `pipeline-deep`.

## Inputs

Start from either:
- A backlog entry in `memory/backlog.md`
- A direct small technical request from the conversation

If the task comes directly from chat, first normalize it into a short task brief:
- problem
- desired result
- affected area
- test criterion

## Language Rule

See `skills/pipeline/references/shared.md` §Language Rule.

## Phase 0: Branch And Worktree Policy

**MANDATORY before repository file edits.**

1. Run `git status --short --branch`.
2. Read `skills/pipeline/references/branch-worktree-policy.md`.
3. Apply the `pipeline-lite` mode default from that reference.
4. If a dirty worktree, parallel agents, or risky scope appears, read `skills/pipeline/references/worktree-agent-isolation.md` before continuing.
5. If remote feature-branch push is deferred for a tiny docs/test-only change, record residual risk in the design/report or final answer.

### Baseline Gates

See `skills/pipeline/references/shared.md` §Baseline Gates.

Применимость: mandatory. Для lite достаточно Python/Node (Go-проверка опциональна, зависит от стека проекта).

## Phase 1: Intake

**REQUIRED for `feature` or non-trivial `refactor`:** Invoke `superpowers:brainstorming` before implementation thinking.
**For `bugfix`:** brainstorming is optional — invoke only if root cause is unclear or the fix approach has multiple valid paths. Skip for straightforward bugs where the failure mode and fix are already obvious from the repro.

Rationale: `superpowers:brainstorming` is scoped to creative work (features, behavior changes). Running it on a trivial bugfix is ceremonial and degrades signal.

1. Classify the task: `bugfix | feature | refactor`
2. Confirm it is `small | medium`, not discovery-heavy
3. Set a quick risk level: `low | medium | high`
4. Gather a compact context pack:
   - relevant files
   - nearby tests
   - run/test/verify commands
   - local project rules
5. Write a short implementation brief with:
   - scope
   - non-goals
   - risks
   - acceptance criteria
   - regression map
   - evidence to collect
   - for user-facing frontend, UI, page, form, browser route, or user journey work: include browser or user-journey evidence in the first task brief. The brief must cover route, viewport, user steps, expected visible result, and negative check; list all four accepted evidence route options before choosing one: Playwright / agent-browser / project e2e / documented manual browser evidence.
   - Accepted route summary: Playwright, agent-browser, project e2e, or documented manual browser check.
   - before listing implementation steps, include this Browser evidence packet:
     - route/page:
     - viewport: mobile and desktop, or skip reason
     - steps:
     - expected visible result:
     - negative check:
     - evidence route: Playwright / agent-browser / project e2e / documented manual browser evidence
   - Do not write only generic test/manual check wording. If browser automation is unavailable, include a Manual fallback record with exact route, viewport, steps, observed visible result, unchecked items, and residual risk.

### Lightweight Memory Bank

See `skills/pipeline/references/shared.md` §Lightweight Memory Bank.

For lite, read only a project memory index or directly relevant runbook if it exists. Do not create new memory structure unless the task discovers a repeated mistake or known-good command worth preserving.

### Tool and Model Routing Matrix

See `skills/pipeline/references/shared.md` §Tool and Model Routing Matrix.

For lite, default to the current coding agent and local tests. Escalate tools only when the evidence plan needs them.

### CLI Recipes and Tool Failure Log

See `skills/pipeline/references/shared.md` §CLI Recipes and Tool Failure Log.

If a local command takes repeated attempts to get right, capture the known-good command in the report or a focused runbook.
Record the known-good command, cwd, and failure mode.

### Prototype And Trace Practices

See `skills/pipeline/references/shared.md` §Prototype And Trace Practices and `skills/pipeline/references/prototype-trace.md`.

For lite, use this only when the implementation has a clear risky edge: uncertain tool syntax, an API contract, AI-app debugging, or repeated agent/tool failure. Keep the prototype spike disposable and record only the trace evidence needed to explain the decision.
Require a raw artifact before prompt or tool-contract edits.

### Skill vs Runbook vs CLI Decision Rule

See `skills/pipeline/references/shared.md` §Skill vs Runbook vs CLI Decision Rule.

For lite, prefer a runbook note over a new skill unless the lesson is clearly reusable across projects.

File-First Knowledge Before RAG is intentionally omitted from lite intake. If knowledge lookup grows beyond local files, targeted `rg`, and direct runbooks, escalate to `pipeline-deep` instead of adding RAG decisions to lite.

### Skill Packaging and Portability

See `skills/pipeline/references/shared.md` §Skill Packaging and Portability and `skills/pipeline/references/packaging.md`.

For lite, use this only when the task changes pipeline skill packaging, `agents/openai.yaml`, active-copy sync, validators, or third-party skill installation/review.

### Grounding Required

See `skills/pipeline/references/shared.md` §Grounding Required.

For lite, keep this cheap: any uncertain claim in the brief, report, or final answer must be backed by a file reference, command result, test output, or moved into assumptions/residual risk.

### Source Grounding

See `skills/pipeline/references/shared.md` §Source Grounding and `skills/pipeline/references/source-grounding.md`.

For lite, read this only when the small task depends on an external library, API, SDK, framework, CLI, protocol, vendor service, or versioned behavior. Use local dependency version, official docs, and Context7 when available before writing integration code from memory.

### AI Minimalism Guardrails

See `skills/pipeline/references/ai-minimalism.md`.

For lite, use the Minimal Diff Packet before non-trivial code or skill edits, Reuse-Before-Build before custom common infrastructure, and the Post-Green Simplify Pass before reporting when the diff is AI-generated, multi-file, or larger than the accepted scope. Use Context Rule Audit for AGENTS, CLAUDE, SKILL, prompt, or context-rule changes.

### Idea To Ship Stage Gates

See `skills/pipeline/references/shared.md` §Idea To Ship Stage Gates and `skills/pipeline/references/idea-to-ship-gates.md`.

For lite, use only the matching small piece: Raw Idea Intake may escalate to `pipeline-deep`; What-before-How PRD Gate applies to compact specs; Minimal Architecture Pack applies only when boundaries are unclear; Bug Fix Record applies to non-trivial bugs; Chat Summary Gate applies before final handoff.

Also write 1-3 plain-language acceptance scenarios:
- what the user/operator does
- what should happen
- what should not happen

If key requirements are missing, ask focused clarifying questions before coding.

## Phase 1.5: Context-Driven Practices

**Strictness for lite: RECOMMEND.** Каждая применимая practice показывается пользователю, по умолчанию выключена, включается только по подтверждению.

Цель — подтянуть только те практики, которые реально нужны этой конкретной задаче, без перегрузки lite-режима.

### Шаги

1. Прочитать `skills/pipeline/references/practices-index.md` (лёгкий индекс, ~50 строк).
2. Для каждой строки индекса — проверить триггеры в два шага:
   - **Step A — exact match (0 tokens):** ключевое слово из `keywords` есть в brief Phase 1 ИЛИ glob из `paths` совпадает с файлами из context pack.
   - **Step B — semantic fallback (small AI call):** если Step A не сработал, но brief длинный или контекст неявный — короткая AI-проверка против `semantic` строки индекса.
   - Practice активируется, если хотя бы один шаг сказал «да».
3. Для КАЖДОЙ активированной practice — открыть `skills/pipeline/references/practices-full.md` на якоре `#<id>` и прочитать ТОЛЬКО её блок. Не загружать файл целиком.
4. Составить список активированных practices и показать пользователю:

```
Context-Driven Practices для этой задачи:

  [ ] threat-model          — <причина активации>
  [ ] idempotency           — <причина активации>
  [ ] <id>                  — <причина активации>

Действия:
  Enter       принять все (добавить в spec)
  1,2,3       выбрать номера
  +N          добавить ручную <id>
  -N          убрать номер
  none        отключить все
  detail N    показать полный текст practice
```

Для lite по умолчанию чек-боксы **пустые** — пользователь явно выбирает.

5. Для каждой выбранной practice — добавить её `Add to Phase 4 (spec)` секцию в PRD этой задачи. `Add to Phase 7 (verify)` кладётся в чек-лист верификации.

### Output

В начало PRD Phase 2 добавить блок:

```md
## Active Practices
- <id1> — strictness: recommend (selected by user)
- <id2> — strictness: recommend (selected by user)
```

Если ни одна practice не выбрана — `## Active Practices: none` (это валидно для lite).

## Phase 2: Compact Spec

Write a short PRD to `docs/plans/YYYY-MM-DD-<topic>-design.md`.

If a design doc for this topic already exists, update it — preserve completed milestones, decisions, and assumptions. Do not overwrite progress.

Required sections:
- context and problem
- affected files or components
- contract changes, if any
- risk level
- acceptance scenarios
- regression map
- evidence plan
- input validation checklist (baseline — all external inputs)
- active practices (from Phase 1.5, even if empty)

### Input Validation Checklist

See `skills/pipeline/references/shared.md` §Input Validation Checklist.

### Assumptions

See `skills/pipeline/references/shared.md` §Assumptions Section.

### Milestones

See `skills/pipeline/references/shared.md` §Milestones Template.

Для lite опустить секцию `### Tasks` — milestones атомарны, задачи прописываются прямо в Goal/Validation.

### Verifiable Acceptance Criteria

See `skills/pipeline/references/shared.md` §Verifiable Acceptance Criteria.

Each lite milestone must include a runnable validation command or an explicit manual check. If that cannot be written, clarify or escalate to `pipeline-deep`.

### Ambiguity Scanner

See `skills/pipeline/references/shared.md` §Ambiguity Scanner.

For lite, run this before executing medium-risk or multi-file work. Resolve real ambiguity in the spec rather than letting the implementation choose silently.

### Spec Regeneration Rule

See `skills/pipeline/references/shared.md` §Spec Regeneration Rule.

If the compact spec is structurally wrong, patch the spec source and re-check it instead of stacking corrective chat follow-ups.

### Clean-Context Plan Review

See `skills/pipeline/references/shared.md` §Clean-Context Plan Review.

For medium-risk or multi-file feature/refactor work, review the compact spec from a fresh-context perspective before Phase 3. Fix blockers around scope, contracts, tests, or acceptance before execution.

### Skill Behavior Evals and Scorecard

See `skills/pipeline/references/shared.md` §Skill Behavior Evals and Scorecard.

For lite, this is mandatory for non-trivial skill, prompt, or agent-behavior changes. Keep it compact: define/update the relevant clean-context scenarios, fill the scorecard, update `skills/pipeline/evals/metrics.md` when eval metrics are measured, and record any skipped scenarios as residual risk.

### Downstream Contract Handoff

Read `skills/pipeline/references/contract-handoff.md`.

For lite, create a compact handoff when a small change alters an API, schema, event, database shape, or UI-consumed payload. Put it in the compact spec or implementation report, and use it as the subagent contract if another agent will handle the consumer side.

### Resume State

See `skills/pipeline/references/shared.md` §Resume State Block.

### Phasing Rule

When milestones reach 5+, apply this decision tree — do not split-by-default:

1. **Is the task still understandable without new research?**
   - No → escalate to `pipeline-deep` (см. "Escalation to pipeline-deep" ниже).
   - Yes → continue.
2. **Are any milestones ambiguous, cross-cutting, or touching unfamiliar subsystems?**
   - Yes → escalate to `pipeline-deep`.
   - No → phase-split: detail phase 1 fully, keep later phases coarse. Expand them when reached.

Escalation has priority over phase-split. A clear-but-large task stays in lite; an ambiguous-or-cross-cutting task leaves for deep regardless of milestone count.

### Structured Planning (conditional)

If the spec has 5 or more milestones, additionally invoke `superpowers:writing-plans` to decompose milestones into bite-sized tasks (2-5 min each) with explicit failing test → implementation → verify → commit structure per task. This supplements the compact spec — the spec stays as the source of truth, writing-plans adds granular execution detail.

Present the PRD for approval before implementation.

## Phase 3: Execute

**REQUIRED:** Invoke `superpowers:test-driven-development` before writing implementation code.
**On test failures or unexpected behavior:** Invoke `superpowers:systematic-debugging` before proposing fixes.

Before starting, state the execution proposal:

```md
## Ready to execute
- Start: <first unfinished milestone>
- Cycle: implement → validate → fix → mark done → next
- Stop conditions: blocker, user input needed, deferred danger
```

For each milestone:
1. Make a mini-plan for the milestone
2. Write the failing test first
3. Run it and verify the failure is correct
4. Implement the minimum code to pass
5. Run the milestone validation command
6. Run targeted regression checks from the regression map
7. Run the full relevant test suite when risk is `medium | high` or the changed surface is broad
8. Mark the milestone `[x]` and update Resume State in the design doc

Never write behavior-changing code before a failing test. F-045 scope rule: this applies to behavior-changing code (logic, runtime branches, data transformations, contracts). Pure documentation edits, prompt-text edits, configuration files, and exploratory spikes may be reviewed by diff + targeted verification (e.g. `markdownlint`, `yamllint`, manual reading of a rendered prompt) without a synthetic failing test; do not invent fake tests as ritual.

### Retry Discipline

See `skills/pipeline/references/shared.md` §Retry Discipline.

### Skipped or Deleted Tests Policy

See `skills/pipeline/references/shared.md` §Skipped or Deleted Tests Policy.

If a test is removed, skipped, loosened, or quarantined during execution, document why and add replacement coverage or residual risk before continuing.

## Phase 4: Verify

**REQUIRED:** Invoke `superpowers:verification-before-completion` before claiming work is done.

Run the project-standard verification command. If configured, run `pre-commit run -a`.

### CVE Scan

See `skills/pipeline/references/shared.md` §CVE Scan (baseline).

Применимость для lite: high/critical блокируют merge, medium — accepted risk в отчёте.

Also require a reality check when the task touches a user-facing or integration-facing surface:
- browser smoke check for web UI
- CLI smoke check for tools
- messaging or runtime interaction for bot flows
- contract-level request/response validation for APIs

### Browser And Manual Evidence Acceptance

See `skills/pipeline/references/browser-acceptance.md`.

For lite, read this reference when a small change touches user-facing web UI. Use the lightest practical browser evidence: project Playwright/browser test, `agent-browser`, or a documented manual check. If browser evidence is skipped, record the residual risk in the report.

For user-facing web UI acceptance, the report must name route/page, mobile and desktop viewport or a skip reason, user steps, expected visible result, negative check, and Playwright / agent-browser / project e2e / documented manual browser evidence. Usually this packet is not needed for backend-only work with no visible user surface, but if a route can prove acceptance, use it or record a skip reason.

### Review Quality Lenses

See `skills/pipeline/references/shared.md` §Review Quality Lenses and `skills/pipeline/references/review-quality-lenses.md`.

For lite, use the five minimum lenses for medium-risk, multi-file, user-facing, security, performance, or AI-generated changes, then add any context-specific lens that the task suggests. Do not let the five lenses limit the review.

### Ship Readiness

See `skills/pipeline/references/shared.md` §Ship Readiness and `skills/pipeline/references/ship-readiness.md`.

For lite, this is usually `N/A`. Read it only when a small change still affects a real launch, production runtime, data, pricing, or operations.

Collect evidence while verifying:
- test output
- command output
- example bot/UI/API behavior
- note any safeguard that was skipped and why

### Scope and Diff Audit

See `skills/pipeline/references/shared.md` §Scope and Diff Audit.

For lite this is recommended for small single-file tasks and required for medium-risk or multi-file tasks before reporting.

### Saved Auditor Report

See `skills/pipeline/references/shared.md` §Saved Auditor Report.

For medium-risk or multi-file changes, save a short audit under `docs/reports/` before final handoff. It must compare the approved scope with the actual diff and record verification evidence.

### Skill Behavior Evals and Scorecard

See `skills/pipeline/references/shared.md` §Skill Behavior Evals and Scorecard.

If this task changed skill, prompt, or agent behavior, include clean-context scenarios and scorecard results in the saved report before completion.

Skill-change acceptance gate: final acceptance must include clean-context scenario outcomes, a filled or referenced scorecard, and either measured metrics evidence or an explicit statement that precision, recall, and F1 were not measured with residual risk.

### Skipped or Deleted Tests Policy

See `skills/pipeline/references/shared.md` §Skipped or Deleted Tests Policy.

Verify that any deleted, skipped, weakened, or excluded tests are explained in the report with replacement coverage or residual risk.

## Phase 5: Report and Review

Write `docs/reports/YYYY-MM-DD-<topic>-implementation.md` with:
- what changed
- changed files
- tests added and passed
- regression coverage
- safety choice
- acceptance scenario results
- evidence collected
- skipped safeguards, if any
- reality-check evidence if applicable

Use `skills/pipeline/references/report-status-evidence.md` for the report shape when the change has more than one logical effect, skipped safeguard, or residual risk.

Use the report as the human review checkpoint. Do not end the workflow yet.

### Сводка изменений для пользователя

See `skills/pipeline/references/shared.md` §User Summary Blocks.

Apply the Chat Summary Gate before Phase 6 or any final answer: show the numbered pluses, risks, security, affected behavior, and unaffected behavior blocks in chat even when the saved report is compact.

## Phase 6: Branch Completion

See `skills/pipeline/references/shared.md` §Branch Completion.

Required literal handoff for this mode:
- Before invoking `superpowers:finishing-a-development-branch`, show the User Summary Blocks in the current chat response.
- Use the exact labels from `skills/pipeline/references/report-status-evidence.md`. Do not replace them with `Impact`, `Evidence`, `Risks`, or `Branch Status`.
- A saved report or status file alone is not enough.
- Do not present `Implementation complete. What would you like to do?` until the summary blocks have already been shown.
- invoke `superpowers:finishing-a-development-branch`
- present: `Implementation complete. What would you like to do?`

Применимость для lite: только основной блок (без GitHub Issue Closure subsection — она для deep/hard).

## Escalation to pipeline-deep or pipeline-hard

If mid-run you discover the task is ambiguous, cross-cutting, or research-heavy, escalate — do not restart from scratch, preserve work.

Escalate to `pipeline-deep` when the task becomes ambiguous, cross-cutting, research-heavy, or architecturally unclear.

Escalate to `pipeline-hard` when the task now needs the full advanced workflow, maximum autonomous preparation, external oracle review, Repo Prompt handoff, Codex execution, and explicit deferred-decision handling.

1. **Branch**: rename `pipeline-lite/<topic>` → `pipeline-deep/<topic>` or `pipeline-hard/<topic>`:
   ```sh
   git branch -m pipeline-lite/<topic> pipeline-deep/<topic>
   git push origin :pipeline-lite/<topic>
   git push -u origin pipeline-deep/<topic>
   ```
2. **Design doc**: keep the existing `docs/plans/YYYY-MM-DD-<topic>-design.md`. Do not recreate. Add a new section `## Discovery Gap` at the top explaining what turned out to be unclear and why lite was insufficient.
3. **Resume State**: preserve completed milestones marked `[x]`. New deep-mode milestones are appended, not renumbered. Completed work in lite counts toward deep's definition of done.
4. **Resume point**: switch to `pipeline-deep` or `pipeline-hard` skill. For deep, continue from **Phase 2 (Context Gathering and Triage)**. For hard, continue from the earliest phase that has not already been satisfied by lite evidence. Lite's Phase 0 + Phase 1 output maps to the target mode's discovery/intake work — do not redo discovery if it is still valid.

The escalation exists to preserve already-done work, not to reset it.

## Built-In Rules

- Prefer fast local context over heavy discovery
- Keep the spec short but explicit
- Keep safeguards lightweight and explicit for small tasks
- TDD is mandatory
- Verification is mandatory
- Mirror the language of the user's request in all artifacts
- Update existing design docs instead of creating duplicates
- Escalate to `pipeline-deep` or `pipeline-hard` if the task outgrows lite — see "Escalation to pipeline-deep or pipeline-hard" for the preserve-work procedure
