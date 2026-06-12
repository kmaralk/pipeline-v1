# Optional Integrations

This repository does not vendor external skills or third-party tool bundles.
Names such as `superpowers:*`, `agent-browser`, `project-init`, `gh-issues`,
`/codex-security-scan`, and `/cross-check` are runtime hooks.

If an integration is installed, use it. If it is missing, keep the required
behavior and use an equivalent local workflow, then record the fallback and any
residual risk in the task report or final answer.

## Public Sources

| Integration | Used For | Source / Install |
| --- | --- | --- |
| Superpowers | brainstorming, TDD, debugging, worktrees, subagents, code review, verification, branch finish | https://github.com/obra/superpowers. For Claude Code: `/plugin install superpowers@claude-plugins-official` or `/plugin marketplace add obra/superpowers-marketplace` then `/plugin install superpowers@superpowers-marketplace`. For Codex: open `/plugins`, search for `Superpowers`, and install it. |
| agent-browser | browser automation evidence when Playwright/project e2e is not the best route | https://github.com/vercel-labs/agent-browser. Install globally with `npm install -g agent-browser`, then run `agent-browser install`. |
| justdoit | optional execution-pack planning skill for rough repo tasks | https://github.com/serejaris/justdoit/tree/main/skills/justdoit. In Codex, ask `$skill-installer` to install that URL. |
| project-init | optional project bootstrap for GitHub Projects, labels, canonical docs, and agent operating config | https://github.com/serejaris/personal-corp-skills/tree/main/skills/project-init |
| gh-issues | optional GitHub issue workflow for loading context, updating status, and writing final AI session context | https://github.com/serejaris/personal-corp-skills/tree/main/skills/gh-issues |
| codex-plugin-cc | optional Claude Code bridge for asking Codex to review code or delegate tasks | https://github.com/openai/codex-plugin-cc |
| CrossCheck | optional multi-model review loop; the original local setup may differ from upstream | https://github.com/sburl/CrossCheck |
| Codex security guidance | source guidance for local security-scan workflows; not a bundled slash command | https://developers.openai.com/codex/security |

## Local Or Private Equivalents

These hooks were present in the original private working environment, but this
public snapshot does not bundle the local implementation:

| Hook | Replace With |
| --- | --- |
| `/codex-security-scan` | A local security review or secret scan equivalent, ideally adapted from the Codex security guidance above. At minimum run focused review plus `gitleaks` before publishing. |
| `/cross-check` | The upstream CrossCheck project above, your modified local variant, or any independent multi-model review process appropriate for the task risk. |

## Publication Rule

Do not copy third-party skills into this public repository unless their license
allows redistribution and attribution is preserved. Prefer links and install
instructions here, and keep any private archival snapshots outside this repo.
