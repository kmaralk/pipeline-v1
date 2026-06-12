---
name: pipeline-deep
description: "Use when a task starts from a raw idea or has product, UX, contract, research, or architecture uncertainty before implementation. Also use for deep planning, risky handoffs, heavy/тяжелый/autonom+heavy/autonomous heavy/ok C4 A3, or Codex-heavy green-tests-only work; TAR required."
---

# Pipeline Deep

Full discovery-to-delivery workflow for high-uncertainty work. Compared to `pipeline-lite`, this mode adds explicit failure analysis, invariants, rollback thinking, and observability planning.

Discovered tasks and run-control inheritance: read `skills/pipeline/references/run-control-inheritance.md` before accepting or handing off work found during review, testing, implementation, resume, or oracle review. Do not downgrade accepted child work from the parent `run_control`. Do not silently implement discovered new features.

Premortem plan review: read `skills/pipeline/references/premortem-plan-review.md` before accepting a medium/high-risk spec, plan, or autonomous/Codex-heavy handoff. For deep, run it in Phase 4 before spec approval and before Phase 5 Planning and Handoff. It does not reset the selected `run_control`.

## Immediate First Response Gate

If either run control is missing, ask both menus in the first response before Phase 0, Phase 1, file reads, branch work, or discovery artifacts:

Before or alongside Run Control Choices, include any triggered first-response packets that are clear from the user request. Run Control Choices must not suppress required first-response packets; for example, a large existing cross-cutting task still needs the Code Routing Map packet before waiting for run-control answers.

Alias normalization before asking:
- `heavy`, `режим heavy`, `heavy mode`, `тяжелый режим`, `autonom+heavy`, `autonomous heavy`, and `autonom heavy` mean `C4 A3` unless the user explicitly names a different `A#`.
- `ok` means `C4 A3`.
- Do not ignore a bare `heavy` by falling back to memory or older defaults.

```text
Run Control Choices:

Кто работает? Ответ: C1-C4
C1 Один основной агент
C2 Primary + Secondary checkpoints (legacy: Claude-main + Codex checkpoints)
C3 Dual-head quality
C4 Heavy executor + Guardrail reviewer (Recommended; legacy: Codex-heavy + Claude guardrails)

Автономность? Ответ: A1-A4
A1 Interactive
A2 Guided autonomous
A3 Full autonomous (Recommended)
A4 Overnight

Опционально:
X Cross-check в начале
P Premortem plan review перед реализацией
-P Skip optional premortem если задача low-risk

Быстрый ответ:
Ответь коротко: `C# A#` (+ `X` и/или `P` если нужны)
- `ok` = `C4 A3`
- `heavy` = `C4 A3`
- `quality` = `C3 A2`
- `night` = `C4 A4`
- `heavy P` = `C4 A3 P`

