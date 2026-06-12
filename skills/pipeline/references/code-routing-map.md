# Code Routing Map

Use this reference when an existing codebase is large, old, poorly documented, or the requested change crosses several user flows, domains, modules, services, or teams.

Do not create a map for small local work, typo fixes, single-file bugs, or tasks where targeted `rg` plus nearby tests already locate the right code.

## Purpose

A code routing map helps the agent find the relevant current code. It is not a separate product spec and it must not become a second source of truth.

Default rule: code is the source of truth. The map should route the agent to the current code, tests, contracts, and entrypoints that matter for the task.

If the map conflicts with code, trust code, mark the map stale, and refresh only the affected part before relying on it.

## First-Response Shortcut

- Large/old/cross-cutting existing codebase: say `Use Code Routing Map`, then build or refresh the smallest current-code map before planning implementation.
- Stale docs/specs conflict with code: trust current code/tests, mark the doc or map stale, and refresh only the affected map lines.
- Small local work: say `Skip Code Routing Map`, then use targeted `rg`, nearby code/tests, and focused regression/verification.

## When To Build Or Refresh One

Build or refresh a small map when:
- the task asks for a cross-cutting change in an existing product;
- old specs, PRDs, READMEs, or comments may be stale;
- the agent would otherwise scan a large part of the repository to find one flow;
- user flows, domain terms, APIs, workers, or UI routes are spread across multiple areas;
- multiple agents need the same bounded context for implementation or review.

Skip it when the next implementation step is already obvious and reviewable without extra documentation.

## Minimum Shape

Keep the map short and generated from current code.

Include only what helps routing:
- user or operator flow name;
- domain terms and important invariants;
- file paths, symbols, flows, contracts, tests, and known entrypoints;
- command, route, event, job, API, or UI entrypoint that starts the flow;
- known gaps, stale docs, or unverified assumptions.

Every non-obvious claim should cite a file path, symbol, test, command output, or runtime evidence. Avoid long prose that future agents will not read.

## Placement

Prefer an existing project memory, runbook, or architecture note if the project already has one.

If no local convention exists, use one of:
- `docs/agent-memory/code-routing-map.md` for a small shared index;
- `docs/agent-memory/<flow>-map.md` for one important flow;
- a focused runbook when the map is mostly operational steps.

Do not put project-specific maps into the global pipeline skill. The skill only defines when and how to make them.

## Refresh Rule

Before using an old map:
1. Check the cited files still exist.
2. Check the key entrypoints/tests still match the task.
3. Update only stale lines needed for the current task.
4. Record residual risk if a cited area could not be verified.

Do not block small safe fixes only because a full map is missing. Build the smallest map that prevents the current context miss.
