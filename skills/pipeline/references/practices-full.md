# Practices Full Definitions

Полные тексты 16 conditional-практик для Phase 1.5 (совпадает с practices-index.md). Индекс с триггерами и якорями — в `practices-index.md`. Читать отсюда нужно **точечно** (якорь конкретной активированной practice), не целиком.

Baseline-практики B1-B5 (hardcoded в SKILL.md каждого режима) — не здесь; их определения см. `shared.md §Baseline Gates` / `§CVE Scan` / `§Input Validation Checklist`.

Each practice block is a starting kit, not a closed checklist. Fill the baseline fields, then add task-specific fields, tests, evidence, or rollout notes when the actual risk needs them; do not add unrelated ceremony just because an example appears here.

---

## threat-model

**Summary:** Mini-таблица `asset → threat → mitigation → test` перед написанием фичи с security-поверхностью. Проактивный поиск уязвимостей в дизайне, а не после скана в конце.

**Triggers:**
- keywords: `auth`, `login`, `register`, `signup`, `password`, `token`, `jwt`, `session`, `admin`, `permissions`, `rbac`, `upload`, `file upload`, `payment`, `billing`, `checkout`, `pii`, `personal data`, `email verify`, `reset password`, `oauth`, `api key`
- paths: `**/auth/**`, `**/admin/**`, `**/upload*`, `**/payment*`, `**/billing*`, `**/login*`, `**/register*`, `**/security/**`
- semantic: "задача добавляет или меняет точку входа, через которую пользователь может получить доступ к данным, ресурсам или привилегиям; также любая обработка файлов, платежей, PII"

**Add to Phase 4 (spec):** секция `## Threat Model`:

```md
## Threat Model

| Ценность (asset) | Угроза (threat) | Защита (mitigation) | Тест |
|------------------|-----------------|---------------------|------|
| <что ценного под угрозой> | <конкретный класс атаки> | <технический контроль> | <как проверяем, что защита работает> |
```

Заполнить минимум 3 строки. Классы атак для подсказки: injection, broken auth, sensitive data exposure, XXE, broken access control, security misconfig, XSS, insecure deserialization, components with known vulns, insufficient logging.

**Add to Phase 6 (execute):** для каждой строки таблицы — реальный тест перед фиксом. Защита должна быть в коде, не в комментарии.

**Add to Phase 7 (verify):** все тесты из колонки «Тест» проходят. Если включён DAST (см. отдельную practice) — прогнать на новый endpoint.

**Applies (examples):**
- «добавь регистрацию через email»
- «сделай загрузку аватара»
- «прикрути оплату через Stripe»
- «добавь админ-панель модерации отзывов»

**Does NOT apply (examples):**
- «поправь текст кнопки»
- «ускори рендер карточки»
- «обнови CLAUDE.md»

---

## idempotency

**Summary:** Защита от двойных нажатий/ретраев — повторный одинаковый запрос не создаёт дубль операции. Критично для денег, заказов, рассылок, webhook'ов.

**Triggers:**
- keywords: `webhook`, `retry`, `idempotent`, `idempotency`, `payment`, `charge`, `refund`, `send email`, `send notification`, `create order`, `submit`, `process`, `dedupe`, `at-least-once`
- paths: `**/webhooks/**`, `**/payments/**`, `**/orders/**`, `**/tasks/**`, `**/queues/**`, `**/workers/**`
- semantic: "задача создаёт обработчик, который может быть вызван повторно (webhook, очередь, ретрай API-клиента) и побочный эффект не должен дублироваться"

**Add to Phase 4 (spec):** секция `## Idempotency Plan`:

```md
## Idempotency Plan
- **Точки мутации:** <список эндпоинтов/обработчиков, создающих побочные эффекты>
- **Источник ключа:** <X-Idempotency-Key header / webhook.id / task.id / натуральный ключ>
- **Хранилище ключей:** <Redis TTL / БД таблица / хеш>
- **TTL окна дедупликации:** <X часов — обосновать>
- **Поведение при collision:** <вернуть первый результат / ошибка 409 / ...>
```

**Add to Phase 6 (execute):** перед реализацией побочного эффекта — `if key in seen: return cached_result`.

**Add to Phase 7 (verify):** integration-тест «дважды один запрос → один побочный эффект + одинаковый ответ».

