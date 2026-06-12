# Pipeline Skill Scorecard

Use this template for non-trivial changes to `pipeline`, prompts, routing rules, or agent workflow instructions.

## Change

- Scope:
- Files changed:
- Eval set:
- Reviewer or runner:

## Scenario Results

| Scenario ID | Result | Evidence | Notes |
|---|---|---|---|
| `<id>` | pass/fail/not run | command, transcript, diff, or manual observation | |

Treat `not run` as residual risk unless it is explicitly out of scope.

## Quality Axes

Score each axis from 0 to 2.

| Axis | Score | What 2 Means | Evidence |
|---|---:|---|---|
| Trigger Precision | | Correctly triggers on intended requests and rejects near-misses. | |
| Instruction Following | | Follows the body of the skill, not only frontmatter or nearby chat context. | |
| Context Efficiency | | Loads only relevant files and avoids bloating always-loaded instructions. | |
| Verification Strength | | Uses deterministic checks, behavioral scenarios, and residual-risk notes. | |
| Human Usability | | Explains decisions plainly enough for the user to approve or reject. | |

## Clean-context eval

- Context given to evaluator:
- Context intentionally withheld:
- Result:

## A/B comparison

Use when practical.

- Baseline: old vs new / skill vs no-skill
- Difference observed:
- Decision:

## Trace-driven refinement

If any scenario failed, inspect the raw artifact before editing:

- Artifact inspected: prompt / transcript / command output / eval result / diff / log / trace
- Failure cause:
- Change made from evidence:

## Simplifier pass

Before accepting the skill change:

- Kept:
- Shortened:
- Moved to references/templates:
- Deferred:
- Removed:

## Residual Risk

- Unrun scenarios:
- Weak evidence:
- Follow-up needed:
