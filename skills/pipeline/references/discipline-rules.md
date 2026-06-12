# Discipline Rules

Canonical single source for the Fresh Baseline Batch-Fix Rules and Final Polish Rules previously inlined in all four SKILL.md files (dedup executed 2026-06-09). When a rule changes, update here only.

## Fresh Baseline Batch-Fix Rules

- Do not answer a structurally wrong plan by adding five clarifications on top. Edit the source artifact, then regenerate or re-review from that cleaner source.
- For skill-change requests, the first response must name clean-context scenarios, scorecard evidence, and the metrics decision.
- If precision, recall, and F1 were not measured, say they were not measured and record residual risk.
- For repeated tool failures, the first response must create or update a durable recipe with known-good command, cwd, failure mode, and required env. After two materially similar failures, stop repeating the same route and capture failure mode, cwd, known-good command or reset decision, required env/config, and chosen fallback.
- For prompt, model-output, or AI JSON regressions, name the raw artifact before proposing a prompt or skill edit.
- For split producer/consumer work, the first response must create a Downstream Contract Handoff before dispatch.
- The handoff must name producer files, consumer files, contract delta, compatibility, acceptance handshake, and verification commands.
- Before dispatching agents, provide file/module ownership, allowed write scope, acceptance criteria, and verification commands; require each implementation agent to report learned context before edits.
- A context pack must include local rules, current plans/status/test-plan, relevant specs, nearby patterns, and verification commands.

## Final Polish Rules

- When escalating from lite to hard, map completed lite evidence into hard mode and continue from the earliest unsatisfied phase.
- If browser evidence is used for oracle review, ask an independent model, agent, or human reviewer to judge the gathered evidence.
- Run a skill simplifier pass and record kept, moved, deferred, and removed items before accepting skill PRs.
- A prototype spike must name the one question it answers and record the spike result in the design or report.
- Adversarial evaluator findings require reproduction evidence: file path, diff hunk, command output, failing test, log, or trace.
- Final user summaries use numbered impact blocks by default, with pros, cons or risks, security, affected behavior, unaffected behavior, and evidence.
- Context packs for implementation agents must include AGENTS or local rules, current plans/status/test-plan, relevant specs, nearby code patterns, and verification commands.
- Ask implementation agents to report what context they learned before changing files.
- For large or risky AI-generated implementation reviews, lead with blockers first and require reproduction evidence for each finding.
- Before agent execution from chat, write a durable task brief with context, MVP scope, explicit deferrals, questions, contracts, and acceptance checks.
- Open questions require an explicit Questions section or durable artifact with blocking, answered, or deferred status.
- For noisy tool requests, set a context budget and load only relevant files, docs, skills, MCP servers, and tools.