**Applies:**
- «сделай webhook от Stripe»
- «реализуй /checkout endpoint»
- «добавь фоновую задачу рассылки писем»

**Does NOT apply:**
- «почини pagination на /posts»
- «обнови лейаут профиля»

---

## expand-contract-migrations

**Summary:** Миграции БД без даунтайма — меняем схему по шагам: add → dual-write → backfill → switch reads → cleanup. Плюс обязательный down-скрипт.

**Triggers:**
- keywords: `migration`, `alembic`, `schema`, `add column`, `drop column`, `rename`, `index`, `backfill`, `alter table`
- paths: `**/migrations/**`, `**/alembic/**`, `**/schema.prisma`, `**/*.sql`
- semantic: "задача добавляет, переименовывает или удаляет колонки/таблицы/индексы в уже работающей БД с трафиком"

**Prerequisites:** существует запущенный сервис с БД (не свежий проект).

**Add to Phase 4 (spec):** секция `## Migration Plan (expand/contract)`:

```md
## Migration Plan (expand/contract)

| Шаг | Действие | Когда деплоится | Можно откатить? |
|-----|----------|-----------------|------------------|
| 1 | ADD nullable колонку / новая таблица | Релиз N | Да (drop) |
| 2 | Dual-write: писать в старое И новое | Релиз N+1 | Да (убрать код) |
| 3 | Backfill данных скриптом | Между N+1 и N+2 | Да (данные сохранены в старом) |
| 4 | Switch reads на новое | Релиз N+2 | Да (вернуть чтение со старого) |
| 5 | DROP старого | Релиз N+3 (после стабильности) | Нет — точка невозврата |

## Rollback Plan
<down-скрипт для каждого шага 1-4>
```

**Add to Phase 7 (verify):** миграция применяется и откатывается на копии прод-БД (даже малый dump). Reads/writes сервиса работают на каждом шаге.

**Applies:**
- «добавь колонку is_premium в users»
- «переименуй таблицу reviews → feedback»
- «сделай индекс на created_at»

**Does NOT apply:**
- первый релиз проекта без пользователей
- миграция в dev-БД без прод-копии

---

## slo-perf-budget

**Summary:** Цели производительности в цифрах: p95 latency, error rate, availability. Плюс performance budget, который CI валит при регрессии.

**Triggers:**
- keywords: `endpoint`, `api`, `latency`, `performance`, `p95`, `p99`, `slo`, `sla`, `availability`, `throughput`, `rps`, `response time`, `hot path`
- paths: `**/handlers/**`, `**/routes/**`, `**/api/**`, `**/controllers/**`
- semantic: "задача добавляет или меняет публичную ручку, критичный путь пользователя, или горячий участок кода"

**Add to Phase 4 (spec):** секция `## SLO & Performance Budget`:

```md
## SLO & Performance Budget
- **Availability:** <99.9% / 99.5%>
- **p95 latency:** <X ms>
- **p99 latency:** <Y ms>
- **Error rate:** <≤ 0.1%>
- **Budget CI check:** <команда/скрипт, валящий сборку при p95 > X>
- **Baseline (до изменения):** <текущие цифры или "не измерено">
```

**Add to Phase 7 (verify):** измерить реальный p95 на staging. Если > бюджета — блок merge или явное `residual risk`.

**Applies:**
- «добавь endpoint /search с фильтрами»
- «оптимизируй рендер главной страницы»

**Does NOT apply:**
- внутренняя CLI-утилита для админа
- задачи на рефакторинг без пути пользователя

---

## feature-flags

**Summary:** User-visible фича выкатывается за флагом. Выключить — секунды, без redeploy.

**Triggers:**
- keywords: `feature flag`, `toggle`, `rollout`, `gradual`, `beta`, `experiment`, `a/b`, `launchdarkly`, `unleash`, `flipt`
- paths: `**/flags/**`, `**/features/**`
- semantic: "задача добавляет или меняет user-visible поведение, которое в случае проблем хочется быстро отключить без redeploy"

**Add to Phase 4 (spec):** секция `## Feature Flag`:

```md
## Feature Flag
- **Имя флага:** `<feature_snake_case>`
- **Owner:** <человек/агент, отвечающий>
- **Target audience:** <all / beta users / specific cohort>
- **Default state at release:** <off / on 1% / on 10%>
- **Kill-switch criteria:** <какая метрика/сигнал триггерит выключение>
- **Expiry date:** <YYYY-MM-DD — когда флаг удаляется>
- **Metric for success:** <что измеряет успех включения>
```