Подсказка:
- `C` = collaboration
- `A` = autonomy
- `X` = cross-check
- `P` = premortem plan review
```

Do not silently apply defaults before the user sees the recommended choices. Use defaults only after the user accepts the recommended defaults.
If the user answers legacy digits like `4 2`, treat them as `C4 A2`, then record normalized state values.

If the user asks for Codex-heavy and says Claude should only check green tests, state that Claude guardrails include Test Adequacy Review; green tests alone are not enough.

## When to Use

Use when:
- The request begins as a raw idea
- Product behavior, UX, contracts, or architecture are not settled
- External research would materially improve decisions
- The cost of building the wrong thing is high
- Multiple surfaces, integrations, or subsystems are involved

If discovery collapses the task into a small, local change, execution may downgrade to `pipeline-lite`.

## Inputs

Start from either:
- a raw idea from the conversation
- a backlog entry
- a rough note, issue, spec fragment, or failing scenario

## First Response Failure Packets

Canonical wording, trigger table, and minimum fields: read `skills/pipeline/references/first-response-packets.md` before composing the first response when any trigger below appears (F-020 dedup executed 2026-06-09).

Include the relevant first response packets before implementation steps when a trigger appears:

- Browser evidence packet — user-facing frontend/UI/page/form/browser-route/user-journey work.
- Plan repair packet — a draft, prompt, or plan is structurally wrong.
- Premortem plan review packet — medium/high-risk plans, broad feature/refactor work, launch/pricing/contract/migration decisions, or Codex-heavy/autonomous execution.
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

## Language Rule

See `skills/pipeline/references/shared.md` §Language Rule.

## Phase -0.5: State Detect & Resume

**MANDATORY. Before Phase 0.**

Parse `<topic>` from the user request, then check for existing state:

```bash
ls docs/plans/*-<topic>-state.json 2>/dev/null
```

**Decision tree:**

1. **No state files** → new run. Create state.json at end of Phase 0, continue.
2. **One file, `current_phase == "final"` AND `phases.phase_9_branch_completion.status == "completed"`** (deep finalization rule per `shared.md §State Persistence Schema v1`; the schema has no top-level `status` field — finalization is observed via `current_phase` plus the final phase's status) → ask user: "Topic '<topic>' already completed on <date>. Run a new pipeline with today's date? (да/нет)".
3. **One file, `current_phase != "final"` OR `phases.phase_9_branch_completion.status != "completed"`** → parse state, show the Resume UX below, ask user action.
4. **Two or more state files** → list all with date + last_phase, ask user which to resume, or "new".

### Resume UX (Russian, mirrors Language Rule)

```
Нашёл незавершённый pipeline-deep для темы "<topic>":

  <checkbox> Phase 0 — backup (<status>)
  <checkbox> Phase 0.5 — rigor (<status>)
  <checkbox> Phase 1 — discovery (<status>)
  <checkbox> Phase 1.5 — context-driven practices (<status>)
  <checkbox> Phase 2 — context (<status>)
  ...
  <checkbox> Phase 6 — execute (<status>)
      <checkbox> M1 — <title>
      <checkbox> M2 — <title>
      ...

Последнее обновление: <timestamp> (<relative>)
Блокеры: <list or нет>

Что делать?
  [1] Продолжить с <next_step> (рекомендовано)
  [2] Начать заново (старый state → <file>.abandoned-<timestamp>.json)
  [3] Только посмотреть дизайн-док (не запускать pipeline)
```

Checkbox mapping: ✓ completed, ⟳ in_progress, ⊘ skipped, ○ pending, ✗ failed.

### Edge cases

- **Branch mismatch**: if `state.branch_name` does not match current git branch → warn user, ask "switch / continue / abort".
- **Orphaned milestones**: milestone ID in state but absent from design-doc → mark `orphaned`, alert.
- **Stale state**: `last_updated_at > 14 days ago` → warn "state may be stale, continue?".
- **attempts >= 3** on a milestone → do NOT auto-retry; show previous error + offer retry/skip/decompose/abort.

### Resume execution

- Skip all phases with `status = completed | skipped` (no re-work).
- For `status = in_progress` phase → resume at first `in_progress` or `pending` milestone.
- Phase 0 GitHub Backup is skipped if `completed` (branch and backup already exist).
- Update `last_updated_at` after resume starts.

## Phase 0: Branch And Worktree Policy

**MANDATORY before repository file edits.**

1. Run `git status --short --branch`.
2. Read `skills/pipeline/references/branch-worktree-policy.md`.
3. Apply the `pipeline-deep` mode default from that reference.
4. For autonomous execution, broad handoff, or parallel agents, also read `skills/pipeline/references/worktree-agent-isolation.md`.
5. Record branch/worktree choice and any deferred remote backup as residual risk in state/report.

### New Project Check

Если проект новый (нет `CLAUDE.md` с блоком `Agent Operations Config`, нет GitHub Project, нет labels) — **спросить пользователя, запускать ли `project-init` skill** перед продолжением:

> «Проект выглядит новым — в `CLAUDE.md` нет блока `Agent Operations Config`. Запустить `project-init`, чтобы создать GitHub Project, labels, canonical-файлы и config-блок? (да / нет / позже)»

Поведение:
- **да** → invoke `project-init` skill, дождаться завершения, затем продолжить с остальными шагами Phase 0
- **нет** или **позже** → пропустить, продолжить. Не спрашивать повторно в этой сессии
- проект уже настроен (есть `Agent Operations Config`) → пропустить проверку молча, без вопроса

Если GitHub-репозитория у проекта ещё нет — перед `project-init` создать его: `gh repo create <owner>/<name> --private --source=. --push`. `<owner>` взять из `routing:` секции `CLAUDE.md` (пути вида `<owner>/<repo>`). Если в `CLAUDE.md` нет `routing:` или там несколько разных owner — уточнить у пользователя. Всегда подтверждать имя репо и owner перед созданием.

Docker/runtime decision: when `project-init` runs, make sure its Docker / container preference answer is captured before continuing. Do not silently add Docker files; the project-init answer decides whether to create no container files, a Dockerfile, docker-compose, or a devcontainer later in the implementation plan.

### Worktree Agent Isolation

For medium/large tasks, autonomous work, or parallel workers, use `skills/pipeline/references/worktree-agent-isolation.md`.

- Apply its GitHub Issue Policy: issue recommended for medium/large or autonomous deep work; if skipped, record `issue_skipped: <reason>` in state/report.
- Before dispatching parallel agents, write the File Ownership Plan.
- Give every worker the Worker Handoff Template with branch/worktree, allowed files, tests, and stop conditions.
- The orchestrator merges one worker result at a time and runs targeted checks after each merge.

### GitHub Issue Context (optional)

Если задача связана с GitHub Issue — перед началом работы invoke `gh-issues` skill:
1. Загрузить AI Session Context из комментариев issue (если есть предыдущий прогресс):
   ```bash
   gh issue view <NUMBER> --json comments --jq '.comments[] | select(.body | contains("AI-CONTEXT")) | .body'
   ```
2. Привязать ветку к issue: `gh issue develop <NUMBER> --checkout`
3. Пометить issue как in-progress: `gh issue edit <NUMBER> --add-label in-progress`

### State init

**Read-only audit carve-out (F-044):** if the task is a pure read-only audit / inspection / discovery pass that produces no repository mutations beyond a final report, state.json + git commit are NOT required. Maintain run state as chat-local state (the orchestrator's working memory of phase status and open questions) and skip the per-phase `git add state.json` commits. State persistence is required only for write-enabled multi-turn execution where resume across context windows is plausible.

After Phase 0 branch/worktree decision, initialize state.json (write-enabled runs only):
- Create `docs/plans/<DATE>-<topic>-state.json` with schema v1 (см. `shared.md §State Persistence Schema v1`).
- Fields at init: `started_at`, `last_updated_at`, `branch_name`, `design_doc`, `current_phase = "phase_0_5_rigor"` (the first phase that is not yet completed), `phases.phase_0_backup.status = "completed"`, `finished_at = now`.
- Initialize `open_questions: []` for unresolved questions that must survive context resets.
- Persist `run_control` (collaboration_profile, autonomy, cross_check_initial, premortem_plan_review) into state.json at creation time under `orchestration.*`, using the values held in chat state since they were collected. State.json must never exist without a non-empty `orchestration.collaboration_profile` and `orchestration.autonomy`.
- Atomic write (`.tmp` → `fsync` → `mv`), then `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc is not yet created) + `git commit -m "pipeline: state initialized"`.

### Baseline Gates

See `skills/pipeline/references/shared.md` §Baseline Gates.

Применимость для deep: mandatory. Все 3 стека (Python/Node/Go) обязательны при наличии соответствующих lockfile. Результат фиксировать в отчёте Phase 8 под заголовком `Baseline Gates Result`. Если инструмент не установлен — warning + запись в residual risks.

## Phase 0.5: Rigor Level

**REQUIRED:** Set rigor level before any work begins.

Invoke `/dushno 5` — medium challenge level. Question non-obvious decisions, but do not block progress on minor trade-offs.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_0_5_rigor.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_1_discovery"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_0_5_rigor completed"`

## Phase 1: Discovery

**REQUIRED:** Invoke `superpowers:brainstorming` to explore intent, requirements, and design before committing to a direction.

Turn the input into a discovery memo containing:
- problem statement
- desired outcome
- non-goals
- constraints
- open questions
- risks
- risk level
- affected surfaces
- success criteria
- failure modes
- initial invariants

Persist unresolved blockers in `state.json.open_questions`. Remove or mark each item resolved when answered, deferred, or made irrelevant by scope changes.

Ask clarifying questions one at a time until the problem is shaped well enough to evaluate approaches.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_1_discovery.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_1_5_practices"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_1_discovery completed"`

## Run Control Choices

Before Phase 0, Phase 1, or any tool work, resolve the two independent run controls unless the user already specified both:

1. `Model Collaboration Profile` — who participates.
2. `Autonomy Level` — how independently agents work without the human operator.

Use:

- `skills/pipeline/references/collaboration-profiles.md`
- `skills/pipeline/references/autonomy-levels.md`
- `${CLAUDE_SKILL_DIR}/../pipeline/references/collaboration-profiles.md` when resolving the bundled reference from an installed personal skill.
- `${CLAUDE_SKILL_DIR}/../pipeline/references/autonomy-levels.md` when resolving the bundled reference from an installed personal skill.

If either run control is missing, ask both menus in the first response. Do not silently apply defaults before the user sees the recommended choices.

Use defaults only after the user accepts the recommended defaults:

Use the compact Run Control Choices menu from the first-response gate at the top of this skill (single inline copy; canonical aliases and parse rules: `skills/pipeline/references/collaboration-profiles.md` and `skills/pipeline/references/autonomy-levels.md`).

Record the choices in state under `orchestration.collaboration_profile`, `orchestration.cross_check_initial`, `orchestration.premortem_plan_review`, and `orchestration.autonomy`.
If the user answers legacy digits like `4 2`, treat them as `C4 A2`, then record normalized state values.
Parse exact tokens in this order: if the answer includes exact token `-P`, record `premortem_plan_review=skipped` only for optional premortem and do not bypass a mandatory high-risk safety gate without a residual-risk note; else if it includes exact token `P`, record `premortem_plan_review=forced`; else keep `premortem_plan_review=auto`.

Defaults:

- `collaboration_profile = codex_heavy_claude_guardrails`
- `cross_check_initial = false`
- `premortem_plan_review = auto`
- `autonomy = full_autonomous`

For `pipeline-deep`, keep profiles 3/4 and `overnight` available, but recommend escalation to `pipeline-hard` when the run needs the full advanced workflow or night protocol.

If `cross_check_initial = true`, use it as a one-shot early research/spec check around Phase 3/4; do not run it after every milestone.
If `premortem_plan_review = forced`, run Premortem Plan Review at the mode placement even if automatic risk triggers would skip it. If `premortem_plan_review = auto`, run it only when `skills/pipeline/references/premortem-plan-review.md` says the task risk/shape requires it.

## Phase 1.5: Context-Driven Practices

**Strictness for deep: AUTO-ON.** Все применимые практики включаются по умолчанию. Пользователь может убрать конкретные через `-N`, но каждое убирание фиксируется в residual risks.

Цель — автоматически подтянуть дополнительные artifacts и чек-листы, которые нужны именно этой задаче (threat-model, idempotency, migration plan и т.д.), не перегружая spec лишним.

### Шаги

1. Прочитать `skills/pipeline/references/practices-index.md` (лёгкий индекс, ~50 строк).
2. Для каждой строки индекса — проверить триггеры в два шага:
   - **Step A — exact match (0 tokens):** keyword из `keywords` есть в discovery memo Phase 1 ИЛИ glob из `paths` совпадает с affected surfaces или файлами из Phase 2 context pack.
   - **Step B — semantic fallback (small AI call):** если Step A не сработал — запросить короткий AI-верификатор по `semantic` строки индекса.
   - Practice активируется, если хотя бы один шаг сказал «да».
3. Для КАЖДОЙ активированной practice — открыть `skills/pipeline/references/practices-full.md` на якоре `#<id>` и прочитать ТОЛЬКО её блок. Не загружать файл целиком.
4. Проверить `prerequisites` (из прочитанного блока). Если не выполнены — practice активна, но добавить в spec пункт "prerequisites not met → <что создать>".
5. Показать пользователю автоматически составленный набор:

```
Context-Driven Practices (auto-on):

  [✓] threat-model          — trigger: keyword "auth" в brief
  [✓] idempotency           — trigger: keyword "webhook" в brief
  [✓] eval-driven-ai        — trigger: path "skills/**/SKILL.md"
  [ ] slo-perf-budget       — не активировалось

