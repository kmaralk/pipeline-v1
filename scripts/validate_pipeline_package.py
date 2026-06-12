#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

import yaml


PIPELINE_SKILLS = (
    "pipeline",
    "pipeline-lite",
    "pipeline-deep",
    "pipeline-hard",
)

OPTIONAL_BUNDLED_DIRS = (
    "scripts",
    "assets",
    "config",
)

DISALLOWED_BUNDLED_DIRS = (
    "cache",
)

REQUIRED_PIPELINE_FILES = (
    "pipeline/SKILL.md",
    "pipeline/STATE.md",
    "pipeline/references/shared.md",
    "pipeline/references/tool-inventory.md",
    "pipeline/references/practices-index.md",
    "pipeline/references/practices-full.md",
    "pipeline/references/claude-codex-orchestration.md",
    "pipeline/references/collaboration-profiles.md",
    "pipeline/references/autonomy-levels.md",
    "pipeline/references/autonomy-safeguards.md",
    "pipeline/references/orchestration.md",
    "pipeline/references/test-adequacy-review.md",
    "pipeline/references/branch-worktree-policy.md",
    "pipeline/references/oracle-routing.md",
    "pipeline/references/packaging.md",
    "pipeline/references/contract-handoff.md",
    "pipeline/references/browser-acceptance.md",
    "pipeline/references/worktree-agent-isolation.md",
    "pipeline/references/report-status-evidence.md",
    "pipeline/references/idea-to-ship-gates.md",
    "pipeline/references/code-routing-map.md",
    "pipeline/references/ai-minimalism.md",
    "pipeline/references/run-control-inheritance.md",
    "pipeline/references/premortem-plan-review.md",
    "pipeline/references/skill-update-intake.md",
    "pipeline/references/source-grounding.md",
    "pipeline/references/review-quality-lenses.md",
    "pipeline/references/ship-readiness.md",
    "pipeline/evals/eval_set.json",
    "pipeline/evals/behavioral_eval_set.json",
    "pipeline/evals/scorecard-template.md",
    "pipeline/evals/metrics.md",
    "pipeline-lite/SKILL.md",
    "pipeline-deep/SKILL.md",
    "pipeline-hard/SKILL.md",
)

SYNCED_RELATIVE_PATHS = REQUIRED_PIPELINE_FILES + tuple(
    f"{skill}/agents/openai.yaml" for skill in PIPELINE_SKILLS
)


def read_text(path):
    return path.read_text(encoding="utf-8")


def frontmatter(path):
    text = read_text(path)
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


def check_openai_yaml(path, skill_name):
    data = yaml.safe_load(read_text(path)) or {}
    interface = data.get("interface", {})
    if not isinstance(interface, dict):
        return [f"{path}: interface must be a mapping"]

    errors = []
    for field in ("display_name", "short_description", "default_prompt"):
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}: missing interface.{field}")

    short_description = interface.get("short_description", "")
    if isinstance(short_description, str) and not 25 <= len(short_description) <= 64:
        errors.append(f"{path}: short_description must be 25-64 chars")

    default_prompt = interface.get("default_prompt", "")
    if isinstance(default_prompt, str) and f"${skill_name}" not in default_prompt:
        errors.append(f"{path}: default_prompt must mention ${skill_name}")

    return errors


def iter_synced_relative_paths(canonical_root):
    yielded = set()
    for relative in SYNCED_RELATIVE_PATHS:
        yielded.add(relative)
        yield relative

    for skill in PIPELINE_SKILLS:
        for directory in OPTIONAL_BUNDLED_DIRS:
            root = canonical_root / skill / directory
            if not root.exists():
                continue
            for path in sorted(item for item in root.rglob("*") if item.is_file()):
                relative = path.relative_to(canonical_root).as_posix()
                if relative not in yielded:
                    yielded.add(relative)
                    yield relative


def validate_root(root):
    errors = []

    for relative in REQUIRED_PIPELINE_FILES:
        path = root / relative
        if not path.exists():
            errors.append(f"{path}: missing file")

    for skill in PIPELINE_SKILLS:
        skill_md = root / skill / "SKILL.md"
        if skill_md.exists():
            try:
                data = frontmatter(skill_md)
            except ValueError as exc:
                errors.append(f"{skill_md}: {exc}")
            else:
                for field in ("name", "description"):
                    value = data.get(field)
                    if not isinstance(value, str) or not value.strip():
                        errors.append(f"{skill_md}: missing {field}")
                if data.get("name") != skill:
                    errors.append(f"{skill_md}: name must be {skill}")

        openai_yaml = root / skill / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            errors.append(f"{openai_yaml}: missing file")
        else:
            errors.extend(check_openai_yaml(openai_yaml, skill))

        for directory in DISALLOWED_BUNDLED_DIRS:
            path = root / skill / directory
            if path.exists():
                errors.append(f"{path}: runtime-only directory must not be bundled")

    packaging = root / "pipeline" / "references" / "packaging.md"
    if packaging.exists():
        text = read_text(packaging)
        for snippet in (
            "Package validation",
            "Optional bundled resources",
            "Third-party skill security review",
            "Hidden tool assumptions",
            "agents/openai.yaml",
        ):
            if snippet not in text:
                errors.append(f"{packaging}: missing {snippet}")

    return errors


def validate_sync(canonical_root, compare_roots):
    errors = []
    synced_paths = tuple(iter_synced_relative_paths(canonical_root))
    for compare_root in compare_roots:
        for relative in synced_paths:
            source = canonical_root / relative
            target = compare_root / relative
            if not target.exists():
                errors.append(f"{target}: missing synced file")
                continue
            if read_text(source) != read_text(target):
                errors.append(f"{target}: differs from {source}")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate the pipeline skill package.")
    parser.add_argument("--repo", required=True, help="Path to pipeline package repository")
    parser.add_argument(
        "--compare-root",
        action="append",
        default=[],
        help="Additional active skills root to compare against repo/skills",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    canonical_root = repo / "skills"
    errors = []

    if not canonical_root.exists():
        errors.append(f"{canonical_root}: missing skills directory")
    else:
        errors.extend(validate_root(canonical_root))

    compare_roots = [Path(root).resolve() for root in args.compare_root]
    for root in compare_roots:
        errors.extend(validate_root(root))
    if canonical_root.exists():
        errors.extend(validate_sync(canonical_root, compare_roots))

    if errors:
        for error in errors:
            print(error)
        return 1

    print("OK pipeline package validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