**Add to Phase 6 (execute):** код фичи обёрнут в `if flag.enabled(name): ...`. Старое поведение сохранено как fallback.

**Add to Phase 7 (verify):** тест с флагом off (старое поведение) + тест с флагом on (новое).

**Applies:**
- «добавь кнопку экспорта отзывов в PDF»
- «переключи алгоритм рекомендаций»

**Does NOT apply:**
- багфикс без изменения UX
- рефакторинг без user-visible эффекта

---

## resilience-checklist

**Summary:** Для каждого внешнего вызова — явные timeout, bounded retries, circuit breaker, fallback. Один упавший external API не должен валить весь сервис.

**Triggers:**
- keywords: `external api`, `http client`, `requests`, `aiohttp`, `axios`, `grpc`, `webhook`, `messaging api`, `openai`, `claude api`, `third-party`, `integration`
- paths: `**/clients/**`, `**/integrations/**`, `**/adapters/**`
- semantic: "задача вызывает внешний сервис/API/LLM по сети, которым мы не управляем"

**Add to Phase 4 (spec):** секция `## Resilience`:

```md
## Resilience (per external call)

| Вызов | Timeout | Retries | Backoff | Circuit breaker | Fallback |
|-------|---------|---------|---------|-----------------|----------|
| <API name> | <connect/read sec> | <N, only idempotent> | <exp+jitter> | <threshold 5xx/5min> | <cached / default / 503> |
```

**Add to Phase 6 (execute):** обёртки из стандартной либы (tenacity/retry, circuit breaker). Метрика `dependency_failure_rate` по каждому внешнему имени.

**Add to Phase 7 (verify):** тест с замоканным timeout на внешнем вызове → сервис возвращает fallback, не зависает.

**Applies:**
- «вызов OpenAI для генерации»
- «интеграция с messaging platform API»
- «запрос к YouTube Data API»

**Does NOT apply:**
- чисто локальная обработка данных
- запрос к собственной БД (обрабатывается в другом паттерне)

---

## observability-concrete

**Summary:** Конкретная реализация observability (структурные JSON-логи + correlation_id + доменные метрики + span-имена), а не абстрактный «observability plan».

**Triggers:**
- keywords: `new service`, `new endpoint`, `new handler`, `new worker`, `new job`, `background task`, `cron`, `new feature`
- paths: `**/handlers/**`, `**/routes/**`, `**/workers/**`, `**/services/**`, `**/tasks/**`
- semantic: "задача создаёт новый сервис, endpoint, фоновую задачу или значимую точку бизнес-логики"

**Add to Phase 4 (spec):** секция `## Observability`:

```md
## Observability
- **Correlation ID:** <заголовок/поле; как пробрасывается через весь стек>
- **Log fields (JSON):** timestamp, level, service, trace_id, user_id?, domain-fields: <список>
- **Domain metrics:** <counter/histogram/gauge с именем и лейблами>
- **OTel spans:** <имена span'ов на границах: `<module>.<operation>`>
- **Dashboards:** <где смотрит оператор при инциденте>
```

**Add to Phase 7 (verify):** локальный прогон сценария → логи содержат все поля, trace_id виден сквозь все шаги, метрики отдаются на /metrics.

**Applies:**
- «создай сервис управления скидками»
- «добавь endpoint /reviews/summary»

**Does NOT apply:**
- изменение текста сообщения
- замена алгоритма внутри функции без новой операции

---

## runbook-ownership

**Summary:** Каждый новый сервис/компонент имеет владельца и runbook «что делать при инциденте».

**Triggers:**
- keywords: `new service`, `new system`, `new daemon`, `new bot`, `new userbot`, `microservice`, `systemd`, `deploy`
- paths: `**/systemd/**`, `**/deploy/**`, `**/new-service/**`, root-level new dirs
- semantic: "задача создаёт новый долгоживущий исполняемый компонент (сервис, демон, бот), а не доработку существующего"

**Add to Phase 8 (report) — deep/hard only:** файлы `OWNERS` и `RUNBOOK.md` в каталоге сервиса:

```md
## RUNBOOK.md (шаблон)

### Symptoms → Action

| Симптом | Где увидеть | Что делать | Когда эскалировать |
|---------|-------------|------------|--------------------|
| Сервис не отвечает | <health check URL / log line> | `systemctl restart <name>` | После 2 рестартов |
| Высокий error rate | <dashboard> | <runbook link> | >5% 10 мин |
| ... | ... | ... | ... |

### Контакты
- Owner: <name>
- Backup: <name>
- Escalation: <channel>
```

**Applies:**
- «создай новый userbot для канала X»
- «запусти сервис ингеста отзывов»

**Does NOT apply:**
- добавить команду в существующий бот
- изменить текст логов

---

## custom-lint-rules

**Summary:** Компьютер автоматически проверяет архитектурные правила («из папки X нельзя импортить из папки Y»), чтобы архитектура не деградировала.

**Triggers:**
- keywords: `architecture`, `boundary`, `layering`, `clean architecture`, `hexagonal`, `dependency rule`, `cycle`
- paths: `**/pyproject.toml`, `**/.eslintrc*`, `**/semgrep*`, `**/ruff.toml`
- semantic: "проект имеет несколько слоёв/модулей, между которыми важно запрещать определённые импорты или паттерны"

**Prerequisites:** проект уже имеет структуру из >1 модуля с осмысленными границами.

**Add to Phase 4 (spec):** секция `## Architectural Guards`:

```md
## Architectural Guards
- **Правило 1:** <например, "из app/ui нельзя импортить из app/db">
  - Реализация: <semgrep rule / import-linter / eslint-plugin-boundaries>
- **Правило 2:** ...
```

**Add to Phase 7 (verify):** линтер прогнан в CI, нарушения = build fail.

**Applies:**
- зрелые проекты с выраженными слоями
- когда ревью повторно ловит одно и то же нарушение

**Does NOT apply:**
- монолит из одного файла
- задачи, не меняющие структуру

---

## canary-rollout

**Summary:** Поэтапный выкат: 1% → 10% → 50% → 100% с авто-откатом при нарушении SLO.

**Triggers:**
- keywords: `canary`, `gradual rollout`, `progressive`, `staged rollout`, `blue-green`, `deploy`, `release to prod`
- paths: `**/deploy/**`, `**/k8s/**`, `**/.github/workflows/deploy*`
- semantic: "задача включает прод-релиз user-visible изменения с достаточной аудиторией, чтобы плохой релиз навредил многим"

**Prerequisites:** инфра поддерживает процентный роутинг (service mesh, load balancer с весами, feature flags с rollout %).

**Add to Phase 4 (spec):** секция `## Rollout Plan`:

```md
## Rollout Plan
| Этап | % трафика | Длительность | Критерии перехода | Критерии авто-отката |
|------|-----------|--------------|-------------------|----------------------|
| 1 | 1% | 30 мин | error rate < 0.1%, p95 в бюджете | error rate > 1% или p95 > 2× бюджета |
| 2 | 10% | 2 часа | без инцидентов | см. выше |
| 3 | 50% | 4 часа | без инцидентов | см. выше |
| 4 | 100% | — | — | вручную откатываемо через feature flag |
```

**Add to Phase 7 (verify):** сценарий отката проверен на staging.

**Applies:**
- релиз фичи для публичного web-сервиса
- изменение алгоритма, критичного для UX

**Does NOT apply:**
- внутренние dev-инструменты
- проекты без прод-аудитории

---

## load-testing

**Summary:** Нагрузочный тест на staging — имитация реальной нагрузки перед релизом. Находит N+1, deadlocks, memory leaks до прода.

**Triggers:**
- keywords: `load test`, `stress test`, `benchmark`, `k6`, `locust`, `jmeter`, `rps`, `concurrency`, `hot path`, `performance`
- paths: `**/loadtest/**`, `**/benchmarks/**`, `**/perf/**`
- semantic: "задача меняет горячий участок (высоко-частотный endpoint, фоновый worker с объёмом), ожидается рост нагрузки, или готовится к пиковому событию"

**Prerequisites:** staging-среда с инфрой, приближённой к проду.

**Add to Phase 7 (verify):** секция `## Load Test Results`:

