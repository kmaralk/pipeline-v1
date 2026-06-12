# Pipeline Autonomy Levels

Use this reference when `pipeline-deep` or `pipeline-hard` needs an explicit answer to:

```text
Автономность? Ответ: A1-A4
```

This is separate from collaboration. Autonomy answers **how independently the selected agents work without the human operator**. Collaboration answers **who participates**.

## Menu

```text
Автономность? Ответ: A1-A4

A1 Interactive
    Спрашивать пользователя перед крупными шагами:
    spec, plan, implementation, review, merge/completion.
    Лучше, когда пользователь рядом и хочет контролировать решения.

A2 Guided autonomous
    Делать самому всё безопасное.
    Спрашивать только при рисках, неоднозначности, scope change,
    поломанных тестах без понятного fix path или dangerous actions.

A3 Full autonomous (Recommended)
    После preflight идти максимально самостоятельно до acceptance.
    Для дневной автономной работы на 1-3 часа.
    Вести lightweight run-log: progress, commands, failures,
    localization notes, blockers.
    Без ночного протокола: нет обязательного night-log, hard cap,
    morning handoff и milestone sub-branches.

A4 Overnight
    Ночная автономная смена на 6-8 часов.
    Требует night-handoff.md, hard cap timer, night-log.md,
    state.json discipline, stop conditions, milestone boundaries,
    self-review/final-review и morning handoff.
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

If the user answers legacy digits like `4 2`, treat them as `C4 A2`, then record normalized state values. A bare autonomy digit maps to `A#` only when the collaboration choice is otherwise explicit or still being asked.

Default:

```text
full_autonomous
```

## Canonical Gap-Closure Rules

- Guided autonomous default means proceed on safe reversible work and ask only for risk, ambiguity, scope change, broken tests without a clear fix path, or dangerous actions.
- Full autonomous default means proceed independently after run-control acceptance and preflight.
- Ask conditions summary: scope, architecture, contract, security, test weakening, unlocalized repeated failures, dangerous actions.
- Full autonomous requires lightweight run-log; Overnight requires night-handoff, hard cap, night-log, state.json discipline, milestone boundaries, and morning handoff.
- Overnight blocker classes are exactly `deferable_question`, `local_blocker`, `scope_blocker`, and `hard_stop`.

Autonomy gap closure minimum floor:

- A2 minimum: choose Guided autonomous from safe-work/risk-question wording; proceed on safe reversible work without micromanagement.
- A2 ask minimum: ask on scope, architecture, contract, security, test weakening, unlocalized repeated failures, or dangerous actions.
- A3 minimum: Full autonomous daytime work keeps a lightweight run-log.
- A4 minimum: Overnight requires night-handoff, hard cap, night-log, state.json discipline, milestone boundaries, profile-specific self-review/final-review, and Russian morning handoff.
- Overnight blocker classes are exactly `deferable_question`, `local_blocker`, `scope_blocker`, and `hard_stop`.

## State Fields

Record:

```json
{
  "orchestration": {
    "autonomy": "interactive | guided_autonomous | full_autonomous | overnight",
    "premortem_plan_review": "auto | forced | skipped"
  }
}
```

Parse exact premortem tokens before execution: exact `-P` marks optional premortem as skipped; exact `P` forces premortem plan review. No `P` keeps `premortem_plan_review=auto`, so the pipeline still runs premortem for risky work. Do not use `-P` to bypass a mandatory high-risk safety gate without recording residual risk.

Existing state files may only contain:

```text
interactive | guided_autonomous | full_autonomous
```

Treat missing autonomy as `full_autonomous`.

## Interactive

Plain meaning:

```text
Work, but ask the human operator before every major turn.
```

AI may:

- read files;
- gather context;
- draft options;
- find risks;
- write draft spec/plan;
- formulate questions.

AI must ask before:

- final spec;
- implementation plan;
- implementation start;
- Review Menu;
- merge, PR, or completion;
- any dangerous or irreversible action.

## Guided Autonomous

Plain meaning:

```text
Do safe work independently. Ask only when real risk appears.
```

Use this when the user wants a safer autonomous mode than the default.

AI may:

- choose safe branch/worktree defaults;
- select relevant practices;
- investigate;
- prepare oracle packs;
- write spec and plan;
- implement approved scope;
- run tests/review/acceptance;
- record deferred decisions.

For `guided_autonomous`, run Test Adequacy Review when work is test-changing, behavior-changing, security/data/contract-sensitive, or regression-fix work. the human operator is not expected to personally judge test adequacy from code unless he explicitly says he is doing that review.

AI must ask on:

- scope change;
- architecture change;
- public contract/schema change;
- security uncertainty;
- deleting, skipping, or weakening tests;
- failure remains unlocalized after retry limit;
- dangerous action cannot be safely deferred.

## Full Autonomous

Plain meaning:

```text
the human operator stepped away for 1-3 hours. Work independently and leave enough trace to resume quickly.
```

This is not overnight.

Requires a lightweight run-log:

```text
docs/reports/YYYY-MM-DD-<topic>-run-log.md
```

or a section in the implementation report:

```text
## Autonomous Run Log
```

Log:

- phase or milestone start;
- phase or milestone finish;
- commands run;
- pass/fail result;
- changed files summary;
- blockers;
- retry attempts;
- short localization notes after failures.

