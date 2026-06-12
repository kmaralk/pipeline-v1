---
name: pipeline-hard
description: "Use when explicitly requested, when the router selects the full workflow, or when lite/deep escalates to high-risk autonomous prep, oracle review, Repo Prompt handoff, Codex-heavy execution, or deferred decisions. Supports heavy/тяжелый/autonom+heavy/autonomous heavy/ok C4 A3; Codex-heavy green-tests-only; TAR required."
---

# Pipeline Hard

This is the full advanced end-to-end workflow for large, high-value tasks. It is intentionally opinionated and uses the preferred role stack directly:
- current orchestrator for requirements and project shaping [LOCAL]
- Superpowers process skills for disciplined discovery and planning [LOCAL]
- Exa MCP when web-aware local research is useful during requirements work [LOCAL, OPTIONAL]
- local automated oracle routes through Claude Code, Codex, browser tools, docs, GitHub, and MCP/plugin evidence [LOCAL, DEFAULT]
- optional manual premium oracle routes through ChatGPT Pro, Claude web, Gemini, or Repo Prompt handoff [MANUAL, OPTIONAL]
- current orchestrator for consolidation and implementation planning [LOCAL]
- selected executor for autonomous implementation and runtime validation [MANUAL HANDOFF or LOCAL]

Current deployment preference remains Codex-heavy + Claude guardrails when `C4 A3` is selected. The role-neutral mapping is: heavy-executor = Codex, guardrail-reviewer = Claude Code. For flipped-role deployments, swap providers in the `orchestration.roles` state field — the canonical text stays role-neutral. See `skills/pipeline/references/collaboration-profiles.md` §Provider Neutrality.

Discovered tasks and run-control inheritance: read `skills/pipeline/references/run-control-inheritance.md` before accepting or handing off work found during review, testing, implementation, resume, oracle review, or Codex execution. Do not downgrade accepted child work from the parent `run_control`. Do not silently implement discovered new features.

Premortem plan review: read `skills/pipeline/references/premortem-plan-review.md` before accepting a consolidated spec, implementation plan, Codex-heavy batch, or autonomous handoff. For hard, run it in Phase 5 Consolidation before Phase 6 Implementation Planning and before Codex-heavy or autonomous implementation. It does not reset the selected `run_control`.

## Immediate First Response Gate

If either run control is missing, ask both menus in the first response before Phase -1, Phase 0, branch work, oracle work, requirements artifacts, or file reads:

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

## Triggered By Router Or Escalation

Use hard only by one of three single-authority paths (this section is the single source of truth; `## Non-Negotiable Rules` references it instead of duplicating the rule):

1. explicit request from the user (e.g. `pipeline-hard`, `$pipeline-hard`, `/pipeline-hard`);
2. the pipeline router selects it from strong hard-mode triggers — router-selected hard-mode trigger requires a short rationale per `skills/pipeline/SKILL.md` "automatic hard routing requires a short rationale" clause;
3. `pipeline-lite` or `pipeline-deep` escalates to it (lite/deep → hard escalation) because the task now needs the full advanced workflow.

Do not use hard merely because a task is large or important. If the task is broad but does not need the full advanced workflow, use `pipeline-deep` instead.

## When to Use

Use when:
- the task is large, expensive, or strategically important
- the request starts as a big idea and needs full shaping before code
- strong external research would materially improve the outcome
- UX, PRD quality, contracts, and coder handoff all matter
- you want maximum autonomous work before coming back to review
- you want the task prepared for near end-to-end automation later

Do not use when:
- the task is a small or medium technical change
- local context is enough
- the cost and latency of the full advanced pipeline are not justified

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

## Core Principle

The pipeline should do as much safe work as possible without waiting for the user.

If a risky, destructive, privileged, or irreversible step appears:
- do NOT stop the whole pipeline
- do NOT perform the dangerous step
- complete everything else that is safe and verifiable
- record the blocked action in `deferred decisions`
- leave an exact next step for the human

## Phase -0.5: State Detect & Resume

**MANDATORY. Before Phase -1 / Phase 0.**

Parse `<topic>` from the user request, then check for existing state:

```bash
ls docs/plans/*-<topic>-state.json 2>/dev/null
```

**Decision tree:**

1. **No state files** → new run. Create state.json at end of Phase 0, continue.
2. **One file, `current_phase == "final"` AND `phases.phase_11_branch_completion.status == "completed"`** (hard finalization rule per `shared.md §State Persistence Schema v1`; the schema has no top-level `status` field — finalization is observed via `current_phase` plus the final phase's status) → ask user: "Topic '<topic>' already completed on <date>. Run a new pipeline with today's date? (да/нет)".
3. **One file, `current_phase != "final"` OR `phases.phase_11_branch_completion.status != "completed"`** → parse state, show the Resume UX below, ask user action.
4. **Two or more state files** → list all with date + last_phase, ask user which to resume, or "new".

### Resume UX (Russian, mirrors Language Rule)

```
Нашёл незавершённый pipeline-hard для темы "<topic>":

  <checkbox> Phase -1 — rigor (<status>)
  <checkbox> Phase 0 — backup (<status>)
  <checkbox> Phase 1 — requirements (<status>)
  <checkbox> Phase 1.5 — context-driven practices (<status>)
  <checkbox> Phase 2 — boardroom (<status>)
  ...
  <checkbox> Phase 7 — implementation (<status>)
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

## Phase -1: Rigor Level

**REQUIRED:** Set maximum rigor level before any work begins.

Invoke `/dushno 10` — full devil's advocate mode. Challenge every assumption, question every decision, flag every risk. Nothing passes unchecked.

## Phase 0: Branch And Worktree Policy

**MANDATORY before repository file edits.**

1. Run `git status --short --branch`.
2. Read `skills/pipeline/references/branch-worktree-policy.md`.
3. Apply the `pipeline-hard` mode default from that reference.
4. For autonomous execution or parallel agents, also read `skills/pipeline/references/worktree-agent-isolation.md`.
5. Record branch/worktree choice and any deferred remote backup as residual risk in state/report.

### Worktree Isolation (optional)

If the working directory has uncommitted changes that should not be disturbed, or if parallel work needs isolation, invoke `superpowers:using-git-worktrees` instead of `git checkout -b`. This creates an isolated copy of the repo in a separate directory. The standard feature branch approach (above) remains the default.

### Worktree Agent Isolation

For autonomous hard-mode execution or parallel workers, use `skills/pipeline/references/worktree-agent-isolation.md`.

- Apply its GitHub Issue Policy: issue required for autonomous or parallel hard work unless explicitly skipped with a recorded reason.
- The orchestrator writes a File Ownership Plan before dispatch.
- Every worker gets the Worker Handoff Template with branch/worktree, allowed files, forbidden files, acceptance checks, and stop conditions.
- Workers commit only in their own branch/worktree; the orchestrator reviews, tests, and merges one worker result at a time.

### New Project Check

Если проект новый (нет `CLAUDE.md` с блоком `Agent Operations Config`, нет GitHub Project, нет labels) — **спросить пользователя, запускать ли `project-init` skill** перед продолжением:

> «Проект выглядит новым — в `CLAUDE.md` нет блока `Agent Operations Config`. Запустить `project-init`, чтобы создать GitHub Project, labels, canonical-файлы и config-блок? (да / нет / позже)»

Поведение:
- **да** → invoke `project-init` skill, дождаться завершения, затем продолжить с остальными шагами Phase 0
- **нет** или **позже** → пропустить, продолжить. Не спрашивать повторно в этой сессии
- проект уже настроен (есть `Agent Operations Config`) → пропустить проверку молча, без вопроса

Если GitHub-репозитория у проекта ещё нет — перед `project-init` создать его: `gh repo create <owner>/<name> --private --source=. --push`. `<owner>` взять из `routing:` секции `CLAUDE.md` (пути вида `<owner>/<repo>`). Если в `CLAUDE.md` нет `routing:` или там несколько разных owner — уточнить у пользователя. Всегда подтверждать имя репо и owner перед созданием.

Docker/runtime decision: when `project-init` runs, make sure its Docker / container preference answer is captured before continuing. Do not silently add Docker files; the project-init answer decides whether to create no container files, a Dockerfile, docker-compose, or a devcontainer later in the implementation plan.

### GitHub Issue Context (optional)

Если задача связана с GitHub Issue — **invoke `gh-issues` skill** для загрузки контекста:
1. Загрузить AI Session Context из комментариев issue (предыдущий прогресс):
   ```bash
   gh issue view <NUMBER> --json comments --jq '.comments[] | select(.body | contains("AI-CONTEXT")) | .body'
   ```
2. Привязать ветку к issue: `gh issue develop <NUMBER> --checkout`
3. Пометить issue как in-progress: `gh issue edit <NUMBER> --add-label in-progress`

### State init

After Phase 0 branch/worktree decision, initialize state.json:
- Create `docs/plans/<DATE>-<topic>-state.json` with schema v1 (см. `shared.md §State Persistence Schema v1`).
- Fields at init: `started_at`, `last_updated_at`, `branch_name`, `design_doc`, `current_phase = "phase_1_requirements"` (the first phase that is not yet completed), `phases.phase_-1_rigor.status = "completed"` (rigor was already chosen in Phase -1), `phases.phase_0_backup.status = "completed"`, `finished_at = now`.
- Initialize `open_questions: []` for unresolved questions that must survive context resets.
- Persist `run_control` (collaboration_profile, autonomy, cross_check_initial, premortem_plan_review) into state.json at creation time under `orchestration.*`, using the values held in chat state since they were collected. State.json must never exist without a non-empty `orchestration.collaboration_profile` and `orchestration.autonomy`.
- Atomic write (`.tmp` → `fsync` → `mv`), then `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc is not yet created) + `git commit -m "pipeline: state initialized"`.

