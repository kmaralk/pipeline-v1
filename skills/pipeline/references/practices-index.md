# Practices Index

Лёгкий индекс для Phase 1.5 (Context-Driven Practices). Содержит только триггеры и якоря. Полные определения практик (Summary / Prerequisites / Add to Phase 4 / Add to Phase 6 / Add to Phase 7 / примеры) — в `practices-full.md`, читаются точечно по якорю только для активированных практик.

## Как этим пользоваться

Phase 1.5 каждого режима делает:

1. Читает этот файл (~100 строк).
2. Для каждой строки таблицы — проверяет триггеры:
   - **Step A (exact, 0 tokens):** `keywords` ∈ brief ИЛИ `paths` ∈ context files.
   - **Step B (semantic, small AI call):** если Step A не сработал — короткая AI-проверка против `semantic`.
3. Активировавшиеся practices — открывает `practices-full.md#<anchor>` и читает только их блоки.
4. Применяет strictness по режиму:
   - `lite` → recommend (default OFF, пользователь явно выбирает)
   - `deep` → auto-on (пользователь может убрать через `-N`)
   - `hard` → mandatory (пропуск — только через deferred-decisions с обоснованием)

This index is a routing aid, not an exhaustive risk model. If the task exposes a real risk that is not in the table, record an ad-hoc risk in the spec/report with owner, evidence, and verification, or propose a new practice later; do not pretend the risk is absent because no row matched.

## Conditional practices (16)

