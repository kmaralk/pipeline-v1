# Premortem Plan Review

This is not a fourth pipeline mode. It is a short plan-quality gate inside the selected mode.

Use it before the pipeline commits to a costly plan, autonomous implementation, Codex-heavy batch, broad refactor, launch, pricing change, contract change, or other medium/high-risk decision.

## Optional Run-Control Flag

Record the control state as:

```text
`premortem_plan_review`: `auto | forced | skipped`
```

- `P` forces premortem plan review, even if the automatic risk gate would skip it.
- No `P` keeps `premortem_plan_review=auto`: the pipeline still runs premortem when task risk, mode placement, or autonomous/Codex-heavy execution requires it.
- `-P` marks optional premortem as skipped for low-risk work. Do not use `-P` to bypass a mandatory high-risk safety gate without recording residual risk.

When parsing user shorthand, treat `-P` and `P` as exact tokens and check exact `-P` before exact `P`.

## Relation To Run Control

The selected `run_control` remains sticky. Premortem can find holes, but it must not reset the chosen collaboration profile or autonomy level.

- Collaboration profile decides who helps inspect the plan.
- Autonomy level decides whether accepted mitigations can be executed without asking again.
- In `C4` Codex-heavy, Codex may help find technical holes or implementation details, but Claude/current orchestrator keeps guardrails and ratifies scope decisions.
- In `A1`, ask before accepting mitigations.
- In `A2`, execute only safe reversible mitigations; ask for scope, cost, or risk changes.
- In `A3`/`A4`, accepted blocking holes inherit the current `run_control`; continue autonomously within accepted scope.
- New features require explicit acceptance or a new pipeline, even in `A3`/`A4`.

Do not let premortem holes silently expand scope. Classify each hole before action:
- blocking current acceptance;
- non-blocking bug or risk;
- new feature/scope.

Only accepted blocking holes inherit the current `run_control`. Non-blocking holes are recorded as deferred/backlog unless explicitly accepted, and new features require explicit acceptance.

## Mode Placement

- `pipeline-lite`: use only for medium/high-risk, behavior-changing, multi-file, user-facing, contract, migration, or unclear work. Skip for trivial docs, typo, or obvious one-file fixes. Run before Phase 3 Execute.
- `pipeline-deep`: run in Phase 4 before spec approval and before Phase 5 Planning and Handoff.
- `pipeline-hard`: run in Phase 5 Consolidation before Phase 6 Implementation Planning, and before Codex-heavy or autonomous implementation.

## Minimum Context

Use what is already in files and conversation. Ask at most two focused questions at a time. If something stays unclear after a short pass, write it as an assumption instead of blocking forever.

Minimum fields:
- subject: what plan or change is being evaluated;
- audience or affected user;
- success signal;
- horizon: when failure is judged;
- reference class: what similar past project or known example this resembles.

## Frame

Do not ask "is this a good plan" or "what could go wrong". Use past-tense failure framing:

```text
By <horizon>, this plan failed. What specifically happened?
```

The point is concrete failure causes, not generic risk lists.

## Lenses

Use 4-6 lenses depending on task size:
- customer/user: why the target person rejects, ignores, or misunderstands it;
- executor/team: what the people building or operating it cannot actually do;
- competitor/alternative: what wins instead;
- assumptions/evidence: what the plan treats as true without proof;
- future maintainer/operator: how this breaks after attention moves elsewhere;
- situational lens: security, pricing, migration, rollout, support, legal, data, or performance when relevant.

The named lenses are a starting set, not a closed taxonomy. Keep the 4-6 lens budget: substitute a standard lens for a more relevant viewpoint such as accessibility, privacy, compliance, localization, data quality, or operational recovery when the task clearly needs it. If the plan appears to need more than 6 lenses, split or narrow the review instead of adding more roles.

Always include one WYSIATI check: whose view or information is missing from the room?

## Decision Doubt Inside Premortem

Decision doubt is a default extra evaluator inside premortem when the plan contains a concrete risky decision. It is not a separate mode, flag, or function.

Use it for a specific decision, not for the whole plan. Typical triggers: architecture, API, migration, security, expensive implementation, Codex-heavy, or autonomous execution.

Frame it as:

```text
This decision is wrong or incomplete. What specifically breaks?
```

Check only 1-3 decisions in a normal deep/hard premortem. Keep it bounded for lite, and skip it for trivial work. The goal is to catch a wrong decision before implementation, not to create a second review ceremony.

For each decision-doubt finding:
- name the decision being tested;
- explain what breaks if it is wrong;
- classify it as blocking, non-blocking, or new scope;
- choose fix, defer, accept risk, or reject.

Do not duplicate the main premortem holes. If a decision-doubt finding is already covered by a hole, merge it into that hole and keep the output compact.

## Output Shape

Keep the output compact:
- 5-8 concrete holes for deep/hard; 3-5 for lite unless the risk justifies more.
- Each hole gets a short title, why it matters, confidence marker, and classification.
- Confidence markers: `backed by context`, `needs verification`, `assumption`.
- For each accepted hole, record one first step and owner: `agent`, `human`, or `both`.
- Select top 1-3 accepted holes. Do not try to fix every hole at once.
- Final recommendation must be one of: `continue | reduce_stake | delay | abort`.

Recommended report block:

```md
## Premortem Plan Review
- Frame: By <horizon>, this plan failed. What specifically happened?
- Lenses: <used lenses>

### Holes
1. H-001 - <title>
   - Why it matters: <plain language>
   - Confidence: backed by context | needs verification | assumption
   - Classification: blocking | non-blocking | new scope
   - Decision: accepted | deferred | rejected
   - First step: <only if accepted>
   - Owner: agent | human | both

### Top 1-3
- H-001 - <first step>

### Recommendation
continue | reduce_stake | delay | abort
```

## Reverse Premortem

Reverse premortem is required when the recommendation is `reduce_stake`, `delay`, or `abort`.

Use this frame:

```text
By <horizon>, we did not do it, or did much less. That turned out to be a mistake. Why?
```

Return 2-3 strong reasons and one sentence saying what outweighs what. This prevents the review from becoming automatic pessimism.

## Non-Goals

- Do not assign numeric probabilities.
- Do not run heavyweight FMEA unless the user asks for that kind of formal risk method.
- Do not create a separate decision journal when the current design/report/state files can hold the result.
- Do not run premortem for trivial changes where it would be ceremony.
