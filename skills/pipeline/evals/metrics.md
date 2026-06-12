# Pipeline Eval Metrics

Public snapshot status.

Historical raw responses, scored JSONL files, and private evidence paths are not
included in this repository. Use `behavioral_eval_set.json`, `eval_set.json`,
and `scorecard-template.md` as the public evaluation assets.

Before publishing a release, run a fresh clean-context evaluation and record the
summary here without raw transcripts or local machine paths.

Current public package validation:

- `python3 scripts/validate_pipeline_package.py --repo .`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -q`
