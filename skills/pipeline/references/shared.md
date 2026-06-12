# Pipeline Shared Blocks

Каноничные определения блоков, переиспользуемых между `pipeline-lite`, `pipeline-deep`, `pipeline-hard`. Каждый mode ссылается сюда через `See skills/pipeline/references/shared.md §<Section>` и добавляет свои mode-specific override-ы рядом с ссылкой.
**Portable paths (F-064):** all `skills/pipeline/...` paths are relative to the package root; in installed copies (`~/.claude/skills/...`, `~/.codex/skills/...`), resolve relative to the current skill directory. **the human operator (F-066):** the human operator = the human operator / user; "ask the human operator" = "ask the human user".
**Правило изменений:** правка блока здесь — точка синхронизации всех трёх режимов. Если mode хочет отойти от canonical — override остаётся в SKILL.md конкретного режима, shared.md не меняется.

---

## Language Rule

Mirror the language of the user's request. If the user writes in Russian, write all artifacts (spec, report, milestones, design-doc) in Russian. Do not switch to English unless the task itself was asked in English.

---

## Baseline Gates

Запускаются перед переходом к следующей Phase. Отсекают класс проблем, критичный для любого проекта независимо от контекста задачи.

1. **Secret scanning** — `gitleaks detect --no-git -v` по рабочему дереву.
   - Если инструмент не установлен: предупредить, продолжать, но вывести warning в residual risks / отчёт.
   - На hit (severity ≥ medium): остановить pipeline, спросить пользователя перед продолжением.
2. **Lockfiles integrity** — согласованность lockfile с source-of-truth:
   - Python: `pip-compile --check` или проверка, что `requirements*.lock` соответствует `pyproject.toml`/`requirements.in`.
   - Node: `npm ci --dry-run` или `pnpm install --frozen-lockfile --dry-run`.
   - Go: `go mod verify`.
   - Если lockfile отсутствует — Warning: «lockfile не найден, воспроизводимость не гарантируется. Продолжать?»
3. Зафиксировать результат baseline-gates коротким блоком в отчёте (`Baseline Gates Result`).

Если baseline-скан не проходит — это не «фоновая подсказка», а решение пользователя. Молча игнорировать нельзя.

**Applicability per mode:**
- `lite`: mandatory. Go опционален (чаще стек Python/Node).
- `deep`: mandatory. Все 3 стека обязательны при наличии соответствующих файлов.
- `hard`: mandatory. Пропуск — только через deferred-decisions с явным обоснованием.

---

## CVE Scan (baseline)

Прогнать сканер уязвимостей зависимостей в зависимости от стека:

- Python: `pip-audit` или `trivy fs .`
- Node: `npm audit --audit-level=high` или `pnpm audit --audit-level high`
- Go: `govulncheck ./...`

**Severity rule:**
- **high/critical** — блокировать merge
- **medium** — задокументировать как accepted risk в отчёте (для hard — только через deferred-decisions с обоснованием)
- **low** — игнор / упомянуть в отчёте, без блока

Если инструмент не установлен — warning (не блок), запись в отчёт / residual risks. Для hard — добавить deferred decision «установить сканер».

**Applicability per mode:**
- `lite`: Phase 4 (Verify). Высокие severity блокируют merge.
- `deep`: Phase 7 (Acceptance). Высокие — блок.
- `hard`: Phase 8 (Runtime Acceptance), mandatory. **High/critical — абсолютный блок** (rollout не происходит).

---

## Input Validation Checklist

For each external input (HTTP request body, query param, env var, file upload, queue message, third-party webhook payload). The listed input examples are not exhaustive. Add any project-specific trust boundary:

| Входная точка | Тип/Схема | Валидация | Ошибка при несоответствии |
|---------------|-----------|-----------|---------------------------|
| <name> | <type / Pydantic model / Zod schema / JSON schema> | <library / manual> | <HTTP 400 / log + drop / 422> |

Если у задачи нет внешних входов — явно написать `Input Validation: N/A (no external inputs)`.

**Applicability per mode:**
- `lite`: Phase 2 (Compact Spec), обязательная секция.
- `deep`: Phase 4 (Spec), обязательная секция.
- `hard`: Phase 5 (Consolidation), обязательная секция.

---

## Assumptions Section

Keep assumptions in a dedicated section. Never hide them inside milestone prose.

```md
## Assumptions
- <explicit assumption about the task, environment, or constraints>
```

---

## Grounding Required

Uncertain language must not silently pass into planning, implementation, or completion claims.

Trigger phrases include: `probably`, `seems`, `likely`, `should work`, `I think`, `возможно`, `похоже`, `скорее всего`, `кажется`, `должно работать`.

When a trigger phrase appears in a spec, plan, review, report, or final answer, do one of three things:
- replace it with evidence: command output, test result, file reference, source link, or observed runtime behavior;
- move it into `## Assumptions`;
- record it as `residual risk` if evidence is not available.

Do not use uncertain phrasing to close a verification gate.

