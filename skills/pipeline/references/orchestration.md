# Pipeline Orchestration Reference

Detailed reference for optional cross-agent review and Codex-assisted planning/execution.

Read this file only when a mode section explicitly calls for Cross-Agent Review or Codex orchestration. Keep `shared.md` as the short index; this file carries the heavier workflow details.

`A3 Full autonomous` and `A4 Overnight` cannot be chosen silently; they require run-control acceptance or an explicit alias such as `heavy`, `ok`, or `night`.

## Cross-Agent Review Template

Parameterized workflow for reviewing an artifact with another model (Claude ↔ Codex).

### Parameters

- `<ARTIFACT>`: `plan` or `code`.
- `<ENTRY_PHASE>`: calling phase, such as Phase 4, Phase 5, or Phase 7.5.
- `<EXIT_PHASE>`: next phase after approval.
- `<REVIEW_FOCUS>`:
  - plan: `architectural issues, security concerns, race conditions, missing edge cases, contract violations`
  - code: `bugs, security issues, race conditions, error handling gaps, performance problems`
- `<DOC_OR_DIFF>`:
  - plan: design-doc path
  - code: `git diff` plus changed-file list

### Reviewer Selection

- If `CLAUDECODE=1`, current platform is Claude Code and reviewer is Codex.
- If `CODEX_SANDBOX` exists or current platform is Codex, reviewer is Claude (`claude -p`).
- If platform cannot be detected, ask the user.

`CLAUDECODE` is an internal Claude Code CLI variable and may change. If detection fails, falling back to asking the user is correct.

### User Prompt

For plan review:

```text
Spec готов. Отправить на ревью в <ревьюер>?

  [Y] Да — независимое ревью design doc другой моделью
  [N] Нет — перейти к планированию
```

For code review:

```text
Отправить код на ревью в <ревьюер>?

  [Y] Да — независимое ревью кода другой моделью
  [N] Нет — перейти к acceptance
```

### Artifact Description Template

For `plan`:

```text
What: [problem being solved]
Approach: [chosen approach and why]
Alternatives considered: [what was rejected and why]
Files to change: [list]
Addressed concerns: [for resubmit, point-by-point from previous review]
```

For `code`:

```text
What changed: [summary of changes]
Key decisions: [non-obvious decisions made during implementation]
Files modified: [list with brief description per file]
Tests: [what tests were added/run, results]
Addressed concerns: [for resubmit, point-by-point from previous review]
```

### Submission

Claude Code -> Codex:

- Prefer `/codex:review --background` or `/codex:adversarial-review --background` when the official `codex-plugin-cc` is installed and `/codex:setup` is healthy, because it gives job management through `/codex:status` and `/codex:result`.
- Use Bash `codex exec` with explicit log files as the fallback when plugin/app-server sandbox is unhealthy or when the run needs a durable prompt/log contract. Prefer this route only after preflight proves it is safe and reproducible in the current environment.
- Use MCP `mcp__codex__codex` only as a last resort for short read-only critique when plugin and direct CLI are unavailable or unsuitable, because MCP calls are blocking in Claude Code and can hang the orchestrator.
- MCP `prompt`: artifact content plus `Review this <ARTIFACT>. Check for: <REVIEW_FOCUS>. Return APPROVED or CHANGES_REQUESTED with specific numbered items.`
- MCP `sandbox`: `"read-only"`
- CLI fallback:

```bash
codex exec --sandbox read-only \
  "Review this <ARTIFACT>. Check for: <REVIEW_FOCUS>. Return APPROVED or CHANGES_REQUESTED with specific numbered items.\n\n<DOC_OR_DIFF_INLINE>"
```

Use the model from `~/.codex/config.toml` or `.codex/config.toml`; this template does not pin a model version. Determine verdict best-effort from `APPROVED` / `CHANGES_REQUESTED` in the response text.

Codex-side review, Codex -> Claude Code:

Use direct CLI through the Claude Invocation Ladder:

```bash
REVIEW_ID="<review-id>"
mkdir -p /tmp/pipeline-claude
claude --print \
  --permission-mode dontAsk \
  "Review this <ARTIFACT>. Check for: <REVIEW_FOCUS>. Return APPROVED or CHANGES_REQUESTED with specific numbered items." \
  < "/tmp/pipeline-claude/${REVIEW_ID}-prompt.md" \
  > "/tmp/pipeline-claude/${REVIEW_ID}-stdout.log" \
  2> "/tmp/pipeline-claude/${REVIEW_ID}-stderr.log"
```

Pass the review prompt and artifact through stdin. Do not use `tail` while the command is running; inspect the saved stdout/stderr logs after the run or at watchdog checkpoints.

Determine verdict best-effort from `APPROVED` / `CHANGES_REQUESTED` in the response text.

### Claude Invocation Ladder

Use this before any Codex-hosted review, checkpoint, or helper call that depends on Claude Code actually running.

1. Check `command -v claude` and `claude --version`.
2. Prefer read-only review prompts with write tools disabled unless the user explicitly asked Claude Code to edit.
3. Pass long prompts and artifacts through stdin from a saved prompt file; do not rely on unsupported file flags.
4. Save stdout and stderr under `/tmp/pipeline-claude/` with a stable review id.
5. If Claude CLI is missing, unauthenticated, over budget, or returns no useful verdict, record the failure and fall back to solo current-model review or another accepted review layer.
6. If the same Claude invocation route fails twice with the same syntax/auth/budget failure, stop that route and record the known-good alternative or residual risk.

Claude CLI status values:

- `claude_cli_ok`: `claude --version` and a short `claude --print` smoke passed.
- `claude_cli_unavailable`: binary missing or not on PATH.
- `claude_cli_auth_or_budget_blocked`: CLI starts but cannot return an answer.
- `claude_cli_read_only_only`: suitable for critique, not for edits.
- `claude_cli_unverified`: no smoke has been run in the current environment.

Direct CLI known-good pattern:

```bash
REVIEW_ID="<review-id>"
mkdir -p /tmp/pipeline-claude
claude --print \
  --permission-mode dontAsk \
  --tools "Read,Grep,Glob,Bash" \
  --disallowedTools "Edit,Write,MultiEdit,NotebookEdit" \
  < "/tmp/pipeline-claude/${REVIEW_ID}-prompt.md" \
  > "/tmp/pipeline-claude/${REVIEW_ID}-stdout.log" \
  2> "/tmp/pipeline-claude/${REVIEW_ID}-stderr.log"
```

For Codex-main + Claude checkpoints, the prompt file must include the artifact or diff, acceptance criteria, review focus, required verdict tokens, and a request for blockers first with reproduction evidence.

### Accept-or-Argue loop

1. If `CHANGES_REQUESTED`, address each item:
   - Fixed: what changed plus file reference.
   - Disagree: counterargument with rationale. If the same finding repeats 2+ times without new content, escalate to the user through `AskUserQuestion`.
   - Deferred: reason, only with user agreement.
   - Then update artifact and resubmit, up to 3 iterations.
2. If `APPROVED`, move to `<EXIT_PHASE>`.
3. If reviewer is unavailable or errors, tell the user and continue without review.
4. After 3 iterations without `APPROVED`, show unresolved items to the user and ask through `AskUserQuestion`. When escalating unresolved reviewer findings to the human operator, use `shared.md §Human Decision Questions`. Always translate the technical concern into plain language first, then keep any necessary technical term with a parenthetical explanation.
   - one more iteration: continue with iteration 4;
   - stop review: record unresolved findings in report residual risks and move to `<EXIT_PHASE>`.

For code review, run after Parallel Critics and `requesting-code-review`. The cross-agent reviewer should focus on model-family blind spots, not issues already covered by the baseline review layers.

## Codex-Orchestrated Planning and Execution

