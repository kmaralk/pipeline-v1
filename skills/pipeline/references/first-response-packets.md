# First Response Failure Packets

Canonical reference for the First Response Failure Packets list. This file is the single source of truth: when a packet's wording, trigger, or applicability changes, update here first.

F-020 dedup executed 2026-06-09: each SKILL.md (router `pipeline`, lite, deep, hard) now carries only packet names + trigger one-liners + a pointer to this file. Full canonical wording and minimum fields live here. Mode-specific trigger deltas stay inline in the mode's SKILL.md and are mirrored in §Mode-specific deltas below.

## Trigger × Required Packet × Minimum Fields × Skip Condition

| Trigger | Required packet | Minimum fields | Skip condition |
|---|---|---|---|
| User-facing UI / web routes / forms | Browser evidence packet | route/page, viewport (mobile+desktop or skip reason), steps, expected visible result, negative check, evidence route | backend-only with no visible user surface |
| Draft/prompt/plan structurally wrong | Plan repair packet | edit source artifact, regenerate downstream from cleaner source | small clarification fits in chat |
| Medium/high-risk plan, broad refactor, launch/pricing/contract/migration, Codex-heavy/autonomous | Premortem plan review packet | failure-frame, plan holes, accepted mitigations, deferred holes, residual risk | low-risk reversible local change |
| Non-trivial skill/prompt/routing/model/agent-workflow change | Skill-change eval packet | clean-context scenarios, scorecard evidence, metrics decision, simplifier pass result | doc-only edit with no behavior change |
| existing large, old, or cross-cutting codebase; stale docs/specs conflict with code | Code Routing Map packet | read `skills/pipeline/references/code-routing-map.md`; build or refresh the smallest current-code map with file paths, symbols, entrypoints, contracts, tests, and flow/domain terms; when stale docs/specs conflict with code, trust code and refresh only affected map lines | skip it for small local work when targeted `rg`, nearby code, and nearby tests already identify the change |
| Repeated command/tool/MCP/handoff failures | Tool failure recipe packet | known-good command, cwd, failure mode, required env | single transient failure |
| AI prompt/output regression | Trace evidence packet | raw artifact: prompt/context/tool calls/model output/logs/trace IDs | unrelated to AI behavior |
| Producer/consumer surfaces split | Contract handoff packet | producer files, consumer files, contract delta, compatibility, acceptance handshake, verification commands | single-owner change |
| Large or risky AI-generated implementation review | Review evidence packet | blockers first, per-finding reproduction evidence (file path, diff hunk, command output, failing test, log, trace) | small reversible diff |
| Agent execution from chat | Durable task brief packet | context, MVP scope, explicit deferrals, questions, contracts, acceptance checks | task fits in a single message |
| Open questions persist past phase boundary | Questions ledger packet | blocking / answered / deferred status | no unresolved questions |
| Noisy tool requests | Context budget packet | allowed files/docs/skills/MCP/tools list; `rg`, summarized logs, exact file refs | task already context-tight |

## Packet Details (canonical wording)

Include the relevant first response packets before implementation steps when a trigger appears:

- Browser evidence packet: for user-facing frontend/UI/page/form/browser-route/user-journey work, include route/page, viewport: mobile and desktop or skip reason, steps, expected visible result, negative check, and evidence route: Playwright / agent-browser / project e2e / documented manual browser evidence. If automation is unavailable, include a Manual fallback record with exact route, viewport, steps, observed visible result, unchecked items, and residual risk.
- AI Minimalism Guardrails packet: for AI-generated implementation, custom infrastructure logic, oversized diffs, or context-rule changes, read `skills/pipeline/references/ai-minimalism.md` and capture the Minimal Diff Packet, Reuse-Before-Build, Post-Green Simplify Pass, or Context Rule Audit parts that apply.
- Pipeline-update packet: when the user says `pipeline-update`, `pipeline update`, or asks to improve this skill from a post, link, third-party skill, agent failure, or reusable practice, read `skills/pipeline/references/skill-update-intake.md` before choosing `pipeline-lite`, `pipeline-deep`, or `pipeline-hard`. This is not a fourth pipeline mode.
- Plan repair packet: if a draft, prompt, or plan is structurally wrong, edit source artifact and regenerate/re-review from that cleaner source. Follow-up chat is only for small clarifications.
- Premortem plan review packet: for medium/high-risk plans, broad feature/refactor work, launch/pricing/contract/migration decisions, or Codex-heavy/autonomous execution, include a short failure-frame plan check before committing to implementation. Read `skills/pipeline/references/premortem-plan-review.md`. It is not a separate mode. The selected `run_control` remains sticky.
- Skill-change eval packet: for non-trivial skill, prompt, routing, model, or agent-workflow changes, name clean-context scenarios, scorecard evidence, and the metrics decision; before accepting skill PRs, run a simplifier pass and record kept, moved, deferred, and removed items.
- Code Routing Map packet: for an existing large, old, or cross-cutting codebase, or when stale docs/specs conflict with code, read `skills/pipeline/references/code-routing-map.md`; build or refresh the smallest current-code map with file paths, symbols, entrypoints, contracts, tests, and flow/domain terms; trust code over stale docs/specs and refresh only affected map lines; skip it for small local work and use targeted `rg`, nearby code/tests, and focused acceptance.
- Tool failure recipe packet: after repeated command or tool syntax/env/context failures, record known-good command, cwd, failure mode, and required env in a report/runbook. After two materially similar failures, stop repeating the same route; capture failure mode, cwd, known-good command or reset decision, required env/config, and chosen fallback.
- Trace evidence packet: for AI prompt/output regressions, name the raw artifact first - prompt/context/tool calls/model output/logs/trace IDs - before prompt or skill edits; no persistent trace collection unless separately designed.
- Contract handoff packet: when producer/consumer surfaces split, create a Downstream Contract Handoff naming producer files, consumer files, contract delta, compatibility, and acceptance handshake; give consumer agents the same handoff.
- Review evidence packet: for large or risky AI-generated implementation reviews, lead with blockers first and require reproduction evidence for each finding: file path, diff hunk, command output, failing test, log, or trace.
- Durable task brief packet: before agent execution from chat, write a durable task brief with context, MVP scope, explicit deferrals, questions, contracts, and acceptance checks; give agents the artifact, not only chat history.
- Questions ledger packet: open questions require an explicit Questions section or durable artifact with blocking, answered, or deferred status; resume only when blockers are resolved or deferred with residual risk.
- Context budget packet: for noisy tool requests, set a context budget and load only relevant files, docs, skills, MCP servers, and tools; prefer targeted `rg`, concise command output, summarized logs, and exact file references.

## Mode-specific deltas

- Router `pipeline` additionally carries: AI Minimalism Guardrails packet, Pipeline-update packet (they trigger before any mode is selected).
- Lite premortem trigger variant (kept inline in `pipeline-lite/SKILL.md`): for medium/high-risk plans, behavior changes, multi-file work, contract/migration/user-facing changes, or Codex-heavy/autonomous execution, include a short failure-frame plan check before implementation. Read `skills/pipeline/references/premortem-plan-review.md`. It is not a separate mode; the selected `run_control` remains sticky.
- Hard additionally enforces: Premortem plan review packet for any Codex-heavy/autonomous execution regardless of risk size.
- The Browser evidence first-task-brief template (route/page: / viewport: / steps: / expected visible result: / negative check: / evidence route:) stays inline in router `Routing Output Requirements` and lite Phase 2, because it is filled verbatim at those workflow points.
