# Pipeline Packaging And Portability

Use this reference when changing, copying, installing, or auditing the `pipeline` skill family.

## Compatibility Rule

Codex and Claude skill surfaces are compatible in concept, not identical in tooling, metadata, or sync behavior.

Shared concepts:
- `SKILL.md` frontmatter with `name` and `description`;
- concise body instructions plus progressive-disclosure references;
- bundled references, eval assets, scripts, and templates;
- local tests that prevent silent instruction drift.

Differences to preserve:
- Codex may use `agents/openai.yaml` for UI metadata and default prompts;
- Claude Code may expose different plugins, MCP servers, browser tooling, and slash commands;
- active copies can be real directories or symlinks depending on the local setup;
- a tool listed in documentation may still be unavailable, unauthenticated, or inappropriate for the current task.

When copying between agents, do not assume one surface's metadata, plugin names, or MCP syntax automatically works on the other. Keep the shared workflow stable and document surface-specific differences.

## Package validation

Before claiming a `pipeline` packaging change is done, run:

```bash
PIPELINE_KIT_ROOT="${PIPELINE_KIT_ROOT:-$PWD}"
CODEX_SKILLS_ROOT="${CODEX_SKILLS_ROOT:-$HOME/.codex/skills}"
CLAUDE_SKILLS_ROOT="${CLAUDE_SKILLS_ROOT:-$HOME/.claude/skills}"
PIPELINE_BUNDLE_SKILLS_ROOT="${PIPELINE_BUNDLE_SKILLS_ROOT:-$PIPELINE_KIT_ROOT/../pipeline-bundle/skills}"

python3 scripts/validate_pipeline_package.py \
  --repo "$PIPELINE_KIT_ROOT" \
  --compare-root "$CODEX_SKILLS_ROOT" \
  --compare-root "$CLAUDE_SKILLS_ROOT" \
  --compare-root "$PIPELINE_BUNDLE_SKILLS_ROOT"
```

The validator checks:
- required `pipeline`, `pipeline-lite`, `pipeline-deep`, and `pipeline-hard` files;
- YAML frontmatter name/description;
- `agents/openai.yaml` interface fields and `$skill-name` default prompt;
- required references and eval assets;
- optional `scripts/`, `assets/`, and safe committed `config/` files when they exist;
- active-copy sync against the canonical pipeline package `skills` tree.

Run the PR-F pytest file as the regression guard:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_pipeline_pr_f_packaging_portability.py -q
```

## Required Package Shape

Each pipeline-family skill must keep:
- `SKILL.md`;
- `agents/openai.yaml`;
- any referenced files reachable from the skill body.

The shared `pipeline` folder must keep:
- `references/shared.md`;
- `references/tool-inventory.md`;
- `references/practices-index.md`;
- `references/practices-full.md`;
- `references/claude-codex-orchestration.md`;
- `references/collaboration-profiles.md`;
- `references/autonomy-levels.md`;
- `references/orchestration.md`;
- `references/packaging.md`;
- `references/code-routing-map.md`;
- `references/ai-minimalism.md`;
- `references/run-control-inheritance.md`;
- `references/premortem-plan-review.md`;
- `references/skill-update-intake.md`;
- `references/source-grounding.md`;
- `references/review-quality-lenses.md`;
- `references/ship-readiness.md`;
- `evals/behavioral_eval_set.json`;
- `evals/eval_set.json`;
- `evals/scorecard-template.md`.

If a reference is renamed, moved, or deleted, update every pointer and run the validator before syncing active copies.

## Optional bundled resources

Do not create empty optional directories. Add them only when there is a concrete file with a clear use.

- Use `scripts/` for repeatable deterministic operations, fragile command sequences, or code agents would otherwise rewrite.
- Use `assets/` for templates or media consumed by the final output, such as report templates, slide templates, frontend starter files, icons, fonts, or images.
- Use committed `config/` only for safe examples or non-secret defaults. Do not store real tokens, passwords, private paths, or auth material in the skill bundle.
- Do not commit runtime `cache/` data. Use `/tmp` for scratch work and `docs/reports/evidence/` for durable evidence.

When `scripts/`, `assets/`, or safe committed `config/` files are added under a pipeline-family skill, the package validator must compare those files across canonical and active copies before the update is called portable.

## Third-party skill security review

Do not install or copy a third-party skill directly from GitHub or a ZIP into active skill roots until it has been reviewed.

Review checklist:
- inspect `SKILL.md` frontmatter and trigger description for over-broad invocation;
- list scripts, binaries, shell commands, network calls, and file writes;
- identify Hidden tool assumptions: MCP names, plugins, browser tools, env vars, credentials, private paths, or remote services the skill silently expects;
- check for destructive, privileged, secret-dependent, or irreversible actions;
- verify licenses and provenance when the skill includes copied assets or scripts;
- prefer installing into a temporary folder first, then run validation before syncing active copies.

If the review finds risk but the skill is still useful, keep it out of active roots and record the decision in the implementation report or project memory.

## Sync Rule

Canonical source for the pipeline family is `$PIPELINE_KIT_ROOT/skills`.

After changing canonical skill files, sync the pipeline family into:
- `$CODEX_SKILLS_ROOT`;
- `$CLAUDE_SKILLS_ROOT`;
- `$PIPELINE_BUNDLE_SKILLS_ROOT`.

Then run package validation and targeted PR-F tests. Do not say the portable package is ready while canonical and active copies differ.