**Applicability per mode:**
- `lite`: spec, execution notes, verification, and final report.
- `deep`: discovery, spec, planning, execution, acceptance, and report.
- `hard`: all phases; unresolved uncertainty must be a deferred decision or residual risk before finalization.

---

## Source Grounding
Progressive pointer: read `skills/pipeline/references/source-grounding.md` when a task depends on an external library, API, SDK, framework, CLI, protocol, vendor service, or versioned behavior.
Use local dependency versions and official docs before writing code from memory. Context7 when available can provide current library/API docs; if unavailable, fall back to local dependency files, official docs/GitHub, or a recorded assumption/residual risk.

## Context Hygiene Gate

Before planning or executing large work, make context an explicit budget instead of an accidental dump.

Minimum checklist; add task-specific context limits when needed:
- list the files, docs, skills, MCP servers, and tools that are allowed for the next phase;
- prefer `rg`, targeted file reads, summarized logs, and exact line references;
- cap noisy command output with targeted commands, `tail`, or tool output limits;
- avoid loading global or unrelated docs unless they directly affect the task;
- if context is already large or stale, consider compacting or starting a fresh task context before execution.

**Applicability per mode:**
- `lite`: recommended for medium-risk work; keep it short.
- `deep`: mandatory in Phase 2 context gathering, Phase 5 planning, and Phase 6 execution.
- `hard`: mandatory in boardroom/oracle prep, consolidation, implementation, and review gates.

Autonomy safeguards live in `skills/pipeline/references/autonomy-safeguards.md`: ## Autonomous Backup Gate; before guided_autonomous, full_autonomous, overnight, Codex-batched, or subagent-driven execution; record the backup ref; ## Pre-Autonomy Context Freeze And Compact Gate; write the durable task brief; record open questions; Only then compact; ## Independent Parallel Execution Default; When the platform and governing instructions allow subagents; prefer parallel subagents for independent milestones; Immediate blocking work stays local; no shared write targets; ## Unattended Attempt Budget Stop Rule; Only for `full_autonomous` or `overnight` execution in `pipeline-deep` or `pipeline-hard`; attempts >= 3; mark the milestone `failed` or `blocked`; continue with independent unaffected milestones.

---

## Verifiable Acceptance Criteria

Every milestone must be independently checkable before implementation starts.

Valid validation forms:
- a runnable command, such as a test, build, lint, smoke script, `curl`, CLI invocation, or browser automation check;
- an explicit manual check with expected observable behavior when no command exists yet.

Invalid validation forms:
- `works`, `looks good`, `make it better`, `should be fine`, or any statement that cannot be falsified.

If a milestone cannot name a validation command or explicit manual check, it is not ready for execution. Split it, clarify it, or move the uncertainty into assumptions/residual risk.

**Applicability per mode:**
- `lite`: required in the compact spec and each milestone.
- `deep`: required in the spec, planning handoff, and acceptance.
- `hard`: required in consolidation/spec, implementation handoff, and runtime acceptance.

---

## Scope and Diff Audit

Before review or acceptance, compare the actual diff against the approved scope: run `git diff --stat` and `git diff --name-only <base>...HEAD` when a base exists, compare changed files to the spec/handoff, and explain, revert, or explicitly add unexpected file or behavior changes before review proceeds.

**Applicability per mode:**
- `lite`: recommended in Verify; required for medium-risk or multi-file changes.
- `deep`/`hard`: mandatory before Review Menu / Phase 7.5 and final acceptance.

---

## Scope Completion Audit

When a plan, task brief, issue, TODO list, or handoff names explicit work, classify each item before final acceptance as `DONE | PARTIAL | NOT DONE | CHANGED | UNVERIFIABLE`.
Modes: `diff-verifiable` repo evidence, `cross-repo` reachable sibling/path check, or `external-state` dashboard/service/runtime proof. Do not mark an item DONE only because a related file changed; cite proof of the requested deliverable, or for `UNVERIFIABLE` name the exact manual check or handoff.

---

## Ambiguity Scanner

Before implementation planning or execution, scan the task brief, spec, and implementation plan for unresolved choice language.

Trigger terms include: `or`, `either`, `maybe`, `TBD`, `optional`, `not sure`, `или`, `либо`, `может`, `возможно`, `не знаю`, `наверное`.

For each real ambiguity, convert it into an explicit decision, move it into `open_questions` or ask the user if it blocks implementation, or record it as a deferred decision or residual risk if it is intentionally out of scope.

Conflicts are not ambiguity to average away. When requirements, sources, files, or established code patterns contradict, pick one line explicitly, ask the user when that choice is blocking, or record the rejected line as out of scope. Do not blend contradictory patterns into a compromise implementation.

Ignore false positives where the word is part of fixed terminology or a clearly resolved alternative. Do not let unresolved ambiguity pass into an implementation handoff.