### Baseline Gates

See `skills/pipeline/references/shared.md` §Baseline Gates.

Применимость для hard: mandatory. Все 3 стека (Python/Node/Go) обязательны при наличии соответствующих lockfile. Результат фиксируется в отчёте Phase 10 под `Baseline Gates Result`. Инструмент не установлен → warning + запись в residual risks. **Пропуск baseline gate — только через deferred-decisions с явным обоснованием.**

## Phase 1: Requirements

**REQUIRED:** Invoke `superpowers:brainstorming` before implementation thinking.

Environment:
- current orchestrator (`claude_code` or `codex`)
- selected reviewer/helper from `orchestration.roles` when needed
- Superpowers, especially `/brainstorm`

Treat this like a conversation with a strong product partner, not a coding session.

Goals:
- clarify what the user wants
- surface hidden assumptions
- identify success criteria and non-goals
- decide whether the idea should be decomposed

If the task is broad or fuzzy, use brainstorming discipline:
- ask clarifying questions before implementation thinking
- compare approaches
- converge on a concrete direction

If analysis is needed, prefer a boardroom-style investigation before finalizing the spec.

Required output:
- `requirements brief`
- `problem statement`
- `desired outcome`
- `non-goals`
- `constraints`
- `success criteria`
- `open questions`
- `initial prompt pack`

If the task is a feature, also prepare:
- branch name suggestion
- issue/title suggestion

Persist unresolved blockers in `state.json.open_questions`. Remove or mark each item resolved when answered, deferred, or made irrelevant by scope changes.

Artifacts from this phase go to `docs/plans/` (requirements brief, prompt pack) or `docs/research/` (context dossier, oracle bundles).

If this phase does not produce concrete artifacts in the repo, the phase is incomplete.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_1_requirements.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_1_5_practices"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_1_requirements completed"`

## Run Control Choices

Before Phase -1, Phase 0, or any tool work, resolve the two independent run controls unless the user already specified both:

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

If `cross_check_initial = true`, use it as a one-shot early oracle around Phase 3/4; do not run it after every milestone.
If `premortem_plan_review = forced`, run Premortem Plan Review at the mode placement even if automatic risk triggers would skip it. If `premortem_plan_review = auto`, run it only when `skills/pipeline/references/premortem-plan-review.md` says the task risk/shape requires it.

## Phase 1.5: Context-Driven Practices

**Strictness for hard: MANDATORY.** Все триггернувшиеся практики включаются обязательно. Пропуск допустим только через deferred-decisions с письменным обоснованием («почему в этой конкретной задаче эта practice не применяется»). Молчаливо отключить нельзя.

**F-047 anti-inflation cap and named-risk requirement:** activated practices are mandatory **only when they reduce a named risk** in this specific task. For each activated practice, the agent names the concrete risk it mitigates (e.g., "threat-model: SSRF risk in webhook fetcher"); if no concrete named risk applies, the practice is recorded as "auto-activated, no named risk — skipped" in deferred-decisions, not enforced. Cap simultaneously-active practices at 6 unless the user explicitly approves expansion; above 6 the agent asks the user which to defer. The goal is real risk reduction, not document-generation theatre.

Цель — превратить hard-пайплайн в проактивно-производственный: он сам подтягивает threat-model, idempotency plan, rollout plan и прочие артефакты, связанные с риском задачи.

### Шаги

1. Прочитать `skills/pipeline/references/practices-index.md` (лёгкий индекс, ~50 строк).
2. Для каждой строки индекса — проверить триггеры:
   - **Step A — exact match (0 tokens):** keyword из `keywords` есть в requirements brief Phase 1 ИЛИ glob из `paths` совпадает с affected surfaces / boardroom findings / selected files (только если Phase 2 has already run; иначе ограничиться requirements brief Phase 1 и affected surfaces, известными на момент запуска Phase 1.5). Phase 2 may not have run yet — это OK, в этом случае trigger matching работает по доступным входам.
   - **Step B — semantic fallback (small AI call):** короткий AI-верификатор по `semantic`. **F-048 resolution:** для hard-режима semantic-шаг **запускается ВСЕГДА** (правило «запускается ВСЕГДА» takes precedence / превалирует over старого «если Step A не сработал»). Practice активируется, если Step A ИЛИ Step B сказал «да». Старая формулировка "если Step A не сработал" сохраняется только как обоснование запуска при отсутствии exact-hit; в hard режиме Step B всё равно запускается.
   - Practice активируется, если хотя бы один шаг сказал «да».
3. Для КАЖДОЙ активированной practice — открыть `skills/pipeline/references/practices-full.md` на якоре `#<id>` и прочитать ТОЛЬКО её блок. Не загружать файл целиком.
4. Проверить `prerequisites` (из прочитанного блока). Не выполнены → practice активна, добавить в deferred-decisions или отдельный milestone «подготовить prerequisite».
5. Показать пользователю набор (все отмечены по умолчанию):