Use inside `pipeline-deep` and `pipeline-hard` when the current model remains the process owner and another local helper handles technical details, planning, review, or code. The current supported helper pair is Claude Code plus Codex. This is not a separate pipeline mode.

### When to Offer

Offer only when at least one condition is true:

- task is large, roughly 10+ TDD tasks or 5+ milestones;
- current session is near limits and the user wants to save context;
- task needs a long technical plan with exact files, tests, and commands;
- user explicitly asks for Codex as executor.

Do not offer for `pipeline-lite`, simple bugfixes, untrusted projects/VPS, or when Codex CLI/MCP is unavailable.

### Profile-driven defaults

When `pipeline-deep` or `pipeline-hard` has already selected a `Model Collaboration Profile`, derive the strategy fields from the profile instead of asking separate spec/planning/executor questions again.

| Collaboration profile | Spec strategy | Planning strategy | Executor | Review overlay |
|---|---|---|---|---|
| `solo_primary` | `current_model` | `current_model` | `current_model` | main review plus baseline review |
| `claude_main_codex_checkpoints` | `cross_review` | `cross_review` | `current_model` | primary final review plus secondary cross-review |
| `dual_head_quality` | `cross_review` | `cross_review` or `codex_tdd_plan` | chosen main executor | mandatory dual review with ratification |
| `codex_heavy_claude_guardrails` | `current_model` broad-plan plus Codex critique | `codex_tdd_plan` | `codex` | Codex self-review plus Claude final-review |

Use the explicit prompts below only as a fallback for legacy runs where no profile was recorded, or when the user changes the profile mid-run.

### Before spec

Prompt before Phase 4 in `pipeline-deep` or Phase 5 in `pipeline-hard`:

```text
Как готовим spec?

  [A] Обычный режим — я сам пишу полный spec
      Быстрее и проще. Подходит, если задача понятная и не слишком большая.

  [B] Spec + проверка второй моделью
      Я пишу spec, потом отправляю его на независимую проверку. Медленнее, но надёжнее.

  [C] Короткий spec + Codex дополняет технические детали
      Я фиксирую цель, границы и риски. Codex расписывает технические детали. Потом я проверяю и утверждаю решения.
```

Defaults:

- `deep`: `A` for ordinary tasks; `C` if the task is large or the current model is near limits.
- `hard`: `C` if Codex is available and the project is trusted; otherwise `B`.

### Before planning

Prompt before Phase 5 in `pipeline-deep` or Phase 6 in `pipeline-hard`:

```text
Кто пишет implementation plan?

  [A] Обычный режим — я сам пишу полный план
      План остаётся полностью в текущей сессии.

  [B] План + проверка второй моделью
      Я пишу план, потом вторая модель ищет пропуски, риски и ошибки.

  [C] Codex пишет детальный TDD-план, я проверяю
      Codex расписывает задачи, тесты, файлы и команды. Я проверяю, что он не вышел за рамки spec.
```

Defaults:

- `A` for small or medium tasks.
- `C` for large tasks with 10+ TDD tasks.
- `B` when independent review is needed but plan delegation is not.

### Before execution

Prompt before Phase 6 in `pipeline-deep` or Phase 7 in `pipeline-hard`, if the plan is ready:

```text
Autonomy from Run Control Choices:

  A1 Interactive — спрашивать перед каждым крупным шагом
      Самый осторожный режим. Медленнее, зато вы контролируете каждый этап.

  A2 Guided autonomous — работать batch'ами, спрашивать только при рисках
      Более осторожный автономный режим. Codex/текущая модель работают сами, но останавливаются при неоднозначности, ошибках тестов или выходе за scope.

  A3 Full autonomous — Codex делает batch'и сам, я проверяю между batch'ами
      Рекомендуемый режим. Максимальная автономность для trusted проекта/VPS после run-control acceptance.

  A4 Overnight — ночная автономная смена по night protocol
```

Default is `A3 Full autonomous`.