**Applicability per mode:**
- `lite`: required before executing medium-risk or multi-file work.
- `deep`: mandatory in spec and planning before handoff.
- `hard`: mandatory in consolidation, planning, and delegated execution handoff.

---

## Clean-Context Plan Review

Review the written plan from a fresh-context perspective before implementation starts.

The reviewer receives only the approved spec or plan, the relevant contracts, and the acceptance criteria. The review asks at least:
- what is clear enough to implement;
- what is ambiguous or missing;
- what would block implementation;
- whether acceptance criteria are verifiable; plus any context-specific risk the plan shape exposes.

Treat findings with judgment. Fix blockers around scope, contracts, data, UI/API behavior, tests, or acceptance. Record minor preference comments as non-blocking notes or reject them with rationale.

**Applicability per mode:**
- `lite`: recommended for small work, required for medium-risk or multi-file feature/refactor work.
- `deep`: mandatory after spec and before planning handoff.
- `hard`: mandatory after consolidation and before implementation planning.

---

## Spec Regeneration Rule

When a spec or plan is structurally wrong, fix the source artifact instead of stacking corrective chat follow-ups.

Use this when the plan:
- chooses the wrong scope;
- misses a required contract;
- contains unresolved ambiguity after the Ambiguity Scanner;
- produces tasks that are not independently verifiable;
- depends on hidden chat context that is not written in the artifact.

Procedure:
1. Edit the `draft.md`, spec, or implementation plan source.
2. Regenerate or rewrite the downstream artifact from the corrected source.
3. Re-run the Ambiguity Scanner and Clean-Context Plan Review.

Follow-up chat messages are allowed only for small clarifications; structural plan repair must edit the source artifact. Do not start implementation from a plan known to contain stale assumptions.

---

## Saved Auditor Report

After implementation and before final handoff, save an auditor report under `docs/reports/`.

Minimum content; add task-specific evidence when context suggests:
- approved scope and changed files;
- `git diff --stat` summary;
- plan-vs-diff check;
- tests, builds, linters, smokes, and their results;
- skipped safeguards;
- unexpected files or behavior changes;
- residual risk and deferred decisions.

The auditor report may be short, but it must be a durable artifact. Chat-only audit notes do not close this gate.

**Applicability per mode:**
- `lite`: required for medium-risk or multi-file changes; optional for trivial single-file fixes.
- `deep`: mandatory in Report and Review.
- `hard`: mandatory before final runtime acceptance and handoff.

---

## Skipped or Deleted Tests Policy

Deleting, skipping, quarantining, or weakening a test is a risk-bearing change.

If a test is removed, skipped, marked flaky, loosened, or excluded from verification:
- explain why, name replacement coverage, record it in the implementation report, and keep incomplete coverage as residual risk.

Never delete a failing test only to make the pipeline pass. If a test is wrong, prove it is wrong with a focused note and preserve the intended behavior in a corrected test.

Applicability: `lite` during Execute/Verify; `deep` during Execute/Acceptance; `hard` during Autonomous Implementation, Review Gate, and Runtime Acceptance.

## Test Adequacy Review

This is a progressive disclosure pointer. Read `skills/pipeline/references/test-adequacy-review.md` when tests are written, changed, used as regression proof, or when work is test-changing, behavior-changing, Codex-heavy, `full_autonomous`, or `overnight`.

---

## Review Quality Lenses
Progressive pointer: read `skills/pipeline/references/review-quality-lenses.md` when reviewing a plan, spec, code diff, generated implementation, or cross-agent handoff.
Review must cover at least correctness, readability, architecture, security, and performance. Then add any task-specific risks the context suggests, such as UX, migrations, data, compatibility, observability, cost, legal, accessibility, reliability, privacy, rollout, support, or test adequacy. Do not stop at these five if the task requires more.

---

## Ship Readiness
Progressive pointer: read `skills/pipeline/references/ship-readiness.md` when the change can affect real users, production runtime, launch, rollout, pricing, data, or operations.
For docs-only, skill-only, local refactor, or test-only work with no runtime launch impact, record `N/A` with a reason instead of loading the full checklist.

---

## Lightweight Memory Bank
Keep reusable project knowledge in files, not in ever-growing global instructions. Default location: `docs/agent-memory/` with a short `index.md`.
This memory is repo-local and agent-agnostic. Claude Code, Codex, and other coding agents should read the same project memory files. Agent-specific memory is allowed only for tool-local cache or private UI state.
Good entries: repeated agent mistakes and fixes; project facts future agents rediscover; known-good command examples; runbooks; lessons learned from tool failures or reviews.
In this compact convention, do not build a memory engine. No decay, scoring, daemon, sync service, vector DB, or automation is required. If a project already has a memory system, reference it instead of creating a duplicate.
Use this rule to keep `AGENTS.md`, `CLAUDE.md`, and `shared.md` short. Put durable local knowledge in memory files or runbooks.

---

## Tool and Model Routing Matrix
Choose the lightest tool that can produce evidence for the current task.

