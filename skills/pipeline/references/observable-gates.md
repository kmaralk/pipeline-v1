# Observable Gates

Canonical definitions for previously-unobservable gates flagged by the 2026-05-20 audit (F-080..F-083). Each section names what the gate observes and how a reviewer can falsify it.

## F-080 — Resume topic slug normalization

When `pipeline-deep` or `pipeline-hard` Phase -0.5 / -1 parses `<topic>` from a user request to look up `docs/plans/*-<topic>-state.json`, the slug is normalized as follows so resume detection is deterministic.

**Normalization function `slug(s)`:**

1. Lowercase: `s.lower()`.
2. ASCII-fold: replace each character with its closest ASCII equivalent (NFKD decomposition, drop combining marks). Russian-only characters keep their transliterated ASCII form (e.g. `я` → `ya`, `ё` → `yo`, `й` → `y`). Non-letter/non-digit characters become `-`.
3. Collapse runs of `-` to a single `-`.
4. Strip leading/trailing `-`.

**Regex shape of the result:** `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase kebab-case, ASCII-only).

The glob used for state detection is then `docs/plans/*-{slug}-state.json` (date prefix wildcard, slug-suffix literal).

Examples:
- `"Pipeline Audit Fixes"` → `pipeline-audit-fixes`
- `"external review v3"` → `external-review-v3`
- `"feature/foo"` → `feature-foo`

## F-081 — Semantic fallback (Phase 1.5 Step B) callable definition

The "small AI call" semantic fallback in Phase 1.5 is:

- **Callable:** current-model prompt template (no separate subagent) — runs in the same orchestrator session that is processing Phase 1.5.
- **Template:**

  ```
  You are deciding whether a context-driven practice applies to this task.

  Practice id: <id>
  Practice semantic description: <semantic>

  Task signals:
  - Requirements brief: <Phase 1 brief>
  - Affected surfaces: <list>
  - Selected files (if Phase 2 has run): <list>

  Return JSON: {"applies": true|false, "named_risk": "<one sentence or null>", "confidence": "high|medium|low"}
  ```

- **Expected output schema:** `{"applies": bool, "named_risk": str | null, "confidence": "high" | "medium" | "low"}`.

- **State storage:** under `phase_1_5_practices.semantic_checks` as a list of `{"id": <practice-id>, "result": <above-JSON>}` entries. The `semantic_checks_run` counter increments by 1 per practice evaluated.

Practice activates if `applies=true` AND `named_risk != null` (per F-047 named-risk requirement).

## F-082 — Hard "When analysis is needed" trigger

Hard mode Phase 2 (Boardroom Context) previously said "when analysis is needed, launch parallel context gathering". The trigger conditions are now explicit:

**For hard mode the boardroom phase always runs** — there is no "analysis is needed" guard. Hard mode is opted into for tasks that warrant the full advanced workflow, and boardroom evidence is part of that contract. Lite and deep retain the analysis-conditional behavior.

## F-083 — `<base>` definition for git diff scope

When any rule says `git diff --name-only <base>...HEAD` or `git diff <base>...HEAD`:

- **`<base>` is the merge-base of `HEAD` and the integration branch** (`main` by default; the project's configured default branch otherwise).
- Resolve with `git merge-base HEAD main` (or the configured default branch); if no merge-base exists, fall back to the working diff against the index.
- The intent is "show me everything this branch added on top of the integration branch", not "everything since the last commit".