`A3 Full autonomous` can be used as the accepted run-control default after the user sees the menu or says `ok`. `A4 Overnight` still requires explicit confirmation of the night protocol.

### Preflight

Before planning option `C`, Codex executor, autonomy `A3`, or autonomy `A4`, check:

- project is not on `main` or `master`;
- git state is clean or understood;
- Codex CLI or MCP is available;
- Before launching Codex, read `skills/pipeline/references/orchestration.md` §Codex Invocation Ladder and the selected route's command template;
- Do not invoke Codex from memory, stale chat snippets, or an unverified command pattern;
- Codex Invocation Ladder route selection is recorded; record the exact route, command shape, cwd, prompt path, logs, and watchdog cadence before launch;
- Codex sandbox status is known from a short smoke test or existing machine memory;
- project/VPS is trusted;
- user explicitly allowed autonomous mode if `[3]` or `[4]` is needed.

If preflight fails, fall back to `A` or `B` and record the reason in report/residual risks.

### Codex Progress Watchdog

After launching async/background Codex work, follow `skills/pipeline/references/autonomy-safeguards.md` §Codex Progress Watchdog. The orchestrator must check status/result/logs within 1 minute to confirm Codex actually started, then poll on the duration-based cadence from that reference: check every 5 minutes for runs up to 20 minutes, check every 10 minutes for runs from 20 minutes to 2 hours, and check every 20 minutes for longer or overnight runs unless a stricter cap applies. Treat failed before useful work, blocked, waiting for input, or stuck progress as a stop condition that needs an orchestrator decision instead of passive waiting.

### Codex Invocation Ladder

Use this before any Codex-heavy execution, Codex TDD planning, or cross-agent review that depends on Codex actually running. The goal is to avoid the repeated failure pattern where Claude tries MCP, hits the same sandbox problem, then improvises a dangerous CLI command without logs or guardrails.

#### Route inventory

| Route | Best use | Pros | Cons / failure modes |
|---|---|---|---|
| `codex-plugin-cc` official Claude Code plugin | One-shot review, adversarial review, background rescue/task delegation when its app-server sandbox works | Official plugin; `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, `/codex:status`, `/codex:result`; shares local Codex auth/config; good job management | App-server task uses read-only or workspace-write sandbox; on hosts with bwrap failures this can fail before useful work; default rescue is not a durable pipeline batch contract unless the prompt supplies scope, stop conditions, and verification |
| MCP `mcp__codex__codex` | Short interactive Codex critique or small task when Claude Code exposes the MCP tool and sandbox works | Result returns in chat; can preserve thread/tool context | Long runs bloat chat; permission UI can loop; `workspace-write` can hit `bwrap: loopback: Failed RTM_NEWADDR`; do not retry the same broken route more than twice |
| Bash `codex exec` CLI fallback | Scripted batch execution, exact logging, sandbox-failure fallback | Full control over cwd, prompt file, logs, `--output-last-message`, `--json`; easiest to reproduce when preflight succeeds | `--dangerously-bypass-approvals-and-sandbox` is unsafe outside externally hardened/trusted environments; without explicit log files failures are easy to lose |
| GitHub/Codex connector or GitHub app | Read-only repository inspection when local sandbox is broken | Can still inspect remote files/PRs without local bwrap | Read-only; not a coder path; cannot replace local tests or local diff verification |

#### Selection rules

1. For integrated Claude Code review, prefer `codex-plugin-cc` if `/codex:setup` is healthy and the task is review/rescue sized. Use `--background` for long reviews and fetch with `/codex:status` / `/codex:result`.
2. For Codex-heavy coder batches on hosts with a known bwrap failure, use Bash `codex exec` with explicit log files only after the fallback is approved and preflighted. Do not spend attempts on `workspace-write` if the same host already has the `bwrap: loopback: Failed RTM_NEWADDR` memory.
3. Use MCP `mcp__codex__codex` only for short runs or when preflight proves the requested sandbox works. If MCP permission UI refuses or the sandbox fails twice, stop that route and record the failure mode.
4. Never use bypass or danger-full-access for untrusted repositories, unknown code, multi-tenant machines, secret-heavy work, or production servers.

#### Codex sandbox status

Record one of these in the design/report/state before delegating:

- `sandbox_ok`: read-only and the intended write mode passed a smoke test.
- `sandbox_broken_bwrap`: failure includes `bwrap: loopback: Failed RTM_NEWADDR` or equivalent known host memory.
- `plugin_only`: official plugin works for review/rescue but write sandbox is not proven.
- `read_only_only`: only review/read paths are available.
- `unavailable`: Codex binary/auth/plugin is missing.

Known sandbox-failure rule: if machine memory or a fresh smoke shows `bwrap: loopback: Failed RTM_NEWADDR`, do not retry `workspace-write` or read-only sandbox more than twice. Either use the trusted-host CLI bypass route with guardrails, use a read-only remote connector, or keep execution in the current model and record residual risk.

Operational shorthand: do not retry the same broken route more than twice.

#### Direct CLI known-good pattern

Use this when Codex is the coder/details writer and the chosen route is direct CLI. It is designed for reproducible logs and non-interactive pipeline evidence:

```bash
mkdir -p /tmp/pipeline-codex
codex exec \
  --cd /path/to/project \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --color never \
  --json \
  --output-last-message /tmp/pipeline-codex/<batch>-last.txt \
  < /tmp/pipeline-codex/<batch>-prompt.md \
  > /tmp/pipeline-codex/<batch>-stdout.jsonl \
  2> /tmp/pipeline-codex/<batch>-stderr.log