Before choosing specialized tools, check `skills/pipeline/references/tool-inventory.md` (or the equivalent active skill copy) for the current local Claude Code and Codex inventory. Treat it as a snapshot: available does not always mean enabled, authenticated, or appropriate.

## Deterministic Before Model
If code, a script, parser, query, formula, table lookup, status code, or test can answer exactly, use that deterministic route before asking a model to decide. Use the model for judgment calls: unclear tradeoffs, classification of ambiguous unstructured input, drafting, summarization, review, or synthesis. If a deterministic route and a model disagree, treat the deterministic evidence as the default and record why any exception was chosen.
| Task type | Preferred route |
|---|---|
| planning/research | strongest reasoning model plus targeted local docs/search |
| small edits | current coding agent with local tests |
| broad implementation | planned batches, subagents, or Codex only with contracts |
| audit/review | independent reviewer or cross-agent review after deterministic checks |
| browser acceptance | Playwright MCP/CLI, `agent-browser`, project Playwright tests, or documented manual browser smoke |
| AI trace debugging | trace/log review before prompt or code edits |
| knowledge lookup | `rg`, local dependency versions, official docs, and Context7 when available before RAG |

Record explicit deviations in the implementation report when a heavier tool is used for a small task or a weaker tool is used for high-risk work.

## CLI Recipes and Tool Failure Log
Fragile tool syntax should become a reusable recipe.
When a CLI, MCP, browser runner, auditor, or code agent fails because of command syntax, argument order, missing env, timeout, or context mismatch:
- save the known-good command in `docs/agent-memory/` or a focused runbook;
- include the exact command, working directory, required env vars, and expected output shape;
- record the incident in a short failure log entry;
- update a skill only when the lesson is broadly reusable across projects.

Every recipe should identify one known-good command and one failure mode it prevents.

---

## Prototype And Trace Practices
This is a progressive disclosure pointer. Read this reference when a task has uncertain tool syntax, API contracts, risky implementation paths, AI-app debugging, or repeated agent/tool quality failures.
Detailed workflow: `skills/pipeline/references/prototype-trace.md`.

---

## Skill vs Runbook vs CLI Decision Rule
Choose the smallest durable artifact:

- **Runbook:** project-specific steps, deployment notes, local service commands, one repo's conventions.
- **CLI:** deterministic repeated operation with arguments, API calls, parsing, or secret handling.
- **CLI + skill:** the operation is both deterministic and judgment-heavy; the CLI performs mechanics, the skill teaches when and how to use it.
- **Skill:** reusable cross-project judgment, workflow, or technique that cannot be fully automated with a command.
- **Global instructions:** only universal discipline, safety, and routing rules.

Do not create a skill for a one-off solution. Do not put secrets in skills or runbooks; point to env/config names only.

---

## Skill Packaging and Portability

Use `skills/pipeline/references/packaging.md` when changing, copying, installing, or auditing the `pipeline` skill family.

Read this reference when:
- adding or updating `agents/openai.yaml`;
- changing skill frontmatter, referenced files, eval assets, scripts, or bundled metadata;
- syncing `.codex`, `.claude`, or `pipeline-bundle` copies;
- installing or reviewing third-party skills with scripts, network access, hidden tool assumptions, or special MCP/plugin requirements.

Before claiming a packaging change is complete, run `python3 scripts/validate_pipeline_package.py --repo "$PIPELINE_KIT_ROOT"` with the relevant `--compare-root` active copies, then run the targeted PR-F package tests.

---

## Idea To Ship Stage Gates
Use `skills/pipeline/references/idea-to-ship-gates.md` when a task starts from a raw idea, PRD/spec, architecture uncertainty, implementation chunking, bugfix verification, or release handoff. It augments the current mode; it does not replace run-control, TDD, premortem, source grounding, browser evidence, review, or ship-readiness rules.
---
## Skill Behavior Evals and Scorecard

Use this block when the task changes a skill, prompt, agent workflow, model-routing rule, or other agent behavior. It is mandatory for non-trivial skill, prompt, or agent-behavior changes; optional for typo-only docs edits.

Before implementation:
- define or update clean-context scenarios in `skills/pipeline/evals/behavioral_eval_set.json`;
- include both positive cases and near-miss negative cases;
- name expected behavior and forbidden behavior for each case;
- when practical, compare old vs new or skill vs no-skill behavior instead of judging the new version alone.

Before completion:
- fill a scorecard from `skills/pipeline/evals/scorecard-template.md`; record measured eval metrics in `skills/pipeline/evals/metrics.md` when a routing/discovery or behavioral eval run is performed;
- record whether each scenario passed, failed, or was not run; Do not invent metrics; use `not run` plus residual risk when no clean-context run or manual scoring pass exists;
- treat unrun scenarios as residual risk unless explicitly out of scope;
- preserve existing text regressions, but do not treat text presence as a substitute for behavior evidence.

