# Source Grounding

Use this when a task depends on an external library, API, SDK, framework, or versioned behavior.

The goal is simple: do not write integration code from memory when the current local version or official documentation can be checked cheaply.

## Triggers

Read this reference when:

- code uses an external library, API, SDK, framework, CLI, protocol, or vendor service;
- the dependency has version-specific behavior;
- the task mentions "latest", "current", "new API", migration guides, or recently changed behavior;
- examples from memory could be stale;
- tests depend on framework behavior that is not obvious from local code.

Skip this for pure local business logic, docs-only edits, or code that only uses already-established project helpers with no new external behavior.

## Evidence Ladder

Use the lightest evidence that answers the question:

1. Local dependency version, lockfile, package manifest, installed source, or generated types.
2. Official docs, changelog, release notes, migration guide, or vendor API reference.
3. Context7 when available, especially for library/API examples and versioned docs.
4. Official web docs or official GitHub repository when Context7 is unavailable or incomplete.
5. If none can be checked, record the assumption and residual risk before implementing.

The evidence ladder is a starting route, not a closed list. Add task-specific source checks when the dependency risk points to auth, billing, rate limits, migrations, browser APIs, security advisories, data formats, deprecations, platform compatibility, or provider-specific behavior. Use the lightest added check that answers a real dependency risk; do not run every example or add inapplicable checks to routine lookups. For a normal task, add no more than 1-2 extra source checks per dependency; if more seem necessary, narrow the research question or split the work.

Prefer official sources over blog posts, snippets, or model memory. Community examples can help only after the official contract is known.

## What To Record

In the spec, plan, report, or acceptance notes, record:

- library/API/framework name;
- detected local dependency version, if available;
- record the source and version when both are available;
- source checked, such as lockfile, official docs, Context7, or official GitHub;
- the specific API pattern or behavior used;
- any unverified assumption or fallback.

Example:

```md
Source grounding:
- Library: Next.js
- Local version: 15.x from package-lock.json
- Source checked: Context7 + official Next.js docs
- Pattern used: middleware auth redirect
- Residual risk: N/A
```

## Context7 Use

Context7 is an optional provider, not a hard dependency. If it is installed, use it for library/API documentation when it can save context or avoid stale examples. If it is unavailable, fall back to local dependency files and official docs.

Do not let Context7 output override the local repo contract, project tests, or official release notes when they conflict. Record the conflict and choose the source that best matches the local version.

## Autonomy

In `A1`/`A2`, ask the user only when the docs reveal a meaningful product, architecture, cost, or security decision.

In `A3`/`A4`, do not stall on documentation lookup if the risk is low. Record the checked source or assumption and continue with the safest local pattern.
