# Ship Readiness

Use this only when the change can affect real users, production runtime, a launch, rollout, pricing, data, or operations.

It is not required for docs-only, skill-only, local refactor, or test-only work unless that work changes how a real runtime will be released or operated. Record `N/A` with a reason when ship readiness does not apply.

## Launch Checklist

For release-impacting work, record:

- rollback: exact revert path, feature flag off switch, config rollback, migration rollback, or restore plan;
- metrics: what to watch after release and where to see it;
- feature flag: flag name, default state, owner, and expiry/removal plan if a flag exists;
- first hour: checks to run during the first hour after launch;
- error response: what to do if logs, alerts, support messages, or business metrics go wrong;
- staged rollout: who gets it first and how it expands, when relevant;
- data safety: backup, migration verification, idempotency, and restore notes when data changes;
- support/comms: who needs to know and what message is ready, when users or operators are affected.

The launch checklist is a baseline, not an exhaustive release plan. Add task-specific launch checks for compliance, privacy, legal, billing, migration windows, partner dependencies, mobile app review, customer support load, or incident ownership when the task suggests them. Do not force irrelevant release ceremony onto no-runtime-impact work.

## First-Hour Evidence

If the change ships immediately, collect or define:

- deployment or release identifier;
- smoke route, CLI command, API request, or job check;
- dashboard, log query, alert, or metric name;
- success threshold;
- rollback threshold.

If the agent cannot deploy or observe production, record the launch checks as handoff instructions instead of pretending they were run.

## Runtime Gate Evidence

For runtime-facing, production, multiservice, billing, webhook, worker, bot, inference, or integration changes, implementation is not acceptance. Before closing, collect or define:

- smoke route, CLI command, API request, job check, or user-triggered event that exercises the changed path;
- named log sources for each critical service touched, such as gateway, webhook, worker, billing, model server, queue, scheduler, or bot runtime;
- current-agent readback/smoke evidence and logs from every touched service when log access exists;
- observation window chosen for this change and why it is enough;
- success threshold for the smoke result, logs, metrics, alerts, or business event;
- rollback threshold that says when to stop, revert, disable a flag, restore config, or escalate.

Do not accept runtime closure only because a model or builder says `done`. Runtime acceptance needs a readback/smoke result observed by the current agent and logs from every touched service when available, or an explicit handoff when access is unavailable.

Do not require runtime logs for docs-only, skill-only, local refactor, or test-only work with no runtime impact; record Ship Readiness as `N/A` with a reason.

If the agent cannot access runtime logs, production dashboards, or the live system, record the exact handoff instead of pretending the gate was run:

```md
Runtime gate handoff:
- Smoke/event:
- Log sources to inspect:
- Observation window:
- Success threshold:
- Rollback threshold:
- Who must run it:
```

## Dangerous Actions

Do not perform destructive, privileged, secret-dependent, irreversible, production-deploy, billing, or data-migration actions unless the user explicitly asked for that exact operation and local rules allow it.

When such an action is needed but not allowed, record it under deferred decisions:

```md
Deferred ship action:
- Action:
- Why needed:
- Who must do it:
- Preconditions:
- Verification after action:
```
