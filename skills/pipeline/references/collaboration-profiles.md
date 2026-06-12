# Pipeline Collaboration Profiles

Use this reference when `pipeline-deep` or `pipeline-hard` needs an explicit `Model Collaboration Profile` answer to:

```text
Кто работает? Ответ: C1-C4
```

This is separate from autonomy. Collaboration answers **who participates**. Autonomy answers **how independently the selected agents work without the human operator**.

## Menu

```text
Кто работает? Ответ: C1-C4

C1 Один основной агент
    Всё делает тот AI, где сейчас работаем: Claude Code или Codex.
    Для экономии и простых задач.

C2 Primary + Secondary checkpoints
    Один основной агент ведёт работу, второй подключается на ключевые проверки:
    spec review, plan review, code review, edge cases.
    Legacy alias: Claude-main + Codex checkpoints.
    Для баланса цены и качества.

C3 Dual-head quality
    Claude Code и Codex оба смотрят ключевые фазы.
    Один главный, второй критикует; спорные замечания ratify.
    Для максимального качества, когда лимиты позволяют.

C4 Heavy executor + Guardrail reviewer (Recommended)
    Тяжёлый исполнитель берёт основную техническую работу:
    detailed plan, code, tests, self-review.
    Guardrail reviewer экономно держит цель, рамки, ratification и final review.
    Legacy alias: Codex-heavy + Claude guardrails.
    На текущей установке recommended tuple: Codex executor + Claude Code reviewer.
    Для длинных задач или когда основной context нужно экономить.

Дополнительно:
X Cross-check в начале
    Спросить несколько моделей на этапе выбора подхода.
P Premortem plan review перед реализацией
    Принудительно проверить план фреймом "план провалился - почему?".
-P Skip optional premortem
    Пропустить только optional premortem для low-risk задач; high-risk safety gate требует residual-risk note.
```

Run-control shorthand:

```text
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

Alias normalization:

- `heavy`, `режим heavy`, `heavy mode`, `тяжелый режим`, `autonom+heavy`, `autonomous heavy`, and `autonom heavy` mean `C4 A3` unless the user explicitly names a different `A#`.
- `ok` means `C4 A3`.
- Do not ignore a bare `heavy` by falling back to memory or older defaults.

If the user answers legacy digits like `4 2`, treat them as `C4 A2`, then record normalized state values. A bare collaboration digit maps to `C#` only when the autonomy choice is otherwise explicit or still being asked.

Default:

```text
codex_heavy_claude_guardrails
```

Use another profile when the user asks for solo execution, cheaper execution, two heads, or quality-first review.

## Canonical Gap-Closure Rules

- Run Control first response must use the four-profile menu exactly when the profile is missing, with `C1`-`C4` labels.
- cross-check remains a checkbox, never a profile label.
- Premortem remains an optional/automatic plan-review flag, never a fifth collaboration profile.
- Ratify disputed findings before asking the human operator; ask the human operator only on blocking scope, architecture, contract, security, test-weakening, or unlocalized repeated-failure risk.
- Cross-check output is reconciled into the spec or approach note before implementation planning.

Run-control gap closure minimum floor:

- C2 minimum: primary owns requirements, spec, plan, acceptance, and handoff; Phase 7.5 requires primary final review plus secondary cross-review when the secondary is available.
- C3 minimum: both Claude and Codex check key phases; disputed findings use Accepted / Rejected / Accepted with change, reason, action, and reversibility.
- C4 minimum: heavy executor self-review plus guardrail-reviewer final-review; on the current deployment this means Codex self-review plus Claude final-review.
- Cross-check minimum: keep exactly four collaboration profiles; cross-check is an optional early checkbox for approach selection and is reconciled into the spec.
- State minimum: record `collaboration_profile` independently from `autonomy`; do not infer one from the other.

## State Fields

Record the selected profile in state:

```json
{
  "orchestration": {
    "collaboration_profile": "solo_primary | claude_main_codex_checkpoints | dual_head_quality | codex_heavy_claude_guardrails",
    "cross_check_initial": false,
    "premortem_plan_review": "auto | forced | skipped"
  }
}
```

Provider-neutral role layer:

```json
{
  "orchestration": {
    "roles": {
      "orchestrator": "current_model | claude_code | codex",
      "executor": "current_model | claude_code | codex",
      "reviewer": "current_model | claude_code | codex",
      "helpers": ["claude_code | codex"]
    }
  }
}
```