Skill-change acceptance gate: a non-trivial skill, prompt, routing, model, or agent-workflow change must not be accepted unless the report includes clean-context scenario outcomes, a filled or referenced scorecard, and a metrics decision. The metrics decision must update `skills/pipeline/evals/metrics.md only from an actual clean-context run, transcript review, or labeled manual scoring pass`; otherwise it must explicitly say that precision, recall, and F1 were not measured and record residual risk.
text regressions are not behavior evidence. They can prove instructions are present, but they cannot support claims that behavior improved. Trace-driven refinement: when a scenario fails, inspect the raw artifact first: prompt, transcript, command output, eval result, diff, log, or trace. Do not rewrite the skill blindly from a hunch.

Skill simplifier pass: before accepting the skill change, ask what can be removed, shortened, moved to references, templated, or deferred. Record the result in the implementation report.

**Applicability per mode:**
- `lite`: required for medium-risk or non-trivial skill/prompt changes; keep the scorecard short.
- `deep`: mandatory for skill, prompt, or agent-workflow changes.
- `hard`: mandatory, with explicit residual risk for any scenario not run.

---

## File-First Knowledge Before RAG

Prefer local files, indexes, and `rg` before adding retrieval infrastructure.

Use file-first knowledge when:
- docs can be synced or stored in the repo/private workspace;
- targeted search can find the needed facts;
- conversion of PDFs/DOCX/PPTX on demand is enough;
- the knowledge base is small or changes in understandable file chunks.

Consider RAG only after file-first retrieval fails by a clear criterion, such as repeated misses, too many large documents to inspect, or a need for semantic retrieval across unstructured content. Record that criterion before building RAG.
Code Routing Map: use `skills/pipeline/references/code-routing-map.md` when an existing large, old, or cross-cutting codebase needs a short map from current code to flows, domains, entrypoints, contracts, files, and tests. It routes agents to code; skip it for small local work.

## Subagent Dispatch Contract

Every subagent, Codex batch, or parallel worker must receive a bounded contract before it writes code.

Required fields:
- `owner files`: files or modules this worker owns;
- `allowed files`: files it may edit if needed;
- `forbidden files`: files it must not edit;
- `contracts`: API, schema, UI, or data contracts it must preserve or consume;
- `verification`: exact commands or manual checks it must run;
- `stop conditions`: when it must stop and escalate instead of guessing;
- `final reply`: changed files, tests run, results, deviations, and open risks.

Do not dispatch parallel implementation when workers share write targets, depend on each other's uncommitted outputs, or lack a written contract.

**Applicability per mode:**
- `lite`: only when manual subagent delegation is explicitly chosen.
- `deep`: mandatory before subagent-driven development or Codex-batched execution.
- `hard`: mandatory before any subagent team, Codex batch, or delegated implementation engine.

## Planner Generator Evaluator Roles
This is a progressive disclosure pointer. Read this reference when task risk or size justifies separating planning, implementation, and evaluation.
Detailed workflow: `skills/pipeline/references/planner-evaluator.md`.

---

## Milestones Template

Structure subtasks as dependency-ordered milestones with validation commands.

```md
## Milestones
| ID | Title | Depends on | Status |
| M1 | <title> | - | [ ] |
| M2 | <title> | M1 | [ ] |
| M3 | <title> | M1 | [ ] |
| M4 | <title> | M2, M3 | [ ] |

## M1. <Title> `[ ]`
### Goal
- <what becomes true after this milestone>
### Tasks
- [ ] <task 1>
- [ ] <task 2>
### Validation
```sh
<copy-pasteable command>
```
Validation may be an explicit manual check only when no runnable command exists yet. See `shared.md §Verifiable Acceptance Criteria`.
### Stop-and-fix
- If validation fails, fix before moving to dependent milestones.
```

**Mode variations:**
- `lite`: опускает секцию `### Tasks` — milestones в lite обычно атомарны.
- `deep` / `hard`: полная форма с `### Tasks`.

---

## Resume State Block

Add a compact resume section to the design-doc and keep it current: `Current`, `Done`, `Next`, `Blockers`.

---

## Retry Discipline

Repeated test failures degrade solution quality silently — the model may produce calm, methodical reasoning while cutting corners on the actual solution.

1. **First failure:** Invoke `superpowers:systematic-debugging`. Diagnose root cause before changing code.
2. **Second failure (same issue):** STOP fixing. Re-read the milestone, ask whether the approach is wrong, and consider smaller sub-milestones.
3. **Third failure:** STOP completely. Report attempts, cause, alternatives, and ask for guidance or scope change. Never force tests to pass with a workaround.

**Anti-hack check (after every green test):** Re-read the milestone goal and verify each requirement is met substantively, not just formally. A passing test is necessary but not sufficient — the solution must match the goal's intent.

## Human Decision Questions

Use this only when the human operator must make a decision because brainstorming, blocker handling, scope, architecture, contract, security, data, tests, or Claude/Codex disagreement cannot be resolved by a safe reversible default. Do not apply this to Run Control Choices (`C1-C4`, `A1-A4`, `heavy`, `quality`, `night`) or routine progress updates. Ask one decision at a time unless choices are tightly coupled.