Do not log:

- every small thought;
- every file read;
- every minor decision;
- full ratification for every small point;
- mandatory morning handoff;
- hard cap accounting unless explicitly requested.

Before a non-trivial fix after a failure, write:

```text
symptom -> evidence -> suspected layer -> next action
```

If localization is unclear after 3 attempts:

```text
stop and ask the human operator
```

Before completion, `full_autonomous` runs Test Adequacy Review for test-changing or behavior-changing work and records the TAR verdict in the run-log or implementation report.

## Overnight

Plain meaning:

```text
the human operator is away/asleep for a night shift. AI can work for 6-8 hours, but only with rails, logs, and stop conditions.
```

Requires:

- `night-handoff.md`;
- append-only `night-log.md`;
- `state.json` surgical edits;
- hard cap timer, usually 8h;
- stop conditions;
- milestone boundaries;
- sub-branches where useful;
- self-review/final-review according to collaboration profile;
- Test Adequacy Review before morning handoff when tests or behavior changed;
- Russian morning handoff.

Typical files:

```text
docs/plans/YYYY-MM-DD-<topic>-night-handoff.md
docs/plans/YYYY-MM-DD-<topic>-night-log.md
docs/plans/YYYY-MM-DD-<topic>-state.json
docs/plans/YYYY-MM-DD-<topic>-morning-handoff.md
```

Night-log event types:

```text
STARTED
FINISHED
DECIDED
QUESTION
BLOCKED
BLOCKED-BUT-CONTINUING
RETRY
MERGED
STOPPED
```

Important `DECIDED` entries include:

```text
what:
why:
evidence:
risk:
reversibility: S / M / L
morning attention:
```

## Full Autonomous vs Overnight

| Question | Full autonomous | Overnight |
|---|---|---|
| Absence | 1-3 hours | 6-8 hours |
| the human operator may check progress | Yes | Usually no |
| Log | lightweight run-log | append-only night-log |
| State discipline | normal pipeline state/report | strict state.json surgical edits |
| Hard cap | optional | required |
| Morning handoff | optional | required |
| Milestone sub-branches | optional | recommended for large run |
| Decisions | important ones | all important decisions with why and reversibility |
| Blockers | stop or ask | classify: defer, continue, or stop |

## Deferred-But-Continue Protocol

In `Overnight`, do not stop on every question.

Algorithm:

```text
1. Name the blocker.
2. Classify it.
3. If safe to isolate, record and continue independent work.
4. If unsafe to continue, stop.
5. Morning handoff shows what was done, what was skipped, why, and what the human operator must decide.
```

Blocker types:

| Type | Meaning | Action |
|---|---|---|
| `deferable_question` | Question is open, but a safe default exists or it can wait | Record in deferred/morning handoff, continue |
| `local_blocker` | One milestone is blocked, but other milestones are independent | Freeze milestone, continue next independent milestone |
| `scope_blocker` | Scope expansion or contract change is needed | Do not expand silently; continue only safe independent work |
| `hard_stop` | Continuing is unsafe | Stop immediately |

Continue only when all are true:

- no architecture change;
- no prod/data/contract risk;
- blocked work can be isolated;
- independent next task exists;
- acceptance can honestly show done vs deferred;
- reversibility is S or M;
- no silent test deletion or weakening is needed.

Stop when:

- new architecture choice is needed;
- public API/schema/contract changes;
- safe option is unclear;
- remaining milestones depend on the blocker;
- prod/data risk appears;
- common tests are red and unlocalized;
- fix requires allowed-scope expansion;
- tests must be deleted or weakened;
- hard cap expired;
- the executor/tool fails 3 times on the same blocker.

## Ask / Default / Stop

When asking the human operator under these ask/default/stop rules, use `shared.md §Human Decision Questions`. Do not use that format for the C/A run-control menu.

AI must ask the human operator at any autonomy level when:

- architecture changes;
- public API/schema/auth contract changes;
- allowed scope expands;
- production deploy or prod/VPS service touch is needed;
- secrets or privileged access are needed;
- destructive or irreversible action is needed;
- tests would be deleted, skipped, or weakened;
- critical review remains unresolved after retry limit;
- branch mismatch or corrupt state blocks safe resume.

AI may choose a default when:

- the work is inside approved scope;
- the decision is reversible;
- no prod, secrets, data loss, or destructive action is involved;
- verification exists;
- the decision is logged when autonomy is `full_autonomous` or `overnight`.

AI must stop when:

- 3 retries fail without new understanding;
- a design invariant contradicts code;
- all remaining work depends on an unresolved blocker;
- disk or auth failure blocks required verification/push;
- prod or unrelated services were touched accidentally;
- overnight hard cap expires;
- state is corrupt and cannot be resumed safely.

## Forbidden At Any Autonomy

- `git reset --hard`;
- `git push --force`;
- `--no-verify`;
- `git commit --amend` on existing commits;
- push to `main` or `master`;
- silently change eval-tested skill descriptions;
- full-round-trip rewrite of `state.json` when surgical edit is required;
- touch V0 prod or unrelated VPS services;
- destructive migration without approval;
- hide skipped, deleted, weakened, or excluded tests;
- claim done without relevant review and acceptance evidence.