Действия:
  Enter       принять всё (добавить в spec Phase 4)
  -N,-M       убрать номера (причина пойдёт в residual risks)
  +N          вручную добавить по id
  detail N    показать полный текст practice
```

6. Для каждой активной practice — добавить её `Add to Phase 4 (spec)` / `Add to Phase 6 (execute)` / `Add to Phase 7 (verify)` секции в design-doc и чек-лист верификации.

### State update

Записать в state.json в блоке текущей phase:

```json
"phase_1_5_practices": {
  "status": "completed",
  "finished_at": "<ISO>",
  "activated": ["<id1>", "<id2>"],
  "user_removed": ["<id3>"],
  "semantic_checks_run": <N>
}
```

Also set top-level `current_phase = "phase_2_context"`.

Atomic write, `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_1_5_practices completed"`.

### Output

В spec Phase 4 появится секция `## Active Practices` со списком активированных id и краткой причиной активации. Если пользователь убрал какую-то — она попадает в `## Residual Risks` отчёта Phase 8.

## Phase 2: Context Gathering and Triage

**REQUIRED:** При сборе контекста через 2+ независимых домена (e.g., code paths + tests + docs) invoke `superpowers:dispatching-parallel-agents`. Для одного домена — serial gathering.

### Context Hygiene Gate

See `skills/pipeline/references/shared.md` §Context Hygiene Gate.

Before gathering context, name the allowed docs, code paths, skills, MCP servers, and tools for this phase. Keep command output targeted and summarize noisy logs.

Собирать контекст:
- relevant code paths
- existing tests
- current contracts and schemas
- docs and operational notes
- adjacent systems likely to regress

Then synthesize findings into one context pack:
- selected files
- module map
- constraints
- unknowns
- recommended next questions

### Lightweight Memory Bank

See `skills/pipeline/references/shared.md` §Lightweight Memory Bank.

For deep mode, check `docs/agent-memory/index.md` or the project's existing memory index during context gathering if present. Add a memory note only when the run discovers reusable project knowledge, repeated agent failure, or a known-good command.

### Tool and Model Routing Matrix

See `skills/pipeline/references/shared.md` §Tool and Model Routing Matrix.

Use the matrix to justify planning/research, implementation, audit/review, browser acceptance, AI trace debugging, and knowledge lookup tools before choosing heavier tooling.

### CLI Recipes and Tool Failure Log

See `skills/pipeline/references/shared.md` §CLI Recipes and Tool Failure Log.

When a command or tool handoff fails because of syntax, timeout, env, or context mismatch, preserve the known-good command and the failure mode in the report or project memory.

### Prototype And Trace Practices

See `skills/pipeline/references/shared.md` §Prototype And Trace Practices and `skills/pipeline/references/prototype-trace.md`.

For deep, require a prototype spike when discovery finds uncertain tool syntax, an API contract, migration shape, or risky implementation path that would otherwise make the plan speculative. For AI-app debugging, name the trace evidence to inspect before changing prompts or agent instructions.

### Planner Generator Evaluator Roles

See `skills/pipeline/references/shared.md` §Planner Generator Evaluator Roles and `skills/pipeline/references/planner-evaluator.md`.

For deep, use planner/generator/evaluator separation for large, high-risk, broad, or AI-generated implementation. Keep the planner and evaluator roles separate from the generator when delegation or Codex batching is used.

### Skill vs Runbook vs CLI Decision Rule

See `skills/pipeline/references/shared.md` §Skill vs Runbook vs CLI Decision Rule.

Before creating or changing a skill, decide whether the lesson belongs in a runbook, CLI, CLI + skill pair, skill, or global instructions.

### File-First Knowledge Before RAG

See `skills/pipeline/references/shared.md` §File-First Knowledge Before RAG.

Use local files and `rg` first for knowledge lookup. Do not propose RAG unless file-first retrieval has a recorded failure criterion.

### Source Grounding

See `skills/pipeline/references/shared.md` §Source Grounding and `skills/pipeline/references/source-grounding.md`.

Use this during context gathering and spec work when the plan depends on an external library, API, SDK, framework, CLI, protocol, vendor service, or versioned behavior. Check local dependency versions, official docs, and Context7 when available before writing API-specific plans or examples from memory.

### AI Minimalism Guardrails

See `skills/pipeline/references/ai-minimalism.md`.

For deep mode, include the Minimal Diff Packet and Reuse-Before-Build in the spec or implementation handoff when the plan may create broad AI-generated code. Run the Post-Green Simplify Pass before review for broad, multi-file, or custom-code diffs. Use Context Rule Audit for AGENTS, CLAUDE, SKILL, prompt, or context-rule changes.

### Idea To Ship Stage Gates

See `skills/pipeline/references/shared.md` §Idea To Ship Stage Gates and `skills/pipeline/references/idea-to-ship-gates.md`.

For deep mode, use Raw Idea Intake during discovery for rough ideas, What-before-How PRD Gate before spec, Minimal Architecture Pack before planning/code handoff, Bug Fix Record for non-trivial fixes, and Chat Summary Gate before branch completion or final handoff.

### Skill Packaging and Portability

See `skills/pipeline/references/shared.md` §Skill Packaging and Portability and `skills/pipeline/references/packaging.md`.

Use this when the task changes pipeline skill packaging, `agents/openai.yaml`, active-copy sync, validators, third-party skill installation/review, or cross-agent compatibility assumptions.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_2_context.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_3_research"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_2_context completed"`

## Phase 3: Research

Run external research when local context is insufficient.

Typical triggers:
- UX uncertainty
- domain uncertainty
- third-party API or integration behavior
- standards, competitors, workflows, or policy constraints

Capture a research memo with:
- question asked
- sources used
- key findings
- trade-offs
- recommendation
- unresolved disagreements

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_3_research.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_4_spec"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_3_research completed"`

## Phase 4: Spec

### Spec Strategy Choice

Before writing the spec, offer the user the plain-language choice from `orchestration.md §Before spec` (entry under `shared.md §Codex-Orchestrated Planning and Execution`).
Detailed reference: `skills/pipeline/references/orchestration.md` §Codex-Orchestrated Planning and Execution.

Record the selected strategy in state:
- `current_model` for option A
- `cross_review` for option B
- `codex_details` for option C

If option C is selected:
1. Current model writes a thin spec first: goal, non-goals, invariants, contracts, risks, acceptance.
2. Run the Codex preflight and Codex Invocation Ladder route selection from `shared.md §Codex-Orchestrated Planning and Execution`.
3. Ask Codex to add implementation details only: likely files, tests, edge cases, technical risks, open questions.
4. Current model reviews Codex output, ratifies decisions, and writes final spec.

Do not let Codex make high-stakes product, architecture, security, or scope decisions. Codex proposes; current model decides.

Write `docs/plans/YYYY-MM-DD-<topic>-design.md`.

If a design doc for this topic already exists, update it — preserve completed milestones, decisions, and assumptions. Do not overwrite progress.

Required sections:
- context and problem
- proposed approach and rejected alternatives
- risk level and failure-mode review
- invariants
- affected components
- contracts and schema changes
- UX or flow notes where relevant
- rollback or fallback plan
- observability plan
- input validation checklist (baseline — per external input)
- active practices (from Phase 1.5 — injected automatically)

### Input Validation Checklist

See `skills/pipeline/references/shared.md` §Input Validation Checklist.

### Assumptions

See `skills/pipeline/references/shared.md` §Assumptions Section.

### Grounding Required

See `skills/pipeline/references/shared.md` §Grounding Required.

### Milestones

See `skills/pipeline/references/shared.md` §Milestones Template.

Deep-режим использует полную форму с секцией `### Tasks` под каждым milestone.