This role layer is intentionally limited to Claude Code and Codex. Other model families remain manual oracle material unless a later approved pipeline-update adds their invocation, safety, and eval coverage.

Legacy aliases remain supported:
- `claude_main_codex_checkpoints` means the current primary role is Claude Code and the secondary checkpoint reviewer is Codex unless the user says Codex is primary.
- `codex_heavy_claude_guardrails` means the heavy executor is Codex and the guardrail reviewer is Claude Code on this setup.
- If the user says "Codex main, Claude checkpoints", keep `collaboration_profile=claude_main_codex_checkpoints` for backward compatibility and set `roles.orchestrator=codex`, `roles.executor=codex`, `roles.reviewer=claude_code`, `roles.helpers=["claude_code"]`.
- If the user says "Claude main, Codex checkpoints", set `roles.orchestrator=claude_code`, `roles.executor=claude_code`, `roles.reviewer=codex`, `roles.helpers=["codex"]`.

Keep existing strategy fields for compatibility:

```json
{
  "orchestration": {
    "spec_strategy": "current_model | cross_review | codex_details",
    "planning_strategy": "current_model | cross_review | codex_tdd_plan",
    "executor": "current_model | codex"
  }
}
```

## Profile 1: Solo Primary Agent

Plain meaning:

```text
One model does the run because budget, access, or task size does not justify a second model.
```

Typical derived defaults:

```text
spec_strategy = current_model
planning_strategy = current_model
executor = current_model
review_overlay = baseline_review
```

Pipeline-hard phase behavior:

| Phase | Behavior |
|---|---|
| Phase 1-2 | Current agent gathers requirements and investigates |
| Phase 3-4 | Oracle can be skipped unless needed |
| Phase 5 | Current agent writes spec |
| Phase 6 | Current agent writes plan |
| Phase 7 | Current agent implements or uses separately approved delegation |
| Phase 7.5 | Main review plus baseline review; second model not mandatory |
| Phase 8-11 | Current agent accepts, reports, and offers completion choices |

Pipeline-deep behavior:

```text
Use normal discovery/spec/plan/execute/acceptance flow.
Do not schedule mandatory Codex calls.
```

## Profile 2: Primary + Secondary Checkpoints (Claude-main + Codex Checkpoints legacy alias)

Plain meaning:

```text
The primary agent leads the work. The secondary agent is used only where a second technical head is high-value.
```

Typical derived defaults:

```text
spec_strategy = cross_review
planning_strategy = cross_review
executor = current_model
review_overlay = primary_final_review + secondary_cross_review
```

Pipeline-hard phase behavior:

| Phase | Behavior |
|---|---|
| Phase 1-2 | Primary agent leads requirements and investigation |
| Phase 3-4 | Prepare a short secondary-agent critique prompt for key risks |
| Phase 5 | Primary writes spec; secondary reviews gaps, edge cases, contracts |
| Phase 6 | Primary writes plan; secondary checks TDD detail and missing risks |
| Phase 7 | Primary usually implements; secondary can help on a chosen batch |
| Phase 7.5 | Primary final review plus secondary cross-review when available |
| Phase 8-11 | Primary agent owns acceptance, deferred decisions, handoff |

Secondary review supplements primary review. It does not replace it.

Pipeline-deep behavior:

```text
Use the secondary agent sparingly for risky spec, plan, and code-review checkpoints.
Keep discovery and implementation lightweight unless the task escalates to hard.
```

## Profile 3: Dual-head Quality

Plain meaning:

```text
Claude and Codex both check key phases because quality matters more than token economy.
```

Typical derived defaults:

```text
spec_strategy = cross_review
planning_strategy = cross_review or codex_tdd_plan
executor = chosen_main_executor
review_overlay = mandatory_dual_review_with_ratification
```

Pipeline-hard phase behavior:

| Phase | Behavior |
|---|---|
| Phase 1 | Second head checks requirements and hidden questions |
| Phase 1.5 | Both check whether risk practices were missed |
| Phase 2 | Both inspect important risks from different angles |
| Phase 3-4 | One model prepares the oracle angle; the other critiques |
| Phase 5 | One drafts spec; the other reviews gaps |
| Phase 6 | One drafts plan; the other reviews or writes TDD details |
| Phase 7 | One implements; the other checks critical checkpoints |
| Phase 7.5 | Claude and Codex both review the diff; findings are ratified |
| Phase 8-11 | Main agent consolidates acceptance and handoff |