```
Context-Driven Practices (hard: mandatory):

  [✓] threat-model          — trigger: keyword "auth" + semantic match
  [✓] idempotency           — trigger: keyword "webhook"
  [✓] expand-contract-mig   — trigger: path "migrations/"
  [✓] slo-perf-budget       — semantic match
  [✓] feature-flags         — semantic match
  [✓] eval-driven-ai        — path "skills/**/SKILL.md"

Действия:
  Enter       принять всё
  skip N      пропустить с обязательным обоснованием → deferred decisions
  detail N    показать полный текст practice
```

6. Для каждой активной practice — её `Add to Phase 5 (consolidation/spec)` / `Add to Phase 7 (execute)` / `Add to Phase 8 (runtime acceptance)` секции инжектятся в соответствующие артефакты.

### State update

```json
"phase_1_5_practices": {
  "status": "completed",
  "finished_at": "<ISO>",
  "activated": ["<id1>", "<id2>"],
  "skipped_with_reason": [{"id": "<id3>", "reason": "<text>"}],
  "semantic_checks_run": <N>
}
```

Also set top-level `current_phase = "phase_2_boardroom"`.

Atomic write, `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_1_5_practices completed"`.

### Output

Активные practices становятся обязательными секциями spec Phase 5. Пропущенные practices попадают в Phase 9 (Deferred Decisions) как "active practice skipped: `<id>` — reason: `<text>`" и должны быть явно подтверждены пользователем перед Phase 10.

## Phase 2: Boardroom Context

**F-082 — always runs in hard mode.** Hard mode is opted into for tasks that warrant the full advanced workflow, so boardroom evidence is part of that contract; there is no "when analysis is needed" guard for hard. Launch parallel context gathering on the local machine. See `skills/pipeline/references/observable-gates.md §F-082` for the rationale and the lite/deep analysis-conditional carve-out.

### Context Hygiene Gate

See `skills/pipeline/references/shared.md` §Context Hygiene Gate.

Before launching boardroom lanes, name the allowed docs, code paths, skills, MCP servers, and tools. Keep each lane narrow and avoid loading unrelated global context.

Preferred shape:
- up to 10 focused subagents
- each investigates a distinct angle
- results are triaged and synthesized centrally

Good investigation lanes:
- relevant code paths
- existing tests and regression risks
- architecture and neighboring modules
- current contracts and schemas
- docs, runbooks, and deployment notes
- failure modes and dangerous actions
- likely acceptance surfaces

Boardroom rule:
- do not ask 10 agents to solve the same fuzzy task
- give each one a narrow question
- synthesize, compare, and triage findings

**REQUIRED:** Invoke `superpowers:dispatching-parallel-agents` to structure agent prompts with focused scope, self-contained context, and specific output expectations. The boardroom lanes above define WHAT to investigate; the skill defines HOW to dispatch agents correctly.

Required output:
- `context dossier`
- `triage summary`
- `selected files list`
- `risks register`
- `blind spots / open unknowns`

### Lightweight Memory Bank

See `skills/pipeline/references/shared.md` §Lightweight Memory Bank.

For hard mode, check `docs/agent-memory/index.md` or the project's existing memory index during boardroom/context gathering if present. Add a memory note when the run discovers reusable project knowledge, repeated agent failure, or a known-good command.

### Tool and Model Routing Matrix

See `skills/pipeline/references/shared.md` §Tool and Model Routing Matrix.

Use the matrix to justify planning/research, implementation, audit/review, browser acceptance, AI trace debugging, and knowledge lookup tools before choosing heavier tooling.

### CLI Recipes and Tool Failure Log

See `skills/pipeline/references/shared.md` §CLI Recipes and Tool Failure Log.

When a command, MCP, Codex handoff, or browser runner fails because of syntax, timeout, env, or context mismatch, preserve the known-good command and the failure mode in the report or project memory.

### Prototype And Trace Practices

See `skills/pipeline/references/shared.md` §Prototype And Trace Practices and `skills/pipeline/references/prototype-trace.md`.

For hard mode, require a prototype spike when an uncertain tool contract, API contract, migration shape, or risky implementation path would otherwise make the plan speculative. For AI-app debugging or agent quality degradation, name the trace evidence reviewed before changing prompts, orchestration, or agent instructions.

### Planner Generator Evaluator Roles

See `skills/pipeline/references/shared.md` §Planner Generator Evaluator Roles and `skills/pipeline/references/planner-evaluator.md`.

For hard mode, prefer explicit planner/generator/evaluator separation on large or high-risk work. Enforce Cross-agent symmetry when both platforms are available, and make the evaluator an adversarial evaluator that leads with blockers and reproduction evidence.
Record the review result, accepted fixes, rejected nitpicks, and residual risk.

### Skill vs Runbook vs CLI Decision Rule

See `skills/pipeline/references/shared.md` §Skill vs Runbook vs CLI Decision Rule.

Before creating or changing a skill, decide whether the lesson belongs in a runbook, CLI, CLI + skill pair, skill, or global instructions.

### File-First Knowledge Before RAG

See `skills/pipeline/references/shared.md` §File-First Knowledge Before RAG.

Use local files and `rg` first for knowledge lookup. Do not propose RAG unless file-first retrieval has a recorded failure criterion.

### Source Grounding

See `skills/pipeline/references/shared.md` §Source Grounding and `skills/pipeline/references/source-grounding.md`.

Use this in research, consolidation, planning, implementation handoff, and review when the work depends on an external library, API, SDK, framework, CLI, protocol, vendor service, or versioned behavior. Check local dependency versions, official docs, and Context7 when available before committing to API-specific plans, code, or review claims.

### AI Minimalism Guardrails

See `skills/pipeline/references/ai-minimalism.md`.

For hard mode, apply the Minimal Diff Packet and Reuse-Before-Build during consolidation and Codex/autonomous handoff when AI-generated code or custom infrastructure is likely. Require the Post-Green Simplify Pass and Review Burden Budget before review for broad or AI-generated diffs. Use Context Rule Audit for AGENTS, CLAUDE, SKILL, prompt, or context-rule changes.

### Idea To Ship Stage Gates

See `skills/pipeline/references/shared.md` §Idea To Ship Stage Gates and `skills/pipeline/references/idea-to-ship-gates.md`.