### Verifiable Acceptance Criteria

See `skills/pipeline/references/shared.md` §Verifiable Acceptance Criteria.

### Ambiguity Scanner

See `skills/pipeline/references/shared.md` §Ambiguity Scanner.

Run this before presenting the spec. Resolve real ambiguity as a decision, `state.json.open_questions`, deferred decision, or residual risk.

### Spec Regeneration Rule

See `skills/pipeline/references/shared.md` §Spec Regeneration Rule.

If the spec or downstream plan depends on hidden chat context, misses a contract, or has unresolved ambiguity, fix the source artifact and regenerate the downstream artifact before execution.
Prefer the source artifact instead of stacking follow-up chat corrections.

### Premortem Plan Review

Read `skills/pipeline/references/premortem-plan-review.md`.

For deep, run it in Phase 4 before spec approval and before Phase 5 Planning and Handoff. Use the failure-frame review to find concrete plan holes, accept only the blocking mitigations that belong in current scope, record deferred holes, and keep the selected `run_control` sticky for accepted work.

### Resume State

See `skills/pipeline/references/shared.md` §Resume State Block.

### Phasing Rule

If the task has many milestones (7+), split into phases. Detail the current phase fully, keep later phases coarse. Expand them when reached.

### Definition of Done

End the spec with an explicit definition of done section.

Present the spec for approval before planning or implementation.

### Clean-Context Plan Review

See `skills/pipeline/references/shared.md` §Clean-Context Plan Review.

For deep mode, run a fresh-context review after spec and before planning handoff. Fix blocking findings around scope, contracts, data, UI/API behavior, tests, or acceptance. Record rejected nitpicks with rationale if they are mentioned in the report.

### Skill Behavior Evals and Scorecard

See `skills/pipeline/references/shared.md` §Skill Behavior Evals and Scorecard.

For skill, prompt, or agent-workflow changes, the spec must name the clean-context scenarios, scorecard evidence, and `skills/pipeline/evals/metrics.md` update plan that will prove the change improved behavior.

### Downstream Contract Handoff

Read `skills/pipeline/references/contract-handoff.md`.

For deep mode, use this during context gathering and spec work when producer/consumer surfaces differ. If backend, frontend, API, worker, data, prompt-output, or parser ownership is split, the spec must include the handoff before planning starts.

If browser research is used in this phase, record that browser evidence is not oracle judgment unless an independent reviewer judges it.

### Cross-Agent Plan Review (optional)

После написания spec и перед переходом к планированию — предложить ревью другой моделью.

See `skills/pipeline/references/shared.md` §Cross-Agent Review Template.
Detailed reference: `skills/pipeline/references/orchestration.md` §Cross-Agent Review Template.

Параметры для этого вызова:
- `<ARTIFACT>` = `plan`
- `<ENTRY_PHASE>` = Phase 4 (Spec)
- `<EXIT_PHASE>` = Phase 5 (Planning and Handoff)
- `<REVIEW_FOCUS>` = `architectural issues, security concerns, race conditions, missing edge cases, contract violations`
- `<DOC_OR_DIFF>` = путь к `docs/plans/<design-doc>.md`

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_4_spec.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_5_planning"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_4_spec completed"`

## Phase 5: Planning and Handoff

### Context Hygiene Gate

See `skills/pipeline/references/shared.md` §Context Hygiene Gate.

Before writing or delegating the implementation plan, reduce the context pack to the files, contracts, tests, and decisions needed for execution. Do not pass exploratory notes unless they affect implementation.

### Ambiguity Scanner

See `skills/pipeline/references/shared.md` §Ambiguity Scanner.

Run this on the implementation plan before handoff. Do not dispatch work if a milestone still contains unresolved "or/maybe/TBD" style choices.

### Planning Strategy Choice

Before writing the implementation plan, offer the user the plain-language choice from `orchestration.md §Before planning` (entry under `shared.md §Codex-Orchestrated Planning and Execution`).

Record the selected strategy in state:
- `current_model` for option A
- `cross_review` for option B
- `codex_tdd_plan` for option C

If option C is selected:
1. Run Codex preflight if it was not already run in Phase 4.
2. Give Codex the approved spec and context pack.
3. Ask Codex for a detailed TDD implementation plan: tasks, tests, file paths, verify commands, stop conditions.
4. Current model reviews the plan for scope, safety, dependencies, and missing tests before execution.

**REQUIRED:** Invoke `superpowers:writing-plans` to structure the implementation plan before execution.

### Pointer rule

Plan **не дублирует** milestone содержимое из spec. Для каждого milestone (по ID) plan добавляет **только execution-level детали**:
- exact file paths (или likely files)
- test file names и test case names
- exact shell-команды для верификации
- regression map (какие тесты прогнать из других модулей)
- observability checks
- what must not change

Goal / Tasks / Validation берутся из spec by reference (milestone ID). Нет дубликата.

### must_haves Contract (REQUIRED for medium/high risk milestones)

Each medium/high-risk milestone MUST include a `must_haves` block in the design-doc OR implementation plan before execution handoff. This block is the acceptance contract for what must be observably true after the milestone lands.

Use yaml-in-markdown. The block has three required keys:
- `truths`: observable post-conditions that can be checked after implementation.
- `artifacts`: expected file artifacts, each with a `path` and `contains` pattern.
- `forbidden`: banned strings or patterns that must not appear in changed files.

Concrete example:

```yaml
must_haves:
  truths:
    - "Phase 5 contains must_haves Contract before handoff bundle"
  artifacts:
    - path: skills/pipeline-deep/SKILL.md
      contains: "Phase 7 verifies each must_haves entry"
  forbidden:
    - "debug-only"