Ratification template:

```text
Finding:
<what the second model said>

Decision:
Accepted / Rejected / Accepted with change

Reason:
<why>

Action:
<what changes, if accepted>

Reversibility:
S / M / L
```

Pipeline-deep behavior:

```text
Use this only when requested or when the user explicitly prefers quality over cost.
If the task becomes large and multi-milestone, consider escalating to pipeline-hard.
```

## Profile 4: Heavy Executor + Guardrail Reviewer (Codex-heavy + Claude Guardrails legacy alias)

Plain meaning:

```text
The heavy executor carries detailed technical work. The guardrail reviewer conserves context and owns goals, boundaries, ratification, and final review.
```

Typical derived defaults (role-neutral; legacy alias on current deployment in parentheses):

```text
spec_strategy = guardrail-reviewer requirements frame + heavy-executor requirements critique + broad-spec review
planning_strategy = guardrail-reviewer TDD recommendations + heavy-executor detailed TDD plan
executor = heavy-executor
review_overlay = heavy-executor self-review plus TAR plus guardrail-reviewer final-review

# Legacy alias on current deployment: heavy-executor = Codex, guardrail-reviewer = Claude Code.
# Flipped-role deployments swap providers in orchestration.roles without rewriting this text.
```

Use for:

- long technical work;
- guardrail-reviewer token pressure (on current deployment: Claude token pressure);
- heavy-executor has enough budget and tool access (on current deployment: Codex budget);
- overnight Symbiosis Loop;
- detailed TDD plan/code/test execution is the bottleneck.

Loop (role-neutral; substitute providers per `orchestration.roles`):

1. guardrail-reviewer fixes goal, boundaries, non-goals, stop conditions, and what must not break.
2. heavy-executor runs requirements critique: hidden questions, contradictions, edge cases, and underdefined behavior.
3. guardrail-reviewer ratifies findings with accept/reject, reason, and reversibility.
4. guardrail-reviewer writes broad-spec/broad-plan.
5. heavy-executor reviews broad-spec: contracts, UX/API/data implications, backward compatibility, testability, and missed risks.
6. guardrail-reviewer ratifies findings again and updates the frame.
7. guardrail-reviewer writes TDD recommendations for heavy-executor: invariants, required RED proof, edge cases, and tests that must not be weakened.
8. heavy-executor writes detailed TDD plan from guardrail-reviewer's recommendations.
9. guardrail-reviewer spot-checks the detailed TDD plan.
10. heavy-executor implements tests/code/checks.
11. heavy-executor self-reviews.
12. guardrail-reviewer runs or ratifies Test Adequacy Review.
13. guardrail-reviewer final-reviews and decides merge/acceptance.

