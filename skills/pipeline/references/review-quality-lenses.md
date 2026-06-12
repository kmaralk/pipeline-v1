# Review Quality Lenses

Use this when reviewing a plan, spec, code diff, generated implementation, or cross-agent handoff.

This is a minimum floor, not a narrow checklist.

Review must cover at least:

- correctness;
- readability;
- architecture;
- security;
- performance.

Then add any task-specific risks the context suggests. Examples: UX, migrations, data, compatibility, observability, cost, legal, accessibility, reliability, privacy, i18n, developer experience, rollout, support, test adequacy, and operational recovery.

Do not stop at these five if the task requires more. Do not force every example onto every task. Pick the extra lenses from the actual scope, touched files, product surface, and failure modes.

## How To Use

For each active lens, ask:

- what would break in real use?
- what evidence proves it is okay?
- what is blocking versus acceptable residual risk?

For code review, lead with blockers and reproduction evidence. For plan/spec review, lead with missing decisions, unclear contracts, unverifiable acceptance criteria, and scope drift.

## Finding Verification Gate

Before promoting a code-review finding to the main report, quote the specific code line that supports it. Include `file:line`, the short quoted line or symbol source, and a confidence score.

If you cannot quote the motivating line, lower confidence and keep the item out of the blocker list unless it is a P0 risk. Do not present memory, style preference, or pattern suspicion as a verified finding.

## Cross-Agent Use

When Claude Code reviews Codex, or Codex reviews Claude Code, tell the reviewer:

```text
Review must cover at least correctness, readability, architecture, security, and performance. Then add any task-specific risks the context suggests, such as UX, migrations, data, compatibility, observability, cost, legal, accessibility, reliability, privacy, rollout, support, or test adequacy. Do not stop at these five if this task needs more.
```

The point of cross-agent review is to catch model-family blind spots, not to re-run the same generic checklist. Ask the reviewer to add context-specific lenses before giving findings.

## Output Shape

Use a compact form unless the task is high-risk:

```md
Review lenses used:
- Minimum: correctness, readability, architecture, security, performance
- Context-specific: <extra lenses chosen for this task>

Findings:
1. <severity> - <finding>
   - Lens: <lens>
   - Evidence: <file/command/log/trace/manual check>
   - Decision: fix | defer | accept risk | reject
```