```

For background runs:

```bash
nohup codex exec \
  --cd /path/to/project \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --color never \
  --json \
  --output-last-message /tmp/pipeline-codex/<batch>-last.txt \
  < /tmp/pipeline-codex/<batch>-prompt.md \
  > /tmp/pipeline-codex/<batch>-stdout.jsonl \
  2> /tmp/pipeline-codex/<batch>-stderr.log &
```

Rules:

- Pass the prompt file through stdin. Do not inline long prompts.
- Use explicit stdout/stderr log files. With some Codex CLI versions, progress and TUI-like output can appear on stderr even in exec mode.
- Do not pipe through `tail`; it can hide early failures. Read saved logs after the process exits or when checking progress.
- Pair `--json` with `--output-last-message` when possible: JSONL captures progress/events, and the last-message file captures the final natural-language summary.
- If `--dangerously-bypass-approvals-and-sandbox` is used, the prompt must forbid push, rebase, force, main-branch work, secret access, privileged commands, and out-of-scope files. The current model must inspect `git diff`, run verification, and decide acceptance after every batch.

#### Failure handling

- After two materially similar failures on one route, stop that route and record known-good command, cwd, failure mode, required env/config, and chosen fallback.
- If Codex fails before invocation, do not synthesize a fake Codex answer. Report setup/auth/sandbox failure and choose another route.
- If Codex starts but returns malformed/incomplete output, use the saved `last.txt`, stdout JSONL, and stderr log as raw artifacts before editing prompts or skill text.
- If the task requires implementation and every write-capable Codex route is unsafe or broken, execute with the current model instead of bypassing guardrails silently.

### Codex CLI invocation

Use CLI after the Codex Invocation Ladder selects direct CLI. Prefer a safe sandbox only when preflight proves the sandbox works:

```bash
codex exec \
  --cd /path/to/project \
  -s workspace-write \
  --skip-git-repo-check \
  --color never \
  -o /tmp/codex-<batch>-last.txt \
  < /tmp/codex-<batch>-prompt.md \
  > /tmp/codex-<batch>-stdout.log 2>&1