(Legacy reading on current deployment, heavy-executor = Codex and guardrail-reviewer = Claude Code, so the loop reads: Claude fixes goal, boundaries, non-goals, stop conditions; Codex runs requirements critique; Claude ratifies; Claude writes broad-spec/broad-plan; Codex reviews broad-spec; Claude ratifies; Claude writes TDD recommendations for Codex; Codex writes detailed TDD plan from Claude's recommendations; Claude spot-checks the detailed TDD plan; Codex implements; Codex self-reviews; Claude runs or ratifies Test Adequacy Review; Claude final-reviews. Flipped-role deployments swap providers without rewriting this loop.)

Pipeline-hard phase behavior (role-neutral; on current deployment `heavy-executor = Codex`, `guardrail-reviewer = Claude Code`):

| Phase | Behavior |
|---|---|
| Phase 1 | guardrail-reviewer fixes goal, boundaries, non-goals, and stop conditions; heavy-executor runs requirements critique |
| Phase 1.5 | guardrail-reviewer chooses mandatory practices and constraints for heavy-executor |
| Phase 2 | guardrail-reviewer gathers only needed context; heavy-executor critique optional |
| Phase 3-4 | heavy-executor review of broad-plan or key technical direction |
| Phase 5 | guardrail-reviewer broad-spec/broad-plan plus heavy-executor spec review and guardrail-reviewer ratification |
| Phase 6 | guardrail-reviewer writes TDD recommendations; heavy-executor writes detailed TDD plan; guardrail-reviewer spot-checks |
| Phase 7 | heavy-executor implements tests/code/checks |
| Phase 7.5 | heavy-executor self-review plus TAR plus guardrail-reviewer final-review |
| Phase 8 | guardrail-reviewer checks evidence; heavy-executor fixes accepted failures |
| Phase 9-11 | guardrail-reviewer owns deferred decisions, handoff, and completion |

Legacy reading on current deployment (heavy-executor = Codex, guardrail-reviewer = Claude Code):
- Phase 1 | Claude fixes goal, boundaries, non-goals, and stop conditions; Codex runs requirements critique
- Phase 5 | Claude broad-spec/broad-plan plus Codex spec review and Claude ratification
- Phase 6 | Claude writes TDD recommendations; Codex writes detailed TDD plan; Claude spot-checks
- Phase 7 | Codex implements tests/code/checks; Phase 7.5 | Codex self-review plus TAR plus Claude final-review; Phase 8 | Claude checks evidence; Codex fixes accepted failures

Pipeline-deep behavior:

```text
Usually escalate to pipeline-hard for a full Codex-heavy run.
If staying in deep, keep the loop compact and avoid night protocol unless explicitly selected.
```

## Cross-check Checkbox

Cross-check is not a fifth profile.

`Cross-check` is an optional checkbox.

Use it as an optional one-shot early oracle when choosing an approach:

| Phase | Use |
|---|---|
| Phase 2 | Compare risks and approaches |
| Phase 3 | Prepare one clean context pack and question |
| Phase 4 | Run the multi-model answer |
| Phase 5 | Reconcile answers into the spec |

Do not run cross-check:

- after every milestone;
- at the end just in case;
- as a replacement for profile-specific Phase 7.5 review;
- as a new `Multi-model oracle` profile.

## Review Overlay

Phase 7.5 review depends on the profile:

| Profile | Review overlay |
|---|---|
| `solo_primary` | Main review plus baseline review |
| `claude_main_codex_checkpoints` | Primary final review plus secondary cross-review when available |
| `dual_head_quality` | Claude and Codex both review; findings are ratified |
| `codex_heavy_claude_guardrails` | Codex self-review plus Claude final-review |

The overlay is applied before the normal Review Menu. It can add required review layers; it does not remove security scans, baseline review, scope/diff audit, or acceptance evidence.

## Provider Neutrality

The pipeline treats `Claude` and `Codex` as concrete providers, not as roles. Roles are role-neutral:

| Role (canonical) | Legacy alias on current deployment |
|---|---|
| `orchestrator` | Claude Code (in C2/C4 default) |
| `guardrail-reviewer` | Claude Code (in C4 default) |
| `executor` / `heavy-executor` | Codex (in C4 default) |
| `reviewer` (cross-agent or checkpoint) | the other provider, whoever is not orchestrator/executor |

Rules:

1. In role positions in canonical SKILL.md and references, prefer role-neutral names (`orchestrator`, `guardrail-reviewer`, `executor`, `heavy-executor`, `reviewer`). The role-to-provider mapping lives in the `orchestration.roles` state field.
2. For flipped-role deployments (e.g. Codex as orchestrator, Claude Code as executor), the role-neutral text continues to apply without rewriting. The plain-meaning loop steps describe the legacy alias as the default but are not normative for flipped roles.
3. Behavioral evals that name a provider in role position must include an example mapping or be tagged as legacy-alias scenarios.

## Legitimate Provider Mentions

The following provider mentions are intentional and must NOT be rewritten by a provider-neutrality pass:

- CLI / product invocation surfaces: `Codex Invocation Ladder`, `Claude Invocation Ladder`, command templates in `orchestration.md`, `tool-inventory.md`, `autonomy-safeguards.md` Codex Progress Watchdog, `/codex-security-scan`, plugin names, MCP tool names.
- Premium-oracle references: `ChatGPT Pro`, Claude web, Gemini, Repo Prompt — these are concrete product names in the manual premium oracle route.
- `STATE.md` historical ledger entries that record what was actually done by which provider.
- Behavioral eval cases where the user query explicitly named a provider — those are user-input fidelity, not role-position text.
- Run Control menu legacy aliases shown in parentheses (e.g. `legacy: Codex-heavy + Claude guardrails`) — these are aliases for discoverability.
- The plain-meaning Profile 4 loop steps in this file: they describe the legacy alias deployment and are intentional. Flipped-role deployments rely on the role-neutral mapping table above rather than rewriting the loop.

A future provider-neutrality pass that touches any of the items in this whitelist must add an explicit rationale to the commit message.
