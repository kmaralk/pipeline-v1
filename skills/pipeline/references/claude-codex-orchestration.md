# Claude → Codex Orchestration

> **Status:** reference note, generalized from an internal orchestration run. Рабочие правила интегрированы в `shared.md` как `Codex-Orchestrated Planning and Execution`; `pipeline-deep` и `pipeline-hard` ссылаются на этот shared-блок в spec/planning/execution фазах.

## Когда использовать

Этот режим — для **pipeline-deep** и **pipeline-hard** при условиях:
- Claude Code session работает на низких лимитах токенов (или пользователь явно просит экономить).
- Задача — multi-step implementation (10+ task'ов TDD-стиля).
- Codex CLI / MCP доступны, проект помечен trusted в `~/.codex/config.toml`.
- Пользователь явно одобрил автономный режим (см. `feedback_autonomous_codex_orchestration.md`).

**Не использовать** если:
- Простая задача в 2-3 шага (overhead orchestration больше пользы).
- Untrusted, shared, or unavailable execution host.
- Codex sandbox runtime не подтверждён рабочим (тестируй коротким read-pass перед делегированием).

## Pattern overview

Claude = **orchestrator**. Codex = **coder**.

Разделение:

| Артефакт | Кто пишет | Кто ревьюит |
|---|---|---|
| Thin spec (goal + invariants + contracts + acceptance) | **Claude** | Codex (read-only) |
| Implementation details (TDD test list, edge cases, code skeletons, scripts) | **Codex** (Variant C) | Claude (review pass) |
| Implementation plan (writing-plans skill format, 5-step TDD bites) | **Codex** | Claude (skim review) |
| Production code + tests + commits | **Codex** (Phase 6 batches) | Claude (между batch'ами) |
| Orchestrator decisions (Q ratification, R findings) | **Claude** | User (опционально) |

Claude фокусируется на: invariants, scope guarding, decision making, stop-condition handling. Codex фокусируется на: чтение кода, генерация структурированного output, exact code, TDD discipline.

## Phase mapping

В pipeline-deep / pipeline-hard:

- **Phase 4 (Spec):** Variant C — Claude thin spec (~150-300 строк) → Codex дополнения (`<topic>-codex-details.md`, ~400-700 строк) → Claude review pass + ratified decisions section в spec.
- **Phase 5 (Plan):** Codex генерирует TDD-формат plan (`<date>-<topic>-plan.md`, 700-1000 строк, 15-25 task'ов).
- **Phase 6 (Execute):** Codex выполняет plan по **batch'ам** (3-5 task'ов на batch); Claude review между batch'ами (verify gates + scope check).

## Codex invocation policy

Canonical policy now lives in `skills/pipeline/references/orchestration.md` §Codex Invocation Ladder. This legacy note remains as a compact portable reminder from the original internal run.

Route summary:

- `codex-plugin-cc`: official Claude Code plugin for one-shot review, adversarial review, background rescue, status, result, and cancel. It is the best integrated route when its app-server sandbox works.
- MCP `mcp__codex__codex`: useful for short Codex critique or small tasks when the requested sandbox is proven healthy. On some hosts, workspace-write/read-only can hit `bwrap: loopback: Failed RTM_NEWADDR`.
- Direct `codex exec` CLI: useful for Codex-heavy coder batches when sandbox preflight proves safe or a host-specific sandbox failure has an explicitly approved fallback, because it gives exact cwd, prompt file, stdout/stderr logs, `--json`, and `--output-last-message`.

Before choosing a route, record Codex sandbox status: `sandbox_ok`, `sandbox_broken_bwrap`, `plugin_only`, `read_only_only`, or `unavailable`. If the same route fails twice with the same bwrap/permission mode, stop that route and record the fallback.

Before launching Codex, read `skills/pipeline/references/orchestration.md` §Codex Invocation Ladder and the selected route's command template. Do not invoke Codex from memory, stale chat snippets, or an unverified command pattern. Record the exact route, command shape, cwd, prompt path, logs, and watchdog cadence before launch.

## Codex invocation (CLI fallback on bwrap sandbox failure)

**Почему CLI fallback:** on some Linux hosts, `mcp__codex__codex` / app-server sandbox can fail with a bwrap loopback error. A direct Bash CLI fallback may work, but bypass mode is allowed only for a trusted single-tenant machine and trusted project with explicit user approval.

**Шаблон команды:**

```bash
codex exec \
  --cd /path/to/project \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  -m <model> \
  --color never \
  --json \
  --output-last-message /tmp/codex-<batch>-last.txt \
  < /tmp/codex-<batch>-prompt.md \
  > /tmp/codex-<batch>-stdout.jsonl \
  2> /tmp/codex-<batch>-stderr.log
```

Объяснение флагов:
- `--cd <project>` — обязательно, иначе Codex наследует cwd Claude Code.
- `--dangerously-bypass-approvals-and-sandbox` — обходной режим для подтверждённого sandbox failure. Для trusted host/project приемлемо только при явном approval. См. caveat ниже.
- `--skip-git-repo-check` — не падать если запуск не в git-корне (бывает в monorepo).
- `-m <model>` — use the current supported model for the local Codex installation, or omit the flag to use the configured default.
- `--color never` — чистый stdout без ANSI escapes (упрощает парсинг).
- `--json` — progress/events as JSONL for post-mortem analysis.
- `--output-last-message /tmp/.../last.txt` — финальный message Codex'а в отдельный файл (только summary, не весь лог). Идеально для парсинга в Claude.
- `< prompt.md` — prompt через stdin (markdown с инструкциями). Не используй inline `"<heredoc>"`, prompt бывает > 4 KB.
- `> stdout.jsonl 2> stderr.log` — explicit stdout/stderr log files for post-mortem отладки.

**Запуск в фоне:** use background Bash/nohup with explicit log files. Do not pipe through `tail`; it can lose early failures. `timeout` 600000-1200000 ms (10-20 минут) хватает на 4-5 task'ов.

### Codex Progress Watchdog

After launching async/background Codex, follow `autonomy-safeguards.md` §Codex Progress Watchdog. Check status/result/logs within 1 minute to confirm Codex actually started, then use the expected-duration cadence: check every 5 minutes for runs up to 20 minutes, check every 10 minutes for runs from 20 minutes to 2 hours, and check every 20 minutes for longer or overnight runs unless a stricter cap applies. If Codex failed before useful work, is blocked, waiting for input, or stuck with no useful progress, stop waiting and make an orchestrator decision before relaunching or changing route.

### Caveat про `--dangerously-bypass-approvals-and-sandbox`

Этот флаг **отключает Codex sandbox целиком** — Codex может писать в любую директорию, запускать любые shell команды, делать git commits.

Безопасно если:
- Execution host is trusted and single-tenant.
- Проект помечен `trust_level = "trusted"` в `~/.codex/config.toml`.
- Каждый prompt явно прописывает: «не push, не rebase, не force-commit, не модифицируй файлы вне scope X».

Небезопасно если:
- Multi-tenant машина.
- Чужой / непроверенный код в проекте.
- Codex prompt не содержит явных stop-conditions.

Альтернатива (если bwrap починен): `-s workspace-write` без bypass-флага.

## Prompt structure (Codex coder)

Каждый Codex prompt должен содержать:

```markdown
Ты — Codex coder в Phase 6 ... [твоя роль].

**Working directory:** `/path` (передан через --cd).

**Задача:** [batch X = Tasks N1, N2, ...] из плана `<plan-file>`.

**Перед запуском прочти:**
1. <plan-file> — конкретные секции.
2. <support-files> — что нужно для context.

**Tasks summary:**
- Task N1: [короткое описание + scope].
- Task N2: ...

**Выполнение:**
- TDD цикл per task: failing test → verify fail → impl → verify pass → commit.
- Используй exact code из плана и Shared Snippets.
- Один commit per task с conventional message из плана.

**Verify gates:**
- After Step 4: целевой тест pass; общий test count не упал.
- After Task N: build green, bundle ≤ <limit>.

**Stop conditions (escalate, не commit):**
- Failing test pass'ится без impl.
- Existing test регрессирует.
- Build падает.
- Bundle превышает <limit>.
- [специфичные для batch].

**После всех task'ей:**
- `git log --oneline -10` (новые commit'ы).
- Verify command output.
- Bundle/build snapshot.

**Финальный reply:**
- Commits (hash + subject).
- Test count delta.
- Bundle delta.
- Failed tests (если есть, с пометкой ожидаемое/нет).
- Любые отклонения.

**НЕ делай:** push, rebase, force-commit, изменения вне scope.
**НЕ модифицируй** [конкретные файлы которые out-of-scope].
```

Ключевые принципы prompt'а:
1. **Явный scope** — какие файлы трогать, какие не трогать.
2. **Verify gates** — что должно зеленеть после каждого шага.
3. **Stop conditions** — когда escalate, **не** делать workaround.
4. **Финальный reply контракт** — что Codex должен отчитать (commits + metrics).
5. **Negative scope ("НЕ ...")** — повторяй с emphasis. Codex иногда дрейфует в соседние файлы.

## Batch strategy (Phase 6 execution)

Группируй tasks из плана в batch'и **3-5 task'ов** по логическим границам:

- **Setup batch** (Tasks 01-03): config, fonts, tokens — без TDD.
- **TDD batches** (Tasks 04-N): по компоненту/feature, 4-5 task'ов на batch.
- **Integration batch**: подключение всего собранного в production code path (route activation, провайдеры).
- **Test/helper batches**: utility, regression, acceptance gate.

Между batch'ами Claude **обязательно**:
1. Читает финальный summary Codex'а.
2. Проверяет: commits созданы, tests passed, bundle в budget'е.
3. Если ОК — обновляет state.json (textual surgical) с batch result, commit, и делает следующий prompt.
4. Если не ОК — escalate (см. ниже).

**Размер batch'а** = баланс между Codex stamina (~5-10 минут на batch до фарм-out) и orchestrator overhead. 4 task'и обычно идеал.

## Stop conditions handling

Когда Codex эскалирует stop-condition:

1. **Прочитай** финальный reply Codex'а — он явно описывает блокер.
2. **Не пытайся** обойти автоматически — Codex был conservative потому что есть реальная неопределённость.
3. **Сделай orchestrator decision**: либо relax invariant (с обоснованием в state.json), либо переформулируй prompt для Codex с явным указанием как продолжить.
4. **Resume Codex** новым `codex exec` (или MCP `codex-reply` — но через CLI каждый запуск stateless, проще новый run).

Example: Codex stopped because a requested CI workflow file did not exist, while the invariant forbade workflow changes. The orchestrator chose the safe skip-CI option, recorded the rationale, and resumed Codex with an explicit prompt.

## Claude orchestrator decisions

Между batch'ами Claude принимает решения:

- **Q-ratification** (decisions из codex-details Open Questions). Каждый Q имеет 2-4 опции. Claude выбирает опцию + обоснование + фиксирует в spec'е секции «Ratified decisions».
- **R-findings** (Claude review fixes к Codex output). Identify баги/неточности в Codex deliverable, добавь fixes в spec.
- **Scope policing** — если Codex написал лишнего (out-of-scope changes), revert через git.
- **Batch boundary** — следующий batch или escalate to user (если что-то пошло не туда).

Принцип: **trust but verify**. Codex обычно даёт sensible output, но Claude проверяет ключевые метрики каждый batch. Полный rerun только при serious deviation.

## Verify gates per batch (typical)

```bash
# Test count check (frontend example)
cd frontend && npm test -- --run 2>&1 | tail -5
# Expected: N passed (N+ от прошлого batch'а), 0 failed (исключения зафиксированы заранее)

# Build check
cd frontend && npm run build 2>&1 | tail -10
# Expected: built successfully, no warnings

# Bundle budget check
cd frontend && bash scripts/check-bundle-budget.sh
# Expected: bundle-budget: ok main=NN.NNkB limit=132kB precache=NNNKiB limit=862KiB

# Backend regression (если изменения могут косвенно повлиять)
cd backend && source .venv/bin/activate && python -m pytest -q 2>&1 | tail -3
# Expected: 131+ passed
```

Vitest-специфика: используй `--run` (single-run mode, не watch). `--reporter=basic` не работает в vitest 4.1+ — оставь default.

## Optional local memory patterns

If the agent platform supports local memory, store only portable lessons such as:

- user authorization expectations for autonomous mode;
- the current Claude/Codex orchestration pattern;
- host-specific sandbox failure notes;
- state-file update practices that avoid noisy rewrites.

These notes are optional runtime memory, not bundled package dependencies.

## Anti-patterns

1. **Не делегируй Codex'у high-stakes решения** — выбор архитектуры, относительная важность invariants, trade-offs. Это работа orchestrator'а.
2. **Не делай batch'ы > 6 task'ов** — Codex теряет фокус, output деградирует.
3. **Не пропускай verify gates** — даже если предыдущий batch прошёл чисто.
4. **Не объединяй commits** в один — TDD один commit per task сохраняет git bisect.
5. **Не давай Codex'у `--dangerously-bypass-approvals-and-sandbox`** на untrusted кода.
6. **Не давай Codex'у писать на ветку main** напрямую. Только feature branch.
7. **Не используй `mcp__codex__codex` если sandbox runtime сломан** — переключайся на CLI с bypass-флагом сразу.
8. **Не игнорируй Codex Stop conditions** — он эскалирует не зря, обычно есть реальная неоднозначность.

## Метрики качества (как понять что pattern работает)

A healthy orchestration run should show:
- small implementation batches with reviewable commits;
- no regressions in the relevant test suites;
- unchanged scope boundaries unless the orchestrator records an explicit decision;
- stop conditions handled through recorded orchestrator decisions, not silent bypasses.

Целевой ratio: **80% работы делает Codex**, Claude orchestrator съедает 20% (decisions + verify + state).

## Цикл улучшений

После каждого pipeline run:
1. Зафиксировать deviations в state.json.
2. Если pattern сломался / deviations много — обновить эту страницу.
3. Если pattern сработал — добавить новые memory feedback с уточнениями.
4. Пересобрать pipeline skill (после нескольких подтверждённых runs).

---

**Integration status:**

- [x] Pattern перенесён в `shared.md` как `Codex-Orchestrated Planning and Execution`.
- [x] В spec phase добавлен выбор: обычный spec / cross-review / thin spec + Codex details.
- [x] В planning phase добавлен выбор: обычный plan / cross-review / Codex TDD plan.
- [x] В execution phase добавлен выбор автономности: interactive / guided autonomous / full autonomous.
- [x] Кодифицирован batch size 3-5 task'ов и per-batch verification.
- [x] Не добавлено как practice: это execution strategy, а не domain-risk checklist.