| id | keywords (subset) | paths (globs) | semantic trigger | prereq | anchor |
|----|-------------------|---------------|------------------|--------|--------|
| threat-model | auth, login, password, token, admin, upload, payment, pii, oauth | `**/auth/**`, `**/admin/**`, `**/upload*`, `**/payment*`, `**/login*`, `**/security/**` | Добавляется/меняется точка входа с доступом к данным/привилегиям; обработка файлов, платежей, PII | none | `#threat-model` |
| idempotency | webhook, retry, payment, charge, refund, send email, submit, process, dedupe | `**/webhooks/**`, `**/payments/**`, `**/orders/**`, `**/tasks/**`, `**/queues/**`, `**/workers/**` | Обработчик может быть вызван повторно (webhook/очередь/ретрай), побочный эффект не должен дублироваться | none | `#idempotency` |
| expand-contract-migrations | migration, alembic, schema, add column, drop column, rename, index, backfill | `**/migrations/**`, `**/alembic/**`, `**/schema.prisma`, `**/*.sql` | Добавляются/переименовываются/удаляются колонки/таблицы/индексы в работающей БД с трафиком | running service + DB | `#expand-contract-migrations` |
| slo-perf-budget | endpoint, api, latency, p95, p99, slo, sla, availability, throughput, hot path | `**/handlers/**`, `**/routes/**`, `**/api/**`, `**/controllers/**` | Добавляется/меняется публичная ручка, критичный путь пользователя или горячий участок кода | none | `#slo-perf-budget` |
| feature-flags | feature flag, toggle, rollout, gradual, beta, experiment, a/b, launchdarkly, unleash | `**/flags/**`, `**/features/**` | User-visible поведение, которое в случае проблем хочется быстро отключить без redeploy | none | `#feature-flags` |
| resilience-checklist | external api, http client, requests, aiohttp, axios, grpc, webhook, messaging api, openai, claude api | `**/clients/**`, `**/integrations/**`, `**/adapters/**` | Вызов внешнего сервиса/API/LLM по сети, которым мы не управляем | none | `#resilience-checklist` |
| observability-concrete | new service, new endpoint, new handler, new worker, new job, background task, cron, new feature | `**/handlers/**`, `**/routes/**`, `**/workers/**`, `**/services/**`, `**/tasks/**` | Создаётся новый сервис, endpoint, фоновая задача или значимая точка бизнес-логики | none | `#observability-concrete` |
| runbook-ownership | new service, new system, new daemon, new bot, new userbot, microservice, systemd, deploy | `**/systemd/**`, `**/deploy/**`, `**/new-service/**`, root-level new dirs | Создаётся новый долгоживущий исполняемый компонент (сервис, демон, бот) | none | `#runbook-ownership` |
| custom-lint-rules | architecture, boundary, layering, clean architecture, hexagonal, dependency rule, cycle | `**/pyproject.toml`, `**/.eslintrc*`, `**/semgrep*`, `**/ruff.toml` | Проект имеет несколько слоёв/модулей с важными импорт-границами | >1 module with boundaries | `#custom-lint-rules` |
| canary-rollout | canary, gradual rollout, progressive, staged rollout, blue-green, deploy, release to prod | `**/deploy/**`, `**/k8s/**`, `**/.github/workflows/deploy*` | Прод-релиз user-visible изменения с большой аудиторией | % routing infra | `#canary-rollout` |
| load-testing | load test, stress test, benchmark, k6, locust, jmeter, rps, concurrency, hot path | `**/loadtest/**`, `**/benchmarks/**`, `**/perf/**` | Меняется горячий участок или ожидается рост нагрузки / пиковое событие | staging близкий к проду | `#load-testing` |
| dast-scan | public api, web app, public endpoint, external, production-facing, open to internet | `**/api/**` (если публичный), `**/web/**`, `**/frontend/**` | Меняется поверхность, доступная из публичного интернета | staging production-like | `#dast-scan` |
| mutation-testing | mutation test, mutmut, stryker, test quality, coverage, critical module | `**/tests/**` (при 100+ тестах) | Модуль бизнес-критичен (деньги/безопасность/данные), есть зрелый тест-набор | module has >100 tests | `#mutation-testing` |
| eval-driven-ai | prompt, system message, llm, gpt, claude, gemini, openai, anthropic, agent, skill, model, embedding, rag | `**/prompts/**`, `**/*.prompt.md`, `**/agents/**`, `**/skills/**/SKILL.md`, `**/llm/**`, `**/ai/**` | Меняется промпт, модель, параметры LLM или AI-логика, отвечающая пользователю | `evals/golden_dataset.jsonl` ≥20 примеров | `#eval-driven-ai` |
| user-journey-acceptance | frontend, ui, ux, page, component, react, vue, svelte, browser, playwright, form, button, modal, screen | `**/frontend/**`, `**/web/**`, `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/components/**`, `**/pages/**`, `**/app/**` | Меняется пользовательский интерфейс или пользовательский путь, который нужно проверить как реальное действие пользователя | runnable app or documented manual route | `#user-journey-acceptance` |
| business-invariants-db | balance, amount, price, status, state, counter, quota, limit, transaction, order, payment, credit, debit, inventory, stock | `**/models/**`, `**/entities/**`, `**/migrations/**`, `**/schema.prisma` | Добавляется/меняется поле/таблица с финансовой величиной, счётчиком, статусом из enum или временным отношением | none | `#business-invariants-db` |

## Baseline reference (always-on — НЕ conditional)

Эти 5 практик жёстко встроены в SKILL.md каждого режима и запускаются всегда. Здесь — для полноты картины, активации через Phase 1.5 не требуется.

| # | Practice | Enforced in |
|---|----------|-------------|
| B1 | Secret scanning (gitleaks) | Phase 0 (Baseline Gates, см. `shared.md §Baseline Gates`) |
| B2 | Lockfiles integrity check | Phase 0 (Baseline Gates, см. `shared.md §Baseline Gates`) |
| B3 | CVE scan of dependencies | Verify phase (lite:4, deep:7, hard:8 — см. `shared.md §CVE Scan`) |
| B4 | Input validation checklist in spec | Spec phase (lite:2, deep:4, hard:5 — см. `shared.md §Input Validation Checklist`) |
| B5 | Regression test mandatory for `bugfix` class | Execute phase (в TDD-цикле каждого режима) |
