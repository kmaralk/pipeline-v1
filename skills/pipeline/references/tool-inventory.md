# Tool Inventory

Compact runtime inventory for routing decisions. This public snapshot does not
assume any private MCP server, plugin, browser profile, or local helper.

## Baseline Tools

- Local shell commands may be available depending on the agent host.
- `rg` is preferred for file and text search when present.
- `git` is expected for repository inspection.
- `python3` is expected for package validation.

## Optional Integrations

The pipeline skills may mention optional integrations such as browser automation,
GitHub tooling, secondary model review, or documentation lookup. Availability is
environment-specific. Verify each tool at runtime before relying on it.

See `skills/pipeline/references/optional-integrations.md` and the repository
root `OPTIONAL-INTEGRATIONS.md` for public install links, private-hook fallback
rules, and redistribution guidance.

## Safety Rule

Tool availability is not permission. Do not read, print, store, or publish
cookies, browser storage, auth headers, tokens, private keys, environment dumps,
or private transcripts.
