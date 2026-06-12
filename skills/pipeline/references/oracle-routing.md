# Oracle Routing Policy

Use this reference when `pipeline-hard` needs an independent research or review oracle.

Manual web oracle is optional, not mandatory. The pipeline should keep moving with the strongest available route unless the user explicitly wants a manual premium oracle.

## Default Route: Local Automated Oracle

Default route: local automated oracle.

Use available local agents and tools without blocking on manual copy/paste:
- Claude Code as independent researcher, reviewer, or plan critic;
- Codex as independent reviewer, planner, executor, or implementation auditor;
- `agent-browser`, Playwright, Exa, GitHub, docs, or web tools for evidence gathering;
- existing MCP/plugin tooling when it is available and relevant.

Research tools collect evidence. The oracle is the independent judgment over the gathered context, plan, or decision.

## Manual Premium Oracle

Use manual premium oracle when the user explicitly asks for it or when the decision is expensive enough that human-directed model choice is worth the delay.

Possible manual premium oracle routes:
- ChatGPT Pro;
- Claude web;
- Gemini;
- a manually curated Repo Prompt handoff;
- a multi-model council.

Manual web oracle should produce a saved memo, link, or pasted summary before consolidation.

## Hybrid Oracle

Hybrid oracle combines local automated research/review with one or more manual premium opinions.

Use it for rare, high-stakes tasks where disagreement between models is useful evidence.

## Browser And Playwright Boundary

Do not treat browser automation as an oracle by itself.

`agent-browser`, Playwright, screenshots, page extraction, and web search are research/evidence tools. They become part of an oracle route only when an independent model uses that evidence to critique a plan, synthesize options, or identify risks.

Opening a page, collecting screenshots, or extracting DOM text is evidence collection only. Oracle completion requires an independent model, agent, or human reviewer to judge that evidence against the question being asked.

## Required Route Record

Record the selected oracle route:
- `local_automated`;
- `manual_premium`;
- `hybrid`;
- `skipped`.

Also record:
- why that route was chosen;
- which tools/models were used;
- which manual oracle was skipped, if skipping it materially affects confidence;
- residual risk if no independent oracle was run.