For hard mode, use Raw Idea Intake in requirements when the input is rough, What-before-How PRD Gate during consolidation, Minimal Architecture Pack before implementation planning or Codex handoff, Bug Fix Record for non-trivial fixes, and Chat Summary Gate before branch completion or final handoff.

### Skill Packaging and Portability

See `skills/pipeline/references/shared.md` §Skill Packaging and Portability and `skills/pipeline/references/packaging.md`.

Use this when the task changes pipeline skill packaging, `agents/openai.yaml`, active-copy sync, validators, third-party skill installation/review, or cross-agent compatibility assumptions.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_2_boardroom.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_3_oracle_prep"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_2_boardroom completed"`

## Phase 3: Oracle Routing And Prep

### Oracle Routing Policy

Read `skills/pipeline/references/oracle-routing.md`.

Default to local automated oracle unless the user asks for manual premium oracle.

Manual web oracle is optional, not mandatory.

Record the selected oracle route:
If browser tools are used, require independent judgment over browser evidence before calling the oracle complete.
- `local_automated`;
- `manual_premium`;
- `hybrid`;
- `skipped`.

Build an oracle input bundle for the selected route:
- problem;
- desired result;
- requested output format;
- current spec or draft spec;
- selected files or evidence;
- context dossier;
- known constraints;
- explicit questions for the oracle.

Recommended oracle asks:
- UX direction;
- PRD refinement;
- contracts;
- edge cases;
- research synthesis;
- implementation prompt for the coding agent.

Route options:
- **Local automated:** use Claude Code, Codex, `agent-browser`, Playwright, Exa, GitHub, docs, MCP/plugins, or other available tools to gather evidence and get independent critique without waiting for manual handoff.
- **Manual premium:** prepare a concise bundle for ChatGPT Pro, Claude web, Gemini, or Repo Prompt when the user explicitly wants this route.
- **Hybrid:** run local automated research/review first, then add one or more manual premium opinions for high-stakes decisions.
- **Skipped:** allowed only when an oracle would not materially improve confidence; record why.

Required output:
- `oracle route record`;
- `oracle input bundle`;
- `selected context pack`;
- `oracle question set`.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_3_oracle_prep.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_4_oracle"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_3_oracle_prep completed"`

## Phase 4: Oracle Run

Run the selected oracle route from Phase 3.

For `local_automated`:
- gather evidence through available tools;
- ask an independent model/agent to critique the plan or synthesize options;
- keep browser automation and Playwright evidence separate from the model judgment.

For `manual_premium`:
- give the user the prepared bundle and wait only if the user selected this route;
- accept ChatGPT Pro, Claude web, Gemini, or equivalent oracle memo as the returned artifact.

For `hybrid`:
- consolidate local automated findings with manual premium output;
- preserve disagreements instead of averaging them away.

For `skipped` (F-035 skipped route branch):
- skip oracle memo generation; do not invent an oracle artifact;
- require explicit user confirmation of the skip (the route was already chosen in Phase 3, but Phase 4 re-confirms);
- record the skip decision and the reason ("oracle would not materially improve confidence" or equivalent) in the run report;
- carry forward unresolved questions as `state.json.open_questions` or residual risk so Phase 5 consolidation sees them.

Required output:
- `oracle memo`;
- `oracle route record`;
- refined `UX / PRD / contracts / agent prompt` artifacts;
- disagreements or unresolved questions;
- residual risk for skipped manual premium oracle when it materially affects confidence.

Treat oracle output like an executive advisor artifact, not disposable scratch work.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_4_oracle.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_5_consolidation"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add docs/plans/<DATE>-<topic>-state.json` (state.json only — design-doc not yet created), `git commit -m "pipeline: phase_4_oracle completed"`

## Phase 5: Consolidation

Return to the current orchestrator in the same project folder and consolidate oracle output with local project reality.

### Spec Strategy Choice

Before writing the consolidated spec, offer the user the plain-language choice from `orchestration.md §Before spec` (entry under `shared.md §Codex-Orchestrated Planning and Execution`).
Detailed reference: `skills/pipeline/references/orchestration.md` §Codex-Orchestrated Planning and Execution.

Record the selected strategy in state (F-037 — disambiguated names; spec-phase Option B is `planning_option_b_cross_review`, NOT the executor delegation; see Phase 6 / Phase 8 for `executor_option_b_delegated_platform`):
- `current_model` for option A
- `planning_option_b_cross_review` for option B (cross-review of the spec by the other model)
- `codex_details` for option C

For hard mode, prefer option C when Codex is available and the project is trusted. If option C is selected:
1. Current model writes a thin consolidated spec first: goal, non-goals, invariants, contracts, risks, acceptance.
2. Run the Codex preflight and Codex Invocation Ladder route selection from `shared.md §Codex-Orchestrated Planning and Execution`.
3. Ask Codex to add implementation details only: likely files, tests, edge cases, technical risks, open questions.
4. Current model reviews Codex output, ratifies decisions, and writes final spec.

Do not let Codex make high-stakes product, architecture, security, rollout, or scope decisions. Codex proposes; current model decides.

Goals:
- align web research with the actual codebase
- reject advice that conflicts with local constraints
- produce an implementation-ready spec bundle

Write or update `docs/plans/YYYY-MM-DD-<topic>-design.md`.

If a design doc for this topic already exists, update it — preserve completed milestones, decisions, and assumptions. Do not overwrite progress.

Required sections:
- context and problem
- chosen direction and rejected alternatives
- risk register and failure-mode review
- invariants
- affected components
- contracts and schema changes
- UX notes if relevant
- rollback or fallback plan
- rollout notes
- observability and monitoring plan
- input validation checklist (baseline — per external input)
- active practices (from Phase 1.5 — mandatory, all must appear or be in deferred decisions)

### Input Validation Checklist

See `skills/pipeline/references/shared.md` §Input Validation Checklist.

### Assumptions

See `skills/pipeline/references/shared.md` §Assumptions Section.

### Grounding Required

See `skills/pipeline/references/shared.md` §Grounding Required.

### Milestones

See `skills/pipeline/references/shared.md` §Milestones Template.

Hard-режим использует полную форму с секцией `### Tasks` под каждым milestone.

### Verifiable Acceptance Criteria

See `skills/pipeline/references/shared.md` §Verifiable Acceptance Criteria.

### Ambiguity Scanner

See `skills/pipeline/references/shared.md` §Ambiguity Scanner.

Run this before leaving consolidation. Resolve real ambiguity as a decision, `state.json.open_questions`, deferred decision, or residual risk. Hard mode must not pass unresolved choice language into implementation planning.

### Spec Regeneration Rule

See `skills/pipeline/references/shared.md` §Spec Regeneration Rule.

If the consolidated spec or downstream plan depends on hidden chat context, misses a contract, or has unresolved ambiguity, fix the source artifact and regenerate the downstream artifact before execution.

### Premortem Plan Review

Read `skills/pipeline/references/premortem-plan-review.md`.

