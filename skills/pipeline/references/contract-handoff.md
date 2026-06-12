# Downstream Contract Handoff

Create a handoff when one implementation surface produces data, behavior, or contracts consumed by another surface.

Typical producer/consumer pairs:
- backend -> frontend;
- API -> SDK/client;
- database/job -> analytics/UI;
- event producer -> worker/consumer;
- prompt/model output -> parser/downstream stage.

## When to create a handoff

Create a handoff when the task changes any of these:
- public or internal API endpoint;
- request, response, event, webhook, queue, or model-output schema;
- database shape read by another component;
- field semantics, defaults, nullability, enum values, errors, auth, pagination, sorting, cache, timing, or timezone behavior;
- generated types, fixtures, or test data consumed by another agent or team.

Do not create a separate handoff for typo-only edits, isolated styling, local refactors with no contract change, or docs-only changes that do not alter expected behavior.

## Backend -> Frontend/API Handoff

Use this compact template in the spec, implementation plan, report, or subagent contract.

Name producer files, consumer files, contract delta, compatibility, and acceptance handshake.

```md
## Downstream Contract Handoff

### Producer
- Owner/files:
- Change summary:
- Runtime route/job/stage:

### Consumers
- Owner/files:
- UI/API/worker surfaces:
- Generated types or fixtures to update:

### Contract delta
| Field/behavior | Before | After | Required consumer action |
|---|---|---|---|
| <name> | <old> | <new> | <update/test> |

### Compatibility
- Backward compatible: yes/no
- Migration or fallback:
- Empty/loading/error state:
- Auth/permission impact:
- Caching, pagination, timezone, or sorting impact:

### Producer responsibilities
- Tests:
- Example payload/fixture:
- Error cases:

### Consumer responsibilities
- Tests:
- UI/manual acceptance:
- Copy or explanation needed for users:

### Acceptance handshake
- Producer verification command:
- Consumer verification command or manual check:
- Evidence location:

### Out of scope
- <what this contract change does not cover>
```

## Agent handoff rules

- Put the handoff in the artifact that the next owner will actually receive: spec, implementation plan, subagent prompt, or report.
- If producer and consumer are implemented by separate agents, both contracts must reference the same handoff.
- When dispatching separate producer and consumer agents, include the Contract delta table and verification commands in both subagent prompts.
- If only one side is implemented now, record the other side as follow-up or residual risk.
- If the contract is uncertain, stop guessing. Add an open question or a small prototype spike before implementation. If the contract cannot be written clearly, stop or serialize the work.
- Do not hide compatibility changes in prose. Use the `Contract delta` table.

## Plain-language reason

This prevents the common failure where backend work is "done", but frontend, API clients, tests, or docs do not know what changed. The handoff is the receipt that lets the next agent see exactly what to consume, test, and explain.