Default format: `Нужно твоё решение.`; `Простыми словами:` what happened without jargon; `Технически это называется:` term plus parenthetical plain-language explanation when useful; `Варианты:` two or three options with `Плюс` and `Минус`; `Моя рекомендация:` recommended option and why; `Как ответить:` Напиши `1`, `2` или `делай как рекомендуешь`.

Rules: omit `Технически это называется` if no technical term helps; show at most three options; explain consequences in user/project terms; keep the question short enough to answer in chat; if autonomy allows a safe default, record the decision instead of asking.

## User Summary Blocks

### Chat Summary Gate
Before invoking any branch-completion or finishing sub-skill, the pipeline must show the human-readable impact summary in chat. This is a hard gate because branch-completion sub-skills can otherwise bury the final pros/cons/security/impact summary. Before presenting `Implementation complete. What would you like to do?`, show the chat summary blocks in the current assistant response. A saved report file is not a substitute for the chat summary gate.
After writing the technical report when one is required, **present a summary in the chat** for a non-programmer. If the report file was intentionally skipped for a tiny change, still present the compact chat summary before the final answer. Do this even if no branch-completion step will run or no feature branch was created. Prefer numbered blocks. Use numbered blocks instead of Markdown tables unless the renderer displays tables cleanly. Markdown tables are allowed only when the chat renderer displays them cleanly. For report/status/evidence structure, use `skills/pipeline/references/report-status-evidence.md`.
The summary must list **every distinct change**:

```
### 1. <Изменение>
- Плюсы: ...
- Минусы / риски: ...
- Безопасность: ...
- На что влияет и как: ...
- На что НЕ влияет и почему: ...
```

Do not replace this template with generic `Impact`, `Evidence`, `Risks`, or `Branch Status` blocks. Those headings may appear after the required blocks, but never instead of them.
Field guide: **Изменение** is the plain-language change; **Плюсы** is what became better; **Минусы / риски** is the remaining downside or "—"; **Безопасность** is data/access/input/security impact or "не затрагивает"; **На что влияет и как** is the changed user/operator/system behavior; **На что НЕ влияет и почему** is what stays the same and why.
Final Answer Self-Check: before sending the final answer or presenting branch-completion choices, verify the current chat response contains every required label above. If any required label is missing, rewrite the answer before sending it.
Rules:
- One numbered block per logical change, not per file
- Language must match the user's language (Russian if the user writes in Russian)
- Use plain-language facts only: no guesses, no vague claims, no code, no file paths, no jargon
- The summary is shown **in the chat**, not only in the report file
- Do not ask the branch-completion question until these blocks have already been shown

---

## Branch Completion

After reporting and review, the pipeline must explicitly close the branch lifecycle when work happened on a feature branch or worktree.

- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use `superpowers:finishing-a-development-branch`
- Follow that skill to verify tests, present the exact 4 options, and execute the user's choice
- The required options include: `Implementation complete. What would you like to do?`
- Repository file edits should follow Phase 0 Branch And Worktree Policy. If work somehow ended up directly on `main` or `master` without explicit user approval, stop and ask the user before proceeding.

Stop only after the branch decision is explicitly handled.

### GitHub Issue Closure (deep/hard only, if issue was linked)

Если работа была связана с GitHub Issue — invoke `gh-issues` skill для завершения:
1. Сохранить AI Session Context в комментарий к issue (формат из `gh-issues` skill, секция "AI Session Context"):
   ```bash
   gh issue comment <NUMBER> --body-file .ai-context.md
   ```
2. Закрыть issue с ссылкой на PR/коммит: `gh issue close <NUMBER> -c "Done in PR #<PR>"`
3. Или оставить открытым с обновлённым контекстом, если работа не завершена полностью.
4. (hard only) Создать issues для deferred decisions (Phase 9), если они есть — чтобы не потерялись:
   ```bash
   gh issue create -t "deferred: <description>" -l "backlog" -b "<what was deferred and why>"
   ```

**Applicability per mode:**
- `lite`: основной блок (без GitHub Issue Closure subsection).
- `deep`: основной + GitHub Issue Closure (пункты 1-3).
- `hard`: основной + GitHub Issue Closure (пункты 1-4).

---

## Smoke-Test Tools Table

| Продукт | Инструмент | Как использовать |
|---|---|---|
| Web UI | `agent-browser` skill | Описать сценарий на естественном языке → agent-browser навигирует, кликает, проверяет |
|  messaging platform бот | Telethon тестовое сообщение + проверка логов | `journalctl --user -u <service> -f` |
| CLI / скрипт | Запуск с тестовыми аргументами | Проверить exit code + stdout |
| API | `curl` / `httpie` с тестовым запросом | Сравнить response с ожидаемым контрактом |

**Applicability per mode:**
- `lite`: таблица сокращённая по необходимости (часто  messaging platform/CLI пути).
- `deep` / `hard`: полная таблица, ссылка обязательна.

