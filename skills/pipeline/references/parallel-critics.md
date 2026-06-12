# Parallel Critics

Canonical reference for the Parallel Critics review layer. Used by `pipeline-deep` Phase 7 Review Gate and `pipeline-hard` Phase 7.5 Review Gate.

F-023 dedup executed 2026-06-09: this file is the canonical single source for the critics protocol. `pipeline-deep` and `pipeline-hard` SKILL.md carry only the activation gate and a pointer here.

## Activation

Only when the user explicitly selects pun ("Parallel Critics") in the Review Menu. Default: not activated.

## Task class detection

Read task class from Phase 1 brief: `bugfix` | `feature` | `refactor` | `infra`. Infra triggers on touched paths: `*.tf`, `systemd/*`, `docker-compose*`, `.github/workflows/*`, `CLAUDE.md`.

## Presets

See `shared.md §Parallel Critics Presets` for the canonical preset table. Default at activation: `recommended` (tests + security + arch).

`critics-custom` Review Menu choice → show 8 roles as checklist for manual selection.

## Dispatch contract

REQUIRED sub-skill: `superpowers:dispatching-parallel-agents`.

- Each critic = one subagent on `claude-haiku-4-5-20251001`.
- Max 5 concurrent; 6+ runs in two waves.
- Each critic receives: `role`, `focus`, task class, changed files list, `git diff`, relevant design-doc sections.
- Strict JSON output contract:

```json
{
  "findings": [
    {
      "severity": "critical | normal | nit",
      "file": "<repo-relative path>",
      "line_range": "N-M | null",
      "issue": "<one sentence>",
      "suggested_fix": "<concrete, copy-pasteable if possible>"
    }
  ]
}
```

Critics that fail/timeout are logged and skipped; layer continues best-effort with survivors.

## Aggregate + apply (finalizer)

Finalizer runs on the current session model (Sonnet/Opus), NOT Haiku.

- Merge findings by `(file, line_range, severity)` to dedup.
- Sort by severity: critical → normal → nit.
- Apply changes under Hard Rules:
  1. Total diff size MUST NOT grow by more than 30% of this round's delta. Over 30% → escalate to user.
  2. Each `critical` either closed or motively rejected via Accept-or-Argue (`superpowers:receiving-code-review`).
  3. Each finding tracked: `finding_id → changed_lines`.
  4. After each apply, mini-self-check on Haiku: "did this apply create a new critical?" If yes → revert, escalate the original finding.

## Severity-based re-check

| Severity | Max rounds | Between rounds |
|---|---|---|
| critical | 3 | Same critics, `focus: critical_only` sweep — verify closure, detect new critical |
| normal | 1 | Lightweight sweep — verify closures still hold |
| nit | 0 | Fire-and-forget, no re-check |

Stop when: `findings[critical] == []` after a round, OR max rounds hit.

## Escalation (stop conditions)

- Round 3 on critical does not converge → show user list of unclosed critical, options: (a) extra round manually / (b) accept as residual risk / (c) abort.
- Hard Rule #1 triggered (>30% growth) → show summary, options: (a) accept / (b) revert last round / (c) re-pick critics.
- New critical created by apply (Hard Rule #4) → auto-revert, log in residual risks.

## State log

After critics layer completes, write under current phase:

```json
{
  "critics": {
    "selected": ["<role_ids>"],
    "rounds": [
      {
        "round": 1,
        "findings_count": {"critical": 0, "normal": 0, "nit": 0},
        "closed":         {"critical": 0, "normal": 0, "nit": 0},
        "residual":       {"critical": 0, "normal": 0, "nit": 0}
      }
    ],
    "status": "completed | escalated"
  }
}
```

Atomic write, commit `"pipeline: critics layer completed"`.