```md
## Load Test Results
- **Сценарий:** <какой пользовательский поток>
- **Нагрузка:** <N concurrent users / Y rps>
- **Длительность:** <X минут>
- **Результат:** p50/p95/p99, error rate, memory peak, CPU peak
- **Вердикт:** pass / fail против бюджета
- **Найденные проблемы:** <N+1, leaks, deadlocks — ссылки на фиксы>
```

**Applies:**
- «оптимизация поиска отзывов»
- подготовка к Black Friday / запуску
- миграция на новую БД

**Does NOT apply:**
- CLI-утилиты
- фичи с ожидаемой нагрузкой < 1 rps

---

## dast-scan

**Summary:** Автоматический сканер на работающем приложении (ZAP, Burp) — находит runtime-уязвимости, которые SAST не видит.

**Triggers:**
- keywords: `public api`, `web app`, `public endpoint`, `external`, `production-facing`, `open to internet`
- paths: `**/api/**` (если публичный), `**/web/**`, `**/frontend/**`
- semantic: "задача меняет поверхность, доступную из публичного интернета (не только внутренние сервисы)"

**Prerequisites:** наличие staging-среды, запущенной как production-like.

**Add to Phase 7 (verify):** DAST-прогон (OWASP ZAP baseline или full scan):

```md
## DAST Scan
- **Инструмент:** OWASP ZAP <baseline/full>
- **Target:** <staging URL>
- **Результат:** high=0, medium=X, low=Y
- **Фиксы:** <ссылки на PR>
- **Accepted risks:** <medium/low с обоснованием>
```

**Applies:**
- новый публичный API
- большие security-правки

**Does NOT apply:**
- внутренние инструменты за VPN
- изменения в бэкофис-админке

---

## mutation-testing

**Summary:** Компьютер ломает твой код и смотрит, падают ли тесты. Измеряет *качество* тестов (а не количество).

**Triggers:**
- keywords: `mutation test`, `mutmut`, `stryker`, `test quality`, `coverage`, `critical module`
- paths: `**/tests/**` (при зрелом тест-наборе 100+ тестов)
- semantic: "модуль является бизнес-критичным (деньги, безопасность, данные), и у него уже есть зрелый тест-набор, который хочется проверить на силу"

**Prerequisites:** модуль имеет >100 тестов (иначе mutation-testing даёт мусор).

**Add to Phase 7 (verify):** секция `## Mutation Test`:

```md
## Mutation Test
- **Module:** <target>
- **Tool:** <mutmut / stryker / cosmic-ray>
- **Mutation score:** <X%>
- **Threshold:** <≥60% для критичных, ≥40% для обычных>
- **Surviving mutants:** <короткий список с решением — добавить тест / accept>
```

**Applies:**
- core модули (auth, billing, data-pipeline)
- перед продом критичной фичи

**Does NOT apply:**
- свежий код с <20 тестов
- UI-код с визуальной проверкой

---

## eval-driven-ai

**Summary:** Regression-тесты для AI-фич. Golden dataset эталонных промптов и ответов. Каждое изменение промпта/модели — прогон, сравнение метрик.

**Triggers:**
- keywords: `prompt`, `system message`, `llm`, `gpt`, `claude`, `gemini`, `openai`, `anthropic`, `agent`, `skill`, `model`, `temperature`, `max_tokens`, `embedding`, `rag`
- paths: `**/prompts/**`, `**/*.prompt.md`, `**/agents/**`, `**/skills/**/SKILL.md`, `**/llm/**`, `**/ai/**`
- semantic: "задача изменяет промпт, модель, параметры LLM или AI-логику, которая отвечает пользователю"

**Prerequisites:** существует `evals/golden_dataset.jsonl` с ≥20 примерами. Если нет — Phase 1.5 предлагает создать как первую задачу.

**Add to Phase 4 (spec):** секция `## AI Evals Plan`:

```md
## AI Evals Plan
- **Dataset:** `evals/golden_dataset.jsonl` (<N примеров>)
- **Metrics:** accuracy, refusal_rate, hallucination_rate, p95_latency, cost_per_request
- **Baseline (до изменения):** <таблица цифр>
- **Threshold:** <relase-blocker если любая метрика упала на >X%>
- **Cost estimate:** <N примеров × средний ответ токенов × цена модели = $>
```

**Add to Phase 7 (verify):** прогон evals до/после. Таблица изменений:

```md
## AI Eval Run

| Метрика | До | После | Дельта | Статус |
|---------|-----|-------|--------|--------|
| Accuracy | 0.87 | 0.84 | −3.4% | ⚠ BLOCK |
| Refusal | 0.05 | 0.04 | −20% | ✓ |
| p95 latency | 4.2s | 3.8s | −9.5% | ✓ |
| Cost/req | $0.012 | $0.009 | −25% | ✓ |

Блок merge, если хоть одна метрика помечена BLOCK.
```

**Applies:**
- «улучши системный промпт для бота»
- «перейди с Claude 4.6 на Claude 4.7»
- «добавь новый skill в агента»

**Does NOT apply:**
- systemd unit, dockerfile, .env — не AI
- правки в `userbot.py`, не касающиеся промптов

---

## user-journey-acceptance

**Summary:** UI/frontend changes must be checked through a real user journey, not only component tests or visual inspection. The output is a short scenario plus browser smoke or explicit manual evidence.

**Triggers:**
- keywords: `frontend`, `ui`, `ux`, `page`, `component`, `react`, `vue`, `svelte`, `browser`, `playwright`, `form`, `button`, `modal`, `screen`
- paths: `**/frontend/**`, `**/web/**`, `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/components/**`, `**/pages/**`, `**/app/**`
- semantic: "задача меняет пользовательский интерфейс или пользовательский путь, где корректность определяется действиями пользователя"

**Prerequisites:** приложение можно запустить локально, или существует документированный ручной маршрут для проверки. Если нет, добавить это как residual risk.

**Add to Phase 4 (spec):** секция `## User Journey Acceptance`:

```md
## User Journey Acceptance
- **Journey:** <что пользователь делает шаг за шагом>
- **Expected result:** <что должно стать видимым или доступным>
- **Negative check:** <что не должно сломаться или появиться>
- **Evidence:** <browser smoke / screenshot / manual check>
```

**Add to Phase 6 (execute):** сохранить journey рядом со spec или report, например `docs/user-journeys/<topic>.md`, если сценарий длиннее 5 шагов.

**Add to Phase 7 (verify):** read `skills/pipeline/references/browser-acceptance.md`, apply its Evidence ladder, and execute browser smoke through `agent-browser`, Playwright, or project e2e tests when available. If automation is unavailable, record manual evidence plus residual risk. Include screenshot path or trace path when available, and check mobile and desktop when layout can differ.

**Applies:**
- «добавь форму настроек»
- «переделай страницу канала»
- «измени модалку оплаты»
- «почини frontend flow после backend API change»

**Does NOT apply:**
- backend-only API change with no visible UI surface
- copy-only change that is already covered by snapshot/manual review
- CLI-only workflow

---

## business-invariants-db

**Summary:** Бизнес-правила («баланс ≥ 0», «статус из списка {A,B,C}», «created_at ≤ updated_at») фиксируются как DB constraints, а не только в UI или коде. Плюс invariant-тест.

**Triggers:**
- keywords: `balance`, `amount`, `price`, `status`, `state`, `counter`, `quota`, `limit`, `transaction`, `order`, `payment`, `credit`, `debit`, `inventory`, `stock`
- paths: `**/models/**`, `**/entities/**`, `**/migrations/**`, `**/schema.prisma`
- semantic: "задача добавляет или меняет поле/таблицу, которое хранит финансовую величину, счётчик, статус из перечисления, или отношение во времени"

**Add to Phase 4 (spec):** секция `## Invariants`:

```md
## Invariants

| Правило | Где в UI | Где в коде | DB constraint | Тест |
|---------|----------|-----------|----------------|------|
| balance ≥ 0 | form validation | `Balance.validate()` | `CHECK (balance >= 0)` | unit + integration |
| status in {A,B,C} | dropdown | enum | `CHECK (status IN (...))` или ENUM type | unit |
| created_at ≤ updated_at | — | `before_update` hook | `CHECK (created_at <= updated_at)` | unit |
```

**Add to Phase 6 (execute):** constraint попадает в миграцию, не только в ORM.

**Add to Phase 7 (verify):** integration-тест — попытка нарушить инвариант прямым SQL → БД отказывает.

**Applies:**
- «добавь поле balance в users»
- «счётчик использованных кредитов»
- «статус заказа: pending/paid/shipped/cancelled»

**Does NOT apply:**
- текстовые поля без бизнес-правил (имя, заметка)
- чисто UI-изменения
