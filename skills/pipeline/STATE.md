# Pipeline Skill State

Public maintenance index, not runtime instruction.

This file documents the portable package shape for the public snapshot. It does
not contain private development history, raw transcripts, local machine paths, or
active-copy sync records.

## Package Shape

- `skills/pipeline/`
- `skills/pipeline-lite/`
- `skills/pipeline-deep/`
- `skills/pipeline-hard/`
- `scripts/validate_pipeline_package.py`

## Runtime Entry Points

- `pipeline`: route to the right mode.
- `pipeline-lite`: small and already-clear local technical work.
- `pipeline-deep`: unclear, broad, product, architecture, or research-heavy work.
- `pipeline-hard`: advanced workflow for high-value tasks that need stronger
  orchestration and review.

## Public Snapshot Policy

Do not add:

- raw logs, transcripts, browser/network output, or model response dumps;
- machine-local paths or active-copy state;
- auth state, cookies, tokens, private keys, or environment dumps;
- generated caches such as `__pycache__` or `.pytest_cache`;
- third-party skills without license and provenance notes.

Use `README.md`, `SECURITY.md`, tests, and the package validator for public
release readiness.