```

Backward compatibility: low-risk milestones MAY skip this block with an explicit `must_haves: skipped -- <reason>` record in design-doc `residual_risks`. Old design-docs without `must_haves` remain valid for low-risk tasks. Phase 5 returns failure, not warning, only if a medium/high-risk milestone lacks `must_haves`.

Phase 7 verifies each `must_haves` entry: `truths` via grep/curl/test commands, `artifacts` via `grep <contains> <path>`, `forbidden` via `grep -E '<patterns>' <changed-files>`. Any failed check = milestone NOT done.

**F-024 anti-gaming rule:** every medium/high-risk milestone must include at least one **behavioral or artifact-level check that would fail on a known bad implementation** (a pytest/curl/runtime assertion that exercises actual behavior, or a structural check on a generated artifact such as line count, JSON schema validation, or referenced symbol resolution). `grep <contains>` alone is not sufficient — the agent can satisfy a pure substring check by writing the string without producing correct behavior. The must_haves block lists both: the substring/grep checks AND at least one behavioral check.

Prepare an implementation handoff bundle containing:
- approved spec
- context pack
- exact files or likely files
- tests to write first
- verification commands
- edge cases
- acceptance surface
- invariants to preserve
- rollback notes
- observability checks
- what must not change

The implementation plan must be detailed enough for an autonomous coding agent to execute without guessing.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_5_planning.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_6_execute"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_5_planning completed"`

## Phase 6: Execute

**REQUIRED:** Invoke `superpowers:test-driven-development` before writing implementation code.
**On test failures or unexpected behavior:** Invoke `superpowers:systematic-debugging` before proposing fixes.

### Context Hygiene Gate

See `skills/pipeline/references/shared.md` §Context Hygiene Gate.

Before execution, state which files, commands, tools, and skills are in scope for the first milestone or batch.

### Autonomous Backup Gate

See `skills/pipeline/references/autonomy-safeguards.md` §Autonomous Backup Gate.

Apply this before autonomous, Codex-batched, or subagent-driven execution.

### Pre-Autonomy Context Freeze And Compact Gate

See `skills/pipeline/references/autonomy-safeguards.md` §Pre-Autonomy Context Freeze And Compact Gate.

Apply this before full_autonomous, overnight, Codex-batched, or subagent-driven execution. Compact only after the durable task brief, open questions, ownership, verification, stop conditions, backup ref, and current state are written.

### Execution Profile And Autonomy

Use the `Model Collaboration Profile` and `Autonomy Level` already recorded in Run Control Choices.

Do not ask the old execution-phase autonomy menu again.

Apply `skills/pipeline/references/collaboration-profiles.md` for profile-specific Codex/checkpoint behavior, and `skills/pipeline/references/autonomy-levels.md` for ask/default/stop behavior.

If no run controls exist because this is a resumed legacy state, re-ask the user via the Run Control Choices menu before proceeding (per `skills/pipeline/references/run-control-inheritance.md`). Do not silently default to `codex_heavy_claude_guardrails` + `full_autonomous`; the silent legacy default is forbidden because resumed legacy runs do not consistently match the heavy-executor profile.

If planning strategy is `codex_tdd_plan` or executor is Codex, use `shared.md §Codex-Orchestrated Planning and Execution` for Codex Invocation Ladder route selection, batch size, prompt contract, stop conditions, and per-batch verification.

Before starting, state the execution proposal:

```md
## Ready to execute
- Start: <first unfinished milestone>
- Cycle: implement → validate → fix → mark done → next
- Validation: milestone checks + regression map
- Autonomy: <interactive | guided_autonomous | full_autonomous | overnight>
- Stop conditions: blocker, user input needed, deferred danger
```

Implement with strict TDD per milestone:
1. safety checkpoint
2. milestone mini-plan
3. failing test
4. minimal implementation
5. run milestone validation command
6. targeted regressions
7. full tests when risk is `medium | high`
8. mark milestone `[x]` and update Resume State

Continue autonomously until all milestones are complete or a real blocker appears.

### Milestone state update

After marking `[x]` in design-doc (TDD step 8):
- Read state.json
- Set `phases.phase_6_execute.milestones.M<N>.status = "completed"`, `finished_at = <ISO now>`
- On retry: increment `attempts`, store `last_error` (short string) on failure
- Atomic write (write `.tmp` → fsync → rename)
- `git commit -m "pipeline: M<N> completed"`

### Subagent Execution (conditional default)

See `skills/pipeline/references/autonomy-safeguards.md` §Independent Parallel Execution Default.

**Run-control gate (F-033):** default-to-subagents is OFF unless `collaboration_profile` index ≥ 3 (C ≥ 3, i.e. C3 dual-head quality or C4 heavy executor + guardrail reviewer) AND `autonomy` index ≥ 2 (A ≥ 2, i.e. guided_autonomous, full_autonomous, or overnight). C1 (solo primary) and A1 (interactive) keep serial TDD with explicit ask-before-major-step behavior.

**Default (given run-control gate passes):** если Codex-вариант не выбран, platform and governing instructions allow subagents, и выполняются ОБА условия ниже — по умолчанию запускаем subagent-driven-development (параллельная реализация). Иначе — serial TDD (шаги 1-8 выше).

**Условие активации (оба обязательны):**

1. **`plan.milestones >= 4`** — масштаб оправдывает параллелизм (overhead запуска субагентов меньше выигрыша).
2. **Milestones largely independent** — каждое из трёх:
   - **No shared in-memory/on-disk state:** нет состояния, которое один milestone мутирует, а другой читает в том же запуске.
   - **No ordering dependencies:** milestone M2 не требует результата M1 (контракт, файл, схема, API-эндпоинт). Если требует — они зависимы, serial.
   - **No shared write targets:** нет файлов, в которые пишут два+ milestone (кроме чисто append-only журналов — их можно считать независимыми).

При обоих `true` → invoke `superpowers:subagent-driven-development`: dispatch свежий субагент на каждый milestone с двухэтапным ревью (spec compliance + code quality). Каждый субагент следует TDD в своём чистом контексте.

Before dispatching, apply `shared.md §Subagent Dispatch Contract` to every subagent prompt. If owner files, contracts, verification commands, or stop conditions cannot be written, run serial TDD instead.

**Manual override (в execution proposal):**

- `--serial` — форсировать serial TDD даже при выполненных условиях (например, когда пользователь хочет пошагово видеть прогресс).
- `--subagents` — форсировать subagent-driven даже при неполных условиях (на свой риск; пользователь принимает риск конфликтов).
- `--codex-batched` — использовать Codex batch execution по правилам `shared.md §Codex-Orchestrated Planning and Execution` (только после preflight и явного выбора пользователя).