For hard, run it in Phase 5 Consolidation before Phase 6 Implementation Planning and before Codex-heavy or autonomous implementation. Use the failure-frame review to find concrete plan holes, accept only mitigations that belong in current scope, record deferred holes, and keep the selected `run_control` sticky for accepted work.

### Skill Behavior Evals and Scorecard

See `skills/pipeline/references/shared.md` §Skill Behavior Evals and Scorecard.

For skill, prompt, or agent-workflow changes, the consolidated spec must name the clean-context scenarios, scorecard evidence, and `skills/pipeline/evals/metrics.md` update plan that will prove the change improved behavior.

### Downstream Contract Handoff

Read `skills/pipeline/references/contract-handoff.md`.

For hard mode, create the handoff before delegated implementation or Codex execution when backend, frontend, API, worker, or data-contract ownership is split. The consolidated spec and implementation handoff must name producer responsibilities, consumer responsibilities, contract delta, and acceptance handshake.

### Resume State

See `skills/pipeline/references/shared.md` §Resume State Block.

### Phasing Rule

If the task has many milestones (7+), split into phases. Detail the current phase fully, keep later phases coarse. Expand them when reached.

### Definition of Done and Deferred Decisions

End the spec with:
- definition of done
- dangerous or privileged actions that must not be automated

Required output:
- `approved spec bundle`
- `oracle integration notes`
- `deferred decisions` seed list

Unlike smaller pipelines, this mode does not stop for normal approval checkpoints. Keep going unless a true blocker exists.

**F-068 carve-out — pauses that remain mandatory even under full_autonomous:** Do not require normal spec approval. Still pause for Run Control, explicit strategy menus, Review Menu, destructive actions, and true blockers. Autonomy means the agent does not wait for "looks good?" on every artifact; it does NOT mean skipping user-input gates that the menus require by design.

### Context Hygiene Gate

See `skills/pipeline/references/shared.md` §Context Hygiene Gate.

Before implementation planning, reduce the consolidated oracle/context bundle to the files, contracts, tests, decisions, and unresolved risks needed for execution. Do not carry raw research dumps forward unless a specific acceptance or implementation decision depends on them.

### Clean-Context Plan Review

See `skills/pipeline/references/shared.md` §Clean-Context Plan Review.

For hard mode, run a fresh-context review after consolidation and before implementation planning. Fix blocking findings around scope, contracts, data, UI/API behavior, tests, or acceptance. Record rejected nitpicks with rationale if they are mentioned in the report.

### Cross-Agent Plan Review (optional)

После консолидации spec и перед переходом к планированию — предложить ревью другой моделью.

See `skills/pipeline/references/shared.md` §Cross-Agent Review Template.
Detailed reference: `skills/pipeline/references/orchestration.md` §Cross-Agent Review Template.

Параметры для этого вызова:
- `<ARTIFACT>` = `plan`
- `<ENTRY_PHASE>` = Phase 5 (Consolidation)
- `<EXIT_PHASE>` = Phase 6 (Implementation Planning)
- `<REVIEW_FOCUS>` = `architectural issues, security concerns, race conditions, missing edge cases, contract violations`
- `<DOC_OR_DIFF>` = путь к `docs/plans/<design-doc>.md`

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_5_consolidation.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_6_planning"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_5_consolidation completed"`

## Phase 6: Implementation Planning

### Context Hygiene Gate

See `skills/pipeline/references/shared.md` §Context Hygiene Gate.

Before writing or delegating the implementation plan, reduce the oracle/context bundle to the files, contracts, tests, decisions, and constraints needed for execution.

### Ambiguity Scanner

See `skills/pipeline/references/shared.md` §Ambiguity Scanner.

Run this on the implementation plan before handoff. Do not delegate work if a milestone still contains unresolved "or/maybe/TBD" style choices.

### Planning Strategy Choice

Before writing the implementation plan, offer the user the plain-language choice from `orchestration.md §Before planning` (entry under `shared.md §Codex-Orchestrated Planning and Execution`).

Record the selected strategy in state (F-037 — planning-phase Option B is `planning_option_b_cross_review`):
- `current_model` for option A
- `planning_option_b_cross_review` for option B
- `codex_tdd_plan` for option C

For hard mode, prefer option C when Codex preflight passes. If option C is selected:
1. Give Codex the approved spec, oracle integration notes, and context pack.
2. Ask Codex for a detailed TDD implementation plan: tasks, tests, file paths, verify commands, stop conditions.
3. Current model reviews the plan for scope, safety, dependencies, missing tests, and forbidden actions before execution.

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

Still in the current orchestrator, create a detailed implementation plan.

Preferred discipline:
- use the writing-plans shape
- TDD-first
- exact files, tests, commands, and acceptance checks

Never write production code before a failing test.

Required output:
- `implementation plan`
- `execution handoff bundle`

The handoff bundle must include:
- approved spec
- contracts to verify
- exact or likely files to touch
- tests to write first
- verification commands
- reality-check instructions
- invariants to preserve
- rollout and rollback instructions
- observability checks
- forbidden or dangerous actions
- definition of done

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_6_planning.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_7_implementation"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_6_planning completed"`

## Phase 7: Autonomous Implementation

**REQUIRED:** Invoke `superpowers:test-driven-development` before writing implementation code.
**On test failures or unexpected behavior:** Invoke `superpowers:systematic-debugging` before proposing fixes.

### Context Hygiene Gate

See `skills/pipeline/references/shared.md` §Context Hygiene Gate.

Before implementation or delegated execution, state the allowed files, commands, tools, skills, MCP servers, and forbidden areas for the first batch.

### Autonomous Backup Gate

See `skills/pipeline/references/autonomy-safeguards.md` §Autonomous Backup Gate.

Apply this before Phase 7 autonomous implementation, Codex batches, or parallel workers.

### Pre-Autonomy Context Freeze And Compact Gate

See `skills/pipeline/references/autonomy-safeguards.md` §Pre-Autonomy Context Freeze And Compact Gate.

Apply this before full_autonomous, overnight, Codex-batched, or subagent-driven execution. Compact only after the durable task brief, open questions, ownership, verification, stop conditions, backup ref, and current state are written.

### Execution Profile And Autonomy

Use the `Model Collaboration Profile` and `Autonomy Level` already recorded in Run Control Choices.

Do not ask the old execution-phase autonomy menu again.

Apply `skills/pipeline/references/collaboration-profiles.md` to derive:

- spec strategy;
- planning strategy;
- executor;
- Phase 7.5 review overlay.

Apply `skills/pipeline/references/autonomy-levels.md` to derive:

- ask/default/stop behavior;
- lightweight run-log for `full_autonomous`;
- night protocol for `overnight`;
- Deferred-But-Continue rules.

If no collaboration profile was recorded because this is a resumed legacy state, re-ask the user via the Run Control Choices menu before proceeding. Do not silently default to `codex_heavy_claude_guardrails`; the silent legacy default is forbidden because resumed legacy runs do not consistently match the heavy-executor profile.

Before starting, state the execution proposal:

```md
## Ready to execute
- Start: <first unfinished milestone>
- Cycle: implement → validate → fix → mark done → next
- Validation: milestone checks + regression map
- Autonomy: <interactive | guided_autonomous | full_autonomous | overnight>
- Stop conditions: blocker, user input needed, deferred danger
```

Expected behavior:
- follow the handoff bundle exactly
- write tests first
- run targeted regressions
- run full verification
- repair failures autonomously
- mark each milestone `[x]` and update Resume State
- keep refining until acceptance is satisfied

If Codex is selected as executor, run Codex Invocation Ladder route selection first, then run in 3-5 task batches with the prompt contract, stop conditions, and verification loop from `shared.md §Codex-Orchestrated Planning and Execution`.

Preferred strengths to exploit:
- browser-based e2e validation for web products
- messaging/runtime validation for bot products
- repeated fix-verify loops without waiting for the human

For browser-based e2e validation for web products, read `skills/pipeline/references/browser-acceptance.md` and record the real journey evidence, mobile/desktop coverage, screenshot or trace path when available, and residual risk for skipped checks.

### Milestone state update

After marking `[x]` in design-doc:
- Read state.json
- Set `phases.phase_7_implementation.milestones.M<N>.status = "completed"`, `finished_at = <ISO now>`
- On retry: increment `attempts`, store `last_error` (short string) on failure
- Atomic write (write `.tmp` → fsync → rename)
- `git commit -m "pipeline: M<N> completed"`

### Subagent Execution (conditional default)

See `skills/pipeline/references/autonomy-safeguards.md` §Independent Parallel Execution Default.

**Run-control gate (F-033):** default-to-subagents is OFF unless `collaboration_profile` index ≥ 3 (C ≥ 3, i.e. C3 dual-head quality or C4 heavy executor + guardrail reviewer) AND `autonomy` index ≥ 2 (A ≥ 2, i.e. guided_autonomous, full_autonomous, or overnight). C1 (solo primary) and A1 (interactive) keep serial TDD with explicit ask-before-major-step behavior; do not silently expand to parallel subagents.

**Default (given run-control gate passes):** если Codex-вариант не выбран, platform and governing instructions allow subagents, и выполняются ОБА условия ниже — по умолчанию запускаем subagent-driven-development (параллельная реализация). Иначе — serial TDD (шаги выше).

**Условие активации (оба обязательны):**

1. **`plan.milestones >= 4`** — масштаб оправдывает параллелизм (overhead запуска субагентов меньше выигрыша).
2. **Milestones largely independent** — каждое из трёх:
   - **No shared in-memory/on-disk state:** нет состояния, которое один milestone мутирует, а другой читает в том же запуске.
   - **No ordering dependencies:** milestone M2 не требует результата M1 (контракт, файл, схема, API-эндпоинт). Если требует — они зависимы, serial.
   - **No shared write targets:** нет файлов, в которые пишут два+ milestone (кроме чисто append-only журналов — их можно считать независимыми).

При обоих `true` → invoke `superpowers:subagent-driven-development`: dispatch свежий субагент на каждый milestone с двухэтапным ревью (spec compliance + code quality). Каждый субагент следует TDD в своём чистом контексте.

Before dispatching, apply `shared.md §Subagent Dispatch Contract` to every subagent prompt, Codex batch, or delegated implementation handoff. If producer/consumer surfaces differ, also attach the `skills/pipeline/references/contract-handoff.md` handoff so every agent consumes the same contract delta. If owner files, contracts, verification commands, or stop conditions cannot be written, run serial TDD or stop for clarification.

**Manual override (в execution proposal):**

- `--serial` — форсировать serial TDD даже при выполненных условиях (например, когда пользователь хочет пошагово видеть прогресс).
- `--subagents` — форсировать subagent-driven даже при неполных условиях (на свой риск; пользователь принимает риск конфликтов).
- `--codex-batched` — использовать Codex batch execution по правилам `shared.md §Codex-Orchestrated Planning and Execution` (только после preflight и явного выбора пользователя).

Если override не указан — применяется default по условиям выше. Состояние выбора (`execution_mode: "serial" | "subagent-driven" | "codex-batched"`) фиксируется в state.json в блоке `phase_7_implementation` перед началом первого milestone.

**Cross-platform note:** если выбранный `collaboration_profile` или `executor` предполагает делегирование другой платформе, subagent-default оценивается платформой-исполнителем, не вызывающей. Вызывающая платформа получает результат через verification step и проверяет что выбранный mode зафиксирован в implementation report.

### Retry Discipline

See `skills/pipeline/references/shared.md` §Retry Discipline.

### Unattended Attempt Budget Stop Rule

See `skills/pipeline/references/autonomy-safeguards.md` §Unattended Attempt Budget Stop Rule.

Apply this only for `full_autonomous` or `overnight`. Interactive and guided-autonomous runs stop and ask after the retry budget instead of silently skipping.

### Skipped or Deleted Tests Policy

See `skills/pipeline/references/shared.md` §Skipped or Deleted Tests Policy.

If a test is removed, skipped, loosened, or quarantined during autonomous implementation, document why and add replacement coverage or residual risk before continuing.

### Cross-platform verification (only when `executor_option_b_delegated_platform` was chosen)

F-037 disambiguation: this Option B is the **executor-delegation** route (implementation handed to the other platform), not the planning-phase `planning_option_b_cross_review`.

When the other platform finishes implementation, the calling platform MUST verify the work before proceeding to Phase 7.5:

1. **Review changes:** run `git diff` (or `git diff --stat` for overview) to see everything the other platform changed
2. **Run validation:** execute all milestone validation commands from the implementation plan
3. **Run tests:** run the project test suite to catch regressions
4. **Fix loop:** if tests fail or validation breaks:
   - If delegated to Codex via MCP: use `mcp__codex__codex-reply` with the `threadId` to ask Codex to fix specific issues. Repeat until passing.
   - If delegated to Claude Code: the user relays the fix request.
5. **Commit and push:** once validation passes, create a git commit with the implementation results and `git push` to GitHub. This creates a second checkpoint — compare the backup commit (Phase 0) with the implementation commit to see the full diff

Note: both platforms share the same filesystem when running on the same machine. Codex via MCP writes files directly — no git push needed for transfer. Git is used for safety (backup, diff review, rollback) not for transport.

