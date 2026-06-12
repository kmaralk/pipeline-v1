# Prototype And Trace Practices

Use this reference when a task has uncertain tool syntax, API contracts, risky implementation paths, AI-app debugging, or repeated agent/tool quality failures.

## Prototype Spike

Use a prototype spike before committing to a full implementation when the risky part is uncertain tool syntax, an API contract, a migration shape, a concurrency path, or another risky implementation path.

A prototype spike must be small and disposable:
- prove one question with the shortest local command, fixture, script, or throwaway branch;
- state the spike question before the spike runs;
- record the result as trace evidence in the design or implementation report;
- stop after the uncertainty is resolved, then implement the real change cleanly.

## Trace-Driven AI Debugging

Trace-driven AI debugging applies when the broken surface is an AI feature, agent workflow, prompt chain, model call, tool call, or evaluator.

Debug from raw artifacts first:
- prompt;
- context;
- tool calls;
- model output;
- logs;
- trace IDs.

Name what artifact was inspected before changing prompts or skill instructions.
Name the raw artifact that proves the failure. Do not change prompts, skill text, or tool contracts until the raw artifact is named.

## Tooling Observability

Tooling observability applies when agent quality degradation appears, such as repeated bad tool calls, command syntax loops, missing context, unexpected model output, or reviewer failure.

Inspect actual prompts, generated commands, tool logs, and context handoff before rewriting instructions.

For repeated tool failures, record the known-good command, working directory, required env vars, and failure mode in the report or a focused runbook. Only continuing in chat is not enough after a repeated failure.

After two materially similar failures, stop repeating the same route; capture failure mode, cwd, known-good command or reset decision, required env/config, and chosen fallback before continuing.

## Safety Boundary

Do not add automatic trace collection, persistent prompt storage, or new telemetry infrastructure as part of this practice.

If trace storage is needed, design it separately with explicit handling for sensitive prompts, secrets, or user data.