Если override не указан — применяется default по условиям выше. Состояние выбора (`execution_mode: "serial" | "subagent-driven" | "codex-batched"`) фиксируется в state.json в блоке `phase_6_execute` перед началом первого milestone.

### Retry Discipline

See `skills/pipeline/references/shared.md` §Retry Discipline.

### Unattended Attempt Budget Stop Rule

See `skills/pipeline/references/autonomy-safeguards.md` §Unattended Attempt Budget Stop Rule.

Apply this only for `full_autonomous` or `overnight`. Interactive and guided-autonomous runs stop and ask after the retry budget instead of silently skipping.

### Skipped or Deleted Tests Policy

See `skills/pipeline/references/shared.md` §Skipped or Deleted Tests Policy.

If a test is removed, skipped, loosened, or quarantined during execution, document why and add replacement coverage or residual risk before continuing.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_6_execute.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_7_acceptance"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_6_execute completed"`

## Phase 7: Acceptance

**REQUIRED:** Invoke `superpowers:verification-before-completion` before claiming work is done.

Verification is not complete until all three are done:
- code-level verification: tests, linters, formatters, pre-commit if configured
- real-environment acceptance: browser,  messaging platform, CLI, API, or integration smoke/e2e checks as appropriate
- **CVE scan (baseline):** см. `skills/pipeline/references/shared.md` §CVE Scan (baseline). Для deep: high/critical блокируют merge, medium — accepted risk с обоснованием.

### Browser And Manual Evidence Acceptance

See `skills/pipeline/references/browser-acceptance.md`.

For deep mode, apply this when the spec changes a real user journey, frontend state, browser route, responsive layout, or UI consumption of a backend/API contract. The acceptance report must include browser smoke or explicit manual evidence, plus residual risk for any skipped viewport or unavailable runtime check.

For user-facing web UI acceptance, the report must name route/page, mobile and desktop viewport or a skip reason, user steps, expected visible result, negative check, and Playwright / agent-browser / project e2e / documented manual browser evidence. Usually this packet is not needed for backend-only work with no visible user surface, but if a route can prove acceptance, use it or record a skip reason.

### Scope and Diff Audit

See `skills/pipeline/references/shared.md` §Scope and Diff Audit.

Run this before the Review Menu. Unexpected files or behavior changes must be explained, reverted, or added to the plan with rationale before review begins.

### Skipped or Deleted Tests Policy

See `skills/pipeline/references/shared.md` §Skipped or Deleted Tests Policy.

Acceptance must explicitly account for any deleted, skipped, weakened, or excluded tests.

### Test Adequacy Review

See `skills/pipeline/references/test-adequacy-review.md`.

Run TAR for test-changing, behavior-changing, Codex-heavy, full_autonomous, or overnight work before accepting the implementation. the human operator is not expected to personally judge test adequacy; a green test suite is not enough if tests are weak.

### Review Quality Lenses

See `skills/pipeline/references/shared.md` §Review Quality Lenses and `skills/pipeline/references/review-quality-lenses.md`.

Before the Review Menu or any cross-agent review, tell the reviewer to cover at least correctness, readability, architecture, security, and performance, then add context-specific lenses such as UX, migrations, data, compatibility, observability, cost, legal, accessibility, reliability, privacy, rollout, support, or test adequacy.

Apply the profile-specific review overlay from `skills/pipeline/references/collaboration-profiles.md` before the Review Menu. **Precedence (F-036):** Review Menu user choice wins over profile overlay. The profile overlay only applies for layers the user did not explicitly select or skip in the Review Menu; an explicit user choice in the Review Menu is authoritative.

- `solo_primary` — main review plus baseline review.
- `claude_main_codex_checkpoints` — primary final review plus secondary cross-review when available.
- `dual_head_quality` — Claude and Codex both review; findings are ratified.
- `codex_heavy_claude_guardrails` — Codex self-review plus Claude final-review, with TAR between them.

### Review Menu

See `skills/pipeline/references/shared.md` §Review Menu Template.

Параметры для deep:
- `<CLASS>` — из Phase 1 brief
- `<RISK>` — risk level из spec
- `<SECURITY_AUTO>` — см. `skills/pipeline/references/shared.md` §Security Scan Auto-Trigger Paths
- `<SHOW_CROSS_CHECK>` = `false` (в deep нет /cross-check)

Обработать выбор пользователя ДО запуска любого ревью-слоя. Baseline (Secret + CVE + code-reviewer) запустится в любом случае.

### Security Scan (auto-trigger + menu option)

See `skills/pipeline/references/shared.md` §Security Scan Auto-Trigger Paths.

При сработавшем триггере — запустить `/codex-security-scan` автоматически, отметить `[✓]` в Review Menu.

Также доступен как ручной пункт через `+codex-security-scan` в меню.

### Smoke-test инструменты

See `skills/pipeline/references/shared.md` §Smoke-Test Tools Table.

Deep-mode acceptance must also answer:
- did the change preserve the listed invariants?
- are the main failure modes covered by tests, validation, or explicit deferral?
- is rollback/fallback still valid after the final code shape?
- do logs/metrics/debug signals exist for the risky path?

### Ship Readiness

See `skills/pipeline/references/shared.md` §Ship Readiness and `skills/pipeline/references/ship-readiness.md`.

Read this when the accepted change affects real users, production runtime, launch, rollout, pricing, data, or operations. Otherwise record `Ship Readiness: N/A` with a reason.

### Parallel Critics (optional review layer)

> **Активация:** только если пользователь явно выбрал пункт 1 в Review Menu. По умолчанию не запускается.

Full critics protocol — task class detection, presets, dispatch contract (REQUIRED sub-skill `superpowers:dispatching-parallel-agents`, strict JSON output contract), finalizer Hard Rules, severity-based re-check, escalation stop conditions, and state.json logging: read `skills/pipeline/references/parallel-critics.md` (F-023 dedup executed 2026-06-09).

### Code Review (baseline — REQUIRED)

**REQUIRED:** Invoke `superpowers:requesting-code-review` after implementation. Это baseline-слой ревью для всех рисков (low/medium/high). Дополнительные слои — через Review Menu выше.

Dispatches a code-reviewer subagent that independently checks code quality, architecture, testing, and requirements compliance. The review supplements — not replaces — the acceptance checks below.

### Iterative Review Loop

Если code review вернул замечания:

1. Исправить замечания по формату Accept or Argue (см. `superpowers:receiving-code-review`)
2. Переотправить на повторное ревью — проверить что правки действительно решили проблему
3. До 3 раундов: ревью → правки → повторное ревью
4. После 3 раундов без полного одобрения — показать пользователю сводку нерешённых замечаний и спросить:
   - **ещё раунд** — продолжить review loop (начать раунд 4)
   - **принять как есть** — зафиксировать нерешённые замечания в "residual risks" секции отчёта Phase 8 и перейти к acceptance

Применяется к любому источнику ревью: code-reviewer субагент, Codex, cross-check.

### Cross-Agent Review (menu option)

**Активация:** только если пользователь выбрал пункт 2 в Review Menu. На `high-risk` задачах предустанавливается `[x]`, на остальных — `[ ]`. Ревьюер определяется автоматически по текущей платформе (см. `orchestration.md §Reviewer Selection`, entry under `shared.md §Cross-Agent Review Template`).

See `skills/pipeline/references/shared.md` §Cross-Agent Review Template.

Параметры для этого вызова:
- `<ARTIFACT>` = `code`
- `<ENTRY_PHASE>` = Phase 7 (Acceptance), AFTER Parallel Critics + `requesting-code-review`
- `<EXIT_PHASE>` = Phase 8 (Report and Review)
- `<REVIEW_FOCUS>` = `bugs, security issues, race conditions, error handling gaps, performance problems`
- `<DOC_OR_DIFF>` = changed files + `git diff`

### Compact checkpoint

Перед переходом к Phase 8: если сессия длинная (50+ tool calls), предложить `/compact` чтобы сохранить контекст для финального отчёта. Не компактить посреди имплементации или между тестами и фиксами.

Record concrete evidence, not vague claims.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_7_acceptance.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_8_report"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_7_acceptance completed"`

## Phase 8: Report and Review

Write `docs/reports/YYYY-MM-DD-<topic>-implementation.md` with:
- discovery summary
- research summary
- implementation summary
- changed files
- tests and regressions
- acceptance evidence
- safety choice
- invariant check results
- rollback/fallback status
- observability notes
- residual risks

### Saved Auditor Report

See `skills/pipeline/references/shared.md` §Saved Auditor Report.

For deep mode, the implementation report doubles as the saved auditor report only if it includes plan-vs-diff, changed files, verification evidence, skipped safeguards, and residual risks. Use `skills/pipeline/references/report-status-evidence.md` for multi-effect reports or user-facing impact summaries. Otherwise, create a separate `docs/reports/YYYY-MM-DD-<topic>-audit.md`.

### Skill Behavior Evals and Scorecard

See `skills/pipeline/references/shared.md` §Skill Behavior Evals and Scorecard.

If this task changed skill, prompt, or agent behavior, acceptance must include scorecard results and clean-context scenario outcomes.

Skill-change acceptance gate: final acceptance must include clean-context scenario outcomes, a filled or referenced scorecard, and either measured metrics evidence or an explicit statement that precision, recall, and F1 were not measured with residual risk.

When eval metrics were measured, update `skills/pipeline/evals/metrics.md`; when they were not measured, state that as residual risk instead of inventing precision/recall/F1.

Use the report as the human review checkpoint. Do not end the workflow yet.

### Сводка изменений для пользователя

See `skills/pipeline/references/shared.md` §User Summary Blocks.

Apply the Chat Summary Gate before Phase 9 or any final answer: show the numbered pluses, risks, security, affected behavior, and unaffected behavior blocks in chat even when the technical report already exists.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_8_report.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_9_branch_completion"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_8_report completed"`

## Phase 9: Branch Completion

See `skills/pipeline/references/shared.md` §Branch Completion.

Required literal handoff for this mode:
- Before invoking `superpowers:finishing-a-development-branch`, show the User Summary Blocks in the current chat response.
- Use the exact labels from `skills/pipeline/references/report-status-evidence.md`. Do not replace them with `Impact`, `Evidence`, `Risks`, or `Branch Status`.
- A saved report or status file alone is not enough.
- Do not present `Implementation complete. What would you like to do?` until the summary blocks have already been shown.
- invoke `superpowers:finishing-a-development-branch`
- present: `Implementation complete. What would you like to do?`

Применимость для deep: основной блок + GitHub Issue Closure subsection (пункты 1-3 из shared.md).

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_9_branch_completion.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "final"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_9_branch_completion completed"`

## State Persistence

See `skills/pipeline/references/shared.md` §State Persistence Schema v1.

**Phase IDs (deep):** `phase_0_backup`, `phase_0_5_rigor`, `phase_1_discovery`, `phase_1_5_practices`, `phase_2_context`, `phase_3_research`, `phase_4_spec`, `phase_5_planning`, `phase_6_execute`, `phase_7_acceptance`, `phase_8_report`, `phase_9_branch_completion`.

**Finalization:** когда `phase_9_branch_completion.status = "completed"`, state считается финализированным; resume skips it.

## Built-In Rules

- Do not start coding from a raw idea
- Research is conditional, not ceremonial
- Artifacts must survive handoff between phases
- TDD is mandatory once implementation begins
- Real-environment acceptance is mandatory for user-facing or integration-facing changes
- Deep mode must think about failure, rollback, and observability before coding
- Mirror the language of the user's request in all artifacts
- Update existing design docs instead of creating duplicates
- If the task becomes simple after discovery, switch to `pipeline-lite` for execution

## Appendix: /codex:adversarial-review (optional plugin)

Not part of the main flow. Full install/usage/warnings and its relation to Cross-Agent Review: read `skills/pipeline/references/orchestration.md` §Optional Plugin: /codex:adversarial-review (moved 2026-06-09).