---

## Cross-Agent Review Template

This is a progressive disclosure pointer. Read this reference when a mode asks for cross-agent plan/code review details, reviewer selection, plugin vs fallback mode, artifact templates, or the Accept-or-Argue loop.

Detailed workflow: `skills/pipeline/references/orchestration.md` §Cross-Agent Review Template.

---

## Codex-Orchestrated Planning and Execution

This is a progressive disclosure pointer. Read this reference when a mode offers Codex-assisted spec, planning, execution, autonomous batches, CLI invocation, prompt contracts, batch rules, or state fields.

Detailed workflow: `skills/pipeline/references/orchestration.md` §Codex-Orchestrated Planning and Execution. Codex Invocation Ladder: read the same reference before any Codex preflight, route selection, bwrap handling, CLI logging, plugin/MCP trade-offs, or Codex-heavy execution.

---

## State Persistence Schema v1

Pipeline maintains a machine-readable state file for resume-after-failure support.

**Location:** `docs/plans/<DATE>-<topic>-state.json` (alongside design-doc, committed to git).

**Schema (v1):**

```json
{
  "schema_version": 1,
  "topic": "<topic>",
  "mode": "pipeline-<lite|deep|hard>",
  "started_at": "<ISO 8601>",
  "last_updated_at": "<ISO 8601>",
  "design_doc": "docs/plans/<DATE>-<topic>-design.md",
  "branch_name": "pipeline-<mode>/<topic>",
  "current_phase": "<phase_id>",
  "open_questions": [],
  "phases": {
    "<phase_id>": {
      "status": "pending | in_progress | completed | skipped | failed",
      "finished_at": "<ISO or null>",
      "reason": "<string when skipped or failed>",
      "milestones": {
        "M<N>": {
          "status": "<same enum>",
          "started_at": "<ISO or null>",
          "finished_at": "<ISO or null>",
          "attempts": 0,
          "last_error": "<short string or null>"
        }
      },
      "critics": {
        "selected": [],
        "rounds": [],
        "status": "pending | in_progress | completed | escalated"
      }
    }
  },
  "blockers": []
}
```

**Phase IDs per mode — задаются в SKILL.md каждого режима** (у lite/deep/hard разные phase-id наборы).

**Atomic write:** write to `.tmp`, `fsync`, `mv` over target. Never `>` directly.

**`current_phase` advance rule:** every phase-exit state-update block MUST set `current_phase` to the next phase id in the mode's chain (see each SKILL.md's "Phase IDs" list). The final phase exit MUST set `current_phase = "final"`. Init writes `current_phase` to the first phase that is not already `completed` at init time. Without this, resume can never observe finalization.

**Finalization:** когда `<final_phase>.status = "completed"`, state считается финализированным — resume такой топик пропускает.

**Orphan detection:** на resume — сверить milestone IDs в state.json с design-doc. Отсутствующие ID → пометить `orphaned`, предупредить пользователя.

**Applicability per mode:**
- `lite`: state-persistence НЕ используется (короткие прогоны, resume не нужен).
- `deep`: используется, финал — `phase_9_branch_completion`.
- `hard`: используется, финал — `phase_11_branch_completion`.

## Review Menu Template

Универсальный prompt для единого выбора ревью-слоёв в Phase 7 (deep) / Phase 7.5 (hard). Показывается один раз в начале фазы.

### Параметры

- `<CLASS>` — класс задачи из Phase 1 (`bugfix` / `feature` / `refactor` / `infra`)
- `<RISK>` — risk level (`low` / `medium` / `high`)
- `<SECURITY_AUTO>` — `true|false`, см. `## Security Scan Auto-Trigger Paths`. Если `true` — пункт /codex-security-scan предвключён в меню.
- `<SHOW_CROSS_CHECK>` — `true` для hard, `false` для deep (в deep /cross-check нет)

### UX-prompt

```
Code Review Menu. Класс: <CLASS>, риск: <RISK>.

Baseline (автоматом, не отключается):
  ✓ Secret scan (gitleaks)       — baseline gate
  ✓ CVE scan                     — baseline gate (см. shared.md §CVE Scan)
  ✓ superpowers code-reviewer    — общее ревью (Opus 4.7, ~5-10K tokens)

Авто-триггер (по путям):
  <SECURITY_AUTO=true только>
  [✓] /codex-security-scan       — diff трогает <matched path> → включено

Дополнительные слои (ручной выбор):
  [ ] 1. Parallel Critics          — dimension checks (Haiku 4.5, ~1.5K tokens)
                                      preset: recommended (tests + security + arch)
  [ ] 2. Cross-Agent review (Codex / Claude в зависимости от платформы) — независимый взгляд другой модели (~3-5K tokens)
                                      <РЕКОМЕНДОВАНО [x] если RISK=high>
  <SHOW_CROSS_CHECK=true только>
  [ ] 3. /cross-check (3 модели)   — арх-арбитраж Opus+Codex+Gemini (~10-15K tokens)

Действия:
  Enter            продолжить с базовым набором + авто-триггеры
  1,2,3            выбрать номера
  +N,-M            добавить/убрать
  critics-custom   выбрать роли Parallel Critics вручную
  all              все дополнительные слои
  skip-all-extra   только baseline
```

