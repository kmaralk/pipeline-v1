# Optional Integrations

Pipeline may mention external skills and tools by name. In this public package,
those names are integration hooks, not bundled dependencies.

Runtime rule:

1. If the named integration exists in the current agent environment, invoke it.
2. If it is missing, preserve the required behavior with an equivalent local
   practice.
3. Record the fallback and residual risk when the missing integration affects
   evidence, review depth, security, or release confidence.

Known public sources:

- Superpowers: https://github.com/obra/superpowers
- agent-browser: https://github.com/vercel-labs/agent-browser
- justdoit: https://github.com/serejaris/justdoit/tree/main/skills/justdoit
- project-init: https://github.com/serejaris/personal-corp-skills/tree/main/skills/project-init
- gh-issues: https://github.com/serejaris/personal-corp-skills/tree/main/skills/gh-issues
- codex-plugin-cc: https://github.com/openai/codex-plugin-cc
- CrossCheck upstream: https://github.com/sburl/CrossCheck
- Codex security guidance: https://developers.openai.com/codex/security

Known local hooks in the original environment:

- `/codex-security-scan`: local skill or slash-command implementation, not bundled
- `/cross-check`: local variant may differ from upstream CrossCheck, not bundled

For public redistribution, do not vendor third-party skills here unless the
license allows it and the attribution/license text is preserved.