Required output:
- `implementation report`
- updated spec/plan status
- `verification log`

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_7_implementation.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_7_5_review"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_7_implementation completed"`

## Phase 7.5: Review Gate

Before runtime acceptance, require a review checkpoint for high-value work.

### Context Hygiene Gate

See `skills/pipeline/references/shared.md` §Context Hygiene Gate.

Before launching reviewers, build a review pack with the approved scope, changed files, exact diff, verification evidence, and residual risks. Keep unrelated logs, old chat context, and unused oracle material out of the review input.

### Scope and Diff Audit

See `skills/pipeline/references/shared.md` §Scope and Diff Audit.

Run this before the Review Menu. Unexpected files or behavior changes must be explained, reverted, or added to the plan with rationale before review begins.

### Skipped or Deleted Tests Policy

See `skills/pipeline/references/shared.md` §Skipped or Deleted Tests Policy.

The Review Gate must explicitly account for any deleted, skipped, weakened, or excluded tests.

### Test Adequacy Review

See `skills/pipeline/references/test-adequacy-review.md`.

Run TAR for test-changing, behavior-changing, Codex-heavy, full_autonomous, or overnight work before runtime acceptance. the human operator is not expected to personally judge test adequacy; a green test suite is not enough if tests are weak.

### Review Quality Lenses

See `skills/pipeline/references/shared.md` §Review Quality Lenses and `skills/pipeline/references/review-quality-lenses.md`.

Before the Review Menu or any cross-agent review, tell the reviewer to cover at least correctness, readability, architecture, security, and performance, then add context-specific lenses such as UX, migrations, data, compatibility, observability, cost, legal, accessibility, reliability, privacy, rollout, support, or test adequacy.

Minimum review pack:
- summary of the chosen approach
- changed files
- tests added
- regression results
- unresolved risks

Apply the profile-specific review overlay from `skills/pipeline/references/collaboration-profiles.md` before the Review Menu. **Precedence (F-036):** Review Menu user choice wins over profile overlay. The profile overlay only applies for layers the user did not explicitly select or skip in the Review Menu; an explicit user choice in the Review Menu is authoritative.

- `solo_primary` — main review plus baseline review.
- `claude_main_codex_checkpoints` — primary final review plus secondary cross-review when available.
- `dual_head_quality` — Claude and Codex both review; findings are ratified.
- `codex_heavy_claude_guardrails` — Codex self-review plus Claude final-review, with TAR between them.

Preferred review sources:
- human review
- **REQUIRED baseline:** `superpowers:requesting-code-review` — dispatches a code-reviewer subagent that independently checks code quality, architecture, testing, and requirements compliance. Запускается всегда, независимо от risk level.
- security review when auth/input/security surfaces changed

If review is skipped, record:
- why it was skipped
- what risk remains
- why the pipeline is still proceeding

### Review Menu

See `skills/pipeline/references/shared.md` §Review Menu Template.

Параметры для hard:
- `<CLASS>` — из Phase 1 brief
- `<RISK>` — risk level из spec
- `<SECURITY_AUTO>` — см. `skills/pipeline/references/shared.md` §Security Scan Auto-Trigger Paths
- `<SHOW_CROSS_CHECK>` = `true` (hard поддерживает /cross-check)

Обработать выбор пользователя ДО запуска любого ревью-слоя.

### Security Scan (auto-trigger + menu option)

See `skills/pipeline/references/shared.md` §Security Scan Auto-Trigger Paths.

При сработавшем триггере — запустить `/codex-security-scan` автоматически, отметить `[✓]` в Review Menu.

Также доступен как ручной пункт через `+codex-security-scan` в меню.

### Parallel Critics (optional review layer)

> **Активация:** только если пользователь явно выбрал пункт 1 в Review Menu. По умолчанию не запускается.

Full critics protocol — task class detection, presets, dispatch contract (REQUIRED sub-skill `superpowers:dispatching-parallel-agents`, strict JSON output contract), finalizer Hard Rules, severity-based re-check, escalation stop conditions, and state.json logging: read `skills/pipeline/references/parallel-critics.md` (F-023 dedup executed 2026-06-09).

### Iterative Review Loop

Если ревью вернуло замечания:

1. Исправить замечания по формату Accept or Argue (см. `superpowers:receiving-code-review`)
2. Переотправить на повторное ревью — проверить что правки действительно решили проблему
3. До 3 раундов: ревью → правки → повторное ревью
4. После 3 раундов без полного одобрения — показать пользователю сводку нерешённых замечаний и спросить:
   - **ещё раунд** — продолжить review loop (начать раунд 4)
   - **принять как есть** — зафиксировать нерешённые замечания в "residual risks" секции отчёта Phase 8 и перейти к acceptance

Применяется к любому источнику ревью: human review, code-reviewer субагент, Codex, cross-check.

### Cross-Agent Review (menu option)

**Активация:** только если пользователь выбрал пункт 2 в Review Menu. На `high-risk` — предустанавливается `[x]`. Ревьюер определяется автоматически по текущей платформе (см. `orchestration.md §Reviewer Selection`, entry under `shared.md §Cross-Agent Review Template`).

See `skills/pipeline/references/shared.md` §Cross-Agent Review Template.

Параметры:
- `<ARTIFACT>` = `code`
- `<ENTRY_PHASE>` = Phase 7.5 (Review Gate)
- `<EXIT_PHASE>` = Phase 8 (Runtime Acceptance)
- `<REVIEW_FOCUS>` = `bugs, security issues, race conditions, error handling gaps, performance problems`
- `<DOC_OR_DIFF>` = changed files + git diff

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_7_5_review.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_8_runtime_acceptance"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_7_5_review completed"`

## Phase 8: Runtime Acceptance

**REQUIRED:** Invoke `superpowers:verification-before-completion` before claiming work is done.

If implementation was delegated to another platform (Option B), review its implementation report and verification evidence before proceeding. If implementation was local (Option A), perform acceptance checks directly here.

Passing tests are necessary but not sufficient.

When the product lives in a real runtime, require concrete acceptance work:

### Verifiable Acceptance Criteria

See `skills/pipeline/references/shared.md` §Verifiable Acceptance Criteria.

Runtime acceptance must map each acceptance criterion to command evidence, screenshots, logs, transcripts, or an explicit manual check with observable expected behavior.

### Browser And Manual Evidence Acceptance

See `skills/pipeline/references/browser-acceptance.md`.

For hard mode, user-facing web UI changes require browser-based e2e validation when available. If automation is unavailable, use documented manual browser evidence and record the skipped automation as a deferred decision or residual risk.

For user-facing web UI acceptance, the report must name route/page, mobile and desktop viewport or a skip reason, user steps, expected visible result, negative check, and Playwright / agent-browser / project e2e / documented manual browser evidence. Usually this packet is not needed for backend-only work with no visible user surface, but if a route can prove acceptance, use it or record a skip reason.

### Ship Readiness

See `skills/pipeline/references/shared.md` §Ship Readiness and `skills/pipeline/references/ship-readiness.md`.

Read this before final release-facing acceptance when the change affects real users, production runtime, launch, rollout, pricing, data, or operations. If the hard run is design-only or local-only, record `Ship Readiness: N/A` with a reason.

### CVE Scan (baseline — mandatory)

See `skills/pipeline/references/shared.md` §CVE Scan (baseline).

Применимость для hard: **high/critical — абсолютный блок** (rollout не происходит); medium → accepted risk только с обоснованием в Phase 9 (Deferred Decisions); low → упомянуть в отчёте Phase 10, без блока. Инструмент не установлен → warning + запись в residual risks + deferred decision «установить сканер». **Пропуск — только через deferred-decisions.**

### Smoke-test инструменты

See `skills/pipeline/references/shared.md` §Smoke-Test Tools Table.

### Security + Cross-check — через Review Menu