### Предустановки по RISK

- `low` / `medium`: пункты 1, 2, 3 — по умолчанию `[ ]`.
- `high`: пункт 2 (Cross-Agent review) — по умолчанию `[x]`. Остальные `[ ]`.

### Minimum acceptable evidence per risk level (F-046)
Baseline tools (secret scan, CVE scan, code-reviewer) are always required; missing-tool fallback: `low` — residual-risk record naming tool/reason/unchecked class; `medium` — residual-risk record + user-visible gap before merge, missing CVE scan = blocker unless deferred-decision; `high` — deferred-decision with concrete next steps, no soft-warning fallback. Same rule applies to baseline gates above.
### Обработка выбора

1. Запустить baseline всегда (Secret + CVE + code-reviewer).
2. Если `<SECURITY_AUTO>` — запустить `/codex-security-scan` не спрашивая.
3. Для каждого выбранного пункта — запустить соответствующий под-слой (см. ниже).
4. После всех слоёв — перейти к финальному Acceptance.

### Где вызывается

- `pipeline-deep/SKILL.md` Phase 7 — первым блоком после `verification-before-completion`.
- `pipeline-hard/SKILL.md` Phase 7.5 — первым блоком после verification.
- `pipeline-lite/SKILL.md` — НЕ вызывается (lite не имеет этих слоёв).

## Security Scan Auto-Trigger Paths

Автоматически активирует `/codex-security-scan` если diff трогает любой из этих путей.

### Path globs

- `**/auth/**`, `**/login/**`
- `**/secret*/**`, `**/password*/**`, `**/token*/**`
- `**/oauth*/**`, `**/jwt*/**`
- `**/crypto/**`, `**/encrypt*/**`
- `**/*_security.py`, `**/permissions/**`

### Логика

1. В начале Phase 7 / Phase 7.5 получить список изменённых файлов: `git diff --name-only <base>...HEAD`.
2. Для каждого path выше сделать match против списка изменённых файлов (fnmatch).
3. Если хоть один match — `<SECURITY_AUTO> = true`, matched path передаётся в Review Menu.
4. Запустить `/codex-security-scan <matched_files>` не спрашивая подтверждения у пользователя. Отметить `[✓]` в Review Menu для прозрачности.
5. Если ни один не сматчился — `<SECURITY_AUTO> = false`. Пункт `/codex-security-scan` в меню не показывается автоматом, но доступен через `+codex-security-scan` (ручной add).

### Где используется

- `pipeline-deep/SKILL.md` Phase 7 — перед показом Review Menu.
- `pipeline-hard/SKILL.md` Phase 7.5 — перед показом Review Menu.

## Parallel Critics Presets

Пресеты для выбора ролей critics, когда пользователь активировал Parallel Critics через Review Menu (пункт 1).

### Роли (role pool, 8 штук)

- `arch` — architecture, layering
- `tests` — test coverage, edge cases
- `security` — vulnerabilities, secrets, unsafe calls
- `correctness` — logic bugs
- `equivalence` — refactor safety (behavior preserved)
- `ux_contracts` — API contracts, response compat
- `readability` — naming, style, nits
- `observability` — logs, metrics, tracing

### Пресеты

| Preset | Роли | Токены | Когда |
|---|---|---|---|
| `min` | tests + security | ~1K | Быстрая проверка |
| `recommended` (default) | tests + security + arch | ~1.5K | Типичный случай |
| `full` | все 8 ролей | ~4K | Если явно попросили «всё» |
| `custom` | вручную выбрать из всех 8 | переменная | Явная кастомизация |

### Per-class overrides (добавляются к `recommended`, если не `custom`)

| Class | Override | Почему |
|---|---|---|
| refactor | + equivalence | Уникальная роль для рефакторинга — сравнивает поведение до/после |
| feature + touched paths `**/handlers/**` OR `**/routes/**` OR `**/api/**` | + ux_contracts | Только если задача трогает API |
| infra | + observability | Новый service/handler → проверить логи/метрики |

### Важно

- По умолчанию всегда → `recommended`.
- `correctness` и `readability` НЕ входят ни в один preset по умолчанию. Доступны только через `custom` (это осознанное решение — `correctness` дублирует работу code-reviewer на Opus, `readability` шумит nit-ами).
- Модель критиков жёстко прибита к `claude-haiku-4-5-20251001`. Не менять.
- Лимит 5 concurrent (Hard rule, остаётся как раньше).

### Где используется

- `pipeline-deep/SKILL.md` Phase 7 — Parallel Critics section.
- `pipeline-hard/SKILL.md` Phase 7.5 — Parallel Critics section.