```

`--dangerously-bypass-approvals-and-sandbox` is allowed only when all are true:

- trusted single-tenant execution host/project;
- user explicitly confirmed bypass;
- prompt forbids `push`, `rebase`, `force`, work on `main`, and changes outside scope;
- current model checks `git diff`, tests, and summary after every batch.

### Codex prompt contract

Every Codex prompt must include:

- role: Codex coder/details writer;
- working directory;
- exact batch/task scope;
- files that can be read/changed;
- files that cannot be changed;
- TDD rule: failing test -> implementation -> passing test;
- Test Adequacy Review requirement when tests are added or changed;
- verify commands;
- stop conditions;
- final reply contract.

Stop conditions always include:

- test already green without implementation;
- regression in existing tests;
- build/verify failure;
- Codex uncertainty about contract/invariant;
- need to edit forbidden or out-of-scope file;
- need for push, secret, privileged, or irreversible action.

Final reply contract:

- commits or changed files;
- tests run and results;
- TAR verdict and evidence that tests fail for the intended bug or missing behavior, when TAR applies;
- test count/build/bundle changes, if applicable;
- deviations from plan;
- stop condition, if any.

### Batch rule

Codex execution runs in batches of 3-5 tasks:

- setup batch may be non-TDD if it only creates config/scaffold;
- TDD batch must have tests;
- integration batch connects completed parts;
- acceptance/helper batch closes smoke/evidence.

Between batches, current model must:

1. read Codex final reply;
2. check `git diff --stat`;
3. run batch verify commands;
4. run or review Test Adequacy Review for test-changing, behavior-changing, Codex-heavy, full-autonomous, or overnight batches;
5. update state/report;
6. continue, stop, or rewrite the next prompt.

### State fields

If Codex is selected, add this to state:

```json
{
  "orchestration": {
    "spec_strategy": "current_model | cross_review | codex_details",
    "planning_strategy": "current_model | cross_review | codex_tdd_plan",
    "collaboration_profile": "solo_primary | claude_main_codex_checkpoints | dual_head_quality | codex_heavy_claude_guardrails",
    "roles": {
      "orchestrator": "current_model | claude_code | codex",
      "executor": "current_model | claude_code | codex",
      "reviewer": "current_model | claude_code | codex",
      "helpers": ["claude_code | codex"]
    },
    "cross_check_initial": false,
    "premortem_plan_review": "auto | forced | skipped",
    "autonomy": "interactive | guided_autonomous | full_autonomous | overnight",
    "executor": "current_model | codex",
    "batches": [
      {
        "id": "B1",
        "status": "pending | in_progress | completed | stopped | failed",
        "tasks": ["T01", "T02"],
        "summary_file": "/tmp/codex-B1-last.txt",
        "verify": "<command/result summary>",
        "commits": []
      }
    ]
  }
}
```

### Where Used

- `pipeline-deep/SKILL.md`: Phase 4, Phase 5, Phase 6.
- `pipeline-hard/SKILL.md`: Phase 5, Phase 6, Phase 7.

## Optional Plugin: /codex:adversarial-review

(Moved verbatim from the deep/hard SKILL.md appendix, dedup 2026-06-09.)

Не часть основного flow. Упомянут здесь чтобы не забыть.

**Когда использовать:** если хочется фонового Codex-ревью без итераций параллельно с основной работой.

**Установка (одноразово):**
```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/codex:setup
```

**Использование:**
```bash
/codex:adversarial-review --base main --background  # запустить в фоне
/codex:status                                        # проверить
/codex:result                                        # забрать
```

> **Не включать** `/codex:setup --enable-review-gate` — может создать долгий Claude↔Codex цикл и быстро исчерпать лимиты.

**Отношение к pipeline-у:** это НЕ заменяет Cross-Agent Review из Review Menu, а дополняет. На типичной задаче использовать не нужно — Cross-Agent Review покрывает тот же вопрос с итерациями. Плагин `/codex:adversarial-review` специфичен для Codex-as-reviewer (Claude → Codex направление); в Codex-side review (Codex → Claude) он не применяется.