Оба инструмента (`/codex-security-scan` и `/cross-check`) доступны как пункты в Review Menu (Phase 7.5). Если пользователь выбрал их там — они уже запустились.

Если в Phase 8 обнаружены новые security-concerns или архитектурные развилки, которые не были очевидны в Phase 7.5 — можно запустить вручную через `/codex-security-scan` и `/cross-check` явно.

### Compact checkpoint

Перед переходом к Phase 9: если сессия длинная (50+ tool calls), предложить `/compact`. Не компактить посреди имплементации или между тестами и фиксами. Перед compact — убедиться что текущий статус задачи, список изменённых файлов и результаты тестов записаны в plan/report.

### Skipped or Deleted Tests Policy

See `skills/pipeline/references/shared.md` §Skipped or Deleted Tests Policy.

Runtime Acceptance must explicitly account for any deleted, skipped, weakened, or excluded tests before moving to deferred decisions or final handoff.

The agent should keep fixing issues until:
- acceptance passes
- or only risky/deferred items remain

Required output:
- `acceptance evidence pack`
- screenshots, logs, transcripts, or command evidence as applicable
- rollout checklist status
- monitoring plan for the first post-change window

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_8_runtime_acceptance.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_9_deferred"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_8_runtime_acceptance completed"`

## Phase 9: Deferred Decisions

Dangerous actions must be isolated instead of blocking the whole run.

Examples:
- destructive migration
- production deploy
- data deletion
- secret-dependent action
- irreversible integration action
- privileged infrastructure change

For each deferred item, record:
- what was not done
- why it is risky
- what is already prepared
- what the human needs to approve or supply
- the exact next command or action
- expected follow-up verification

The pipeline is successful if all safe work is finished and only deferred-danger items remain.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_9_deferred.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_10_handoff"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_9_deferred completed"`

## Phase 10: Final Handoff

When the user comes back, they should see:
- a finished or near-finished implementation
- passing tests and verification evidence
- runtime acceptance evidence
- exact deferred-danger items
- recommended next steps

Write `docs/reports/YYYY-MM-DD-<topic>-implementation.md` with:
- requirements summary
- boardroom findings summary
- oracle summary and chat link
- implementation summary
- changed files
- tests and regressions
- runtime acceptance evidence
- review gate result
- rollout checklist result
- monitoring plan
- deferred decisions
- next actions for human review

### Saved Auditor Report

See `skills/pipeline/references/shared.md` §Saved Auditor Report.

For hard mode, the final implementation report doubles as the saved auditor report only if it includes plan-vs-diff, changed files, verification evidence, skipped safeguards, review result, runtime acceptance evidence, and residual risks. Use `skills/pipeline/references/report-status-evidence.md` for the human-readable impact and evidence shape. Otherwise, create a separate `docs/reports/YYYY-MM-DD-<topic>-audit.md` before final handoff.

### Skill Behavior Evals and Scorecard

See `skills/pipeline/references/shared.md` §Skill Behavior Evals and Scorecard.

If this task changed skill, prompt, or agent behavior, final acceptance must include scorecard results, clean-context scenario outcomes, and explicit residual risk for any scenario not run.

Skill-change acceptance gate: final acceptance must include clean-context scenario outcomes, a filled or referenced scorecard, and either measured metrics evidence or an explicit statement that precision, recall, and F1 were not measured with residual risk.

When eval metrics were measured, update `skills/pipeline/evals/metrics.md`; when they were not measured, state that as residual risk instead of inventing precision/recall/F1.

### Сводка изменений для пользователя

See `skills/pipeline/references/shared.md` §User Summary Blocks.

Apply the Chat Summary Gate before Phase 11 or any final answer: show the numbered pluses, risks, security, affected behavior, and unaffected behavior blocks in chat even when the technical report already exists.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_10_handoff.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "phase_11_branch_completion"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_10_handoff completed"`

## Phase 11: Branch Completion

See `skills/pipeline/references/shared.md` §Branch Completion.

Required literal handoff for this mode:
- Before invoking `superpowers:finishing-a-development-branch`, show the User Summary Blocks in the current chat response.
- Use the exact labels from `skills/pipeline/references/report-status-evidence.md`. Do not replace them with `Impact`, `Evidence`, `Risks`, or `Branch Status`.
- A saved report or status file alone is not enough.
- Do not present `Implementation complete. What would you like to do?` until the summary blocks have already been shown.
- invoke `superpowers:finishing-a-development-branch`
- present: `Implementation complete. What would you like to do?`

Применимость для hard: основной блок + GitHub Issue Closure subsection (пункты 1-4 из shared.md — включая создание issues для deferred decisions). Для delegated implementation (Option B) — calling platform запускает `superpowers:finishing-a-development-branch` после верификации делегированной работы.

### State update
- Read `docs/plans/<DATE>-<topic>-state.json`
- Set `phases.phase_11_branch_completion.status = "completed"`, `finished_at = <ISO now>`
- Set `current_phase = "final"`
- Atomic write (write `.tmp` → fsync → rename)
- `git add` state.json + design-doc, `git commit -m "pipeline: phase_11_branch_completion completed"`

## State Persistence

See `skills/pipeline/references/shared.md` §State Persistence Schema v1.

**Phase IDs (hard):** `phase_-1_rigor`, `phase_0_backup`, `phase_1_requirements`, `phase_1_5_practices`, `phase_2_boardroom`, `phase_3_oracle_prep`, `phase_4_oracle`, `phase_5_consolidation`, `phase_6_planning`, `phase_7_implementation`, `phase_7_5_review`, `phase_8_runtime_acceptance`, `phase_9_deferred`, `phase_10_handoff`, `phase_11_branch_completion`.

**Finalization:** когда `phase_11_branch_completion.status = "completed"`, state считается финализированным; resume skips it.

## Automation Hooks

Design this pipeline so it can later be automated further.

Good future automation points:
- issue creation
- branch creation
- context-pack generation
- Repo Prompt bundle generation
- oracle artifact import
- plan-to-Codex handoff
- browser or  messaging platform acceptance runs
- rollout checklist generation
- completion notification back to  messaging platform

## Non-Negotiable Rules

- invocation only via the three single-authority paths in `## Triggered By Router Or Escalation` (explicit request, router-selected hard-mode trigger with rationale, or lite/deep escalation)
- no coding before requirements and artifact generation
- no full stop for routine ambiguity; investigate and continue
- no dangerous action when it can be deferred
- no `done` claim without runtime acceptance evidence where relevant
- no oracle output accepted blindly; always reconcile with the local codebase
- no end-to-end handoff without concrete artifacts in the repo
- no hard-pipeline completion without explicit review, rollout, and monitoring posture
- mirror the language of the user's request in all artifacts
- update existing design docs instead of creating duplicates

## Appendix: /codex:adversarial-review (optional plugin)

Not part of the main flow. Full install/usage/warnings and its relation to Cross-Agent Review: read `skills/pipeline/references/orchestration.md` §Optional Plugin: /codex:adversarial-review (moved 2026-06-09).
