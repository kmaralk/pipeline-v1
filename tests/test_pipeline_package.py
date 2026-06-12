import subprocess
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
PIPELINE_SKILLS = ("pipeline", "pipeline-lite", "pipeline-deep", "pipeline-hard")


def test_pipeline_package_validator_accepts_public_snapshot():
    result = subprocess.run(
        [
            "python3",
            str(REPO_ROOT / "scripts" / "validate_pipeline_package.py"),
            "--repo",
            str(REPO_ROOT),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert result.returncode == 0, result.stdout
    assert "OK pipeline package validation passed" in result.stdout


def test_pipeline_skills_have_openai_metadata():
    missing = []
    for skill in PIPELINE_SKILLS:
        path = SKILLS_ROOT / skill / "agents" / "openai.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        interface = data.get("interface", {})
        for field in ("display_name", "short_description", "default_prompt"):
            value = interface.get(field)
            if not isinstance(value, str) or not value.strip():
                missing.append(f"{path}: missing interface.{field}")
        if f"${skill}" not in interface.get("default_prompt", ""):
            missing.append(f"{path}: default_prompt must mention ${skill}")

    assert not missing, "\n".join(missing)


def test_public_snapshot_excludes_private_artifact_dirs():
    forbidden = [
        ".claude",
        ".codex",
        "__pycache__",
        ".pytest_cache",
        "docs/reports/evidence",
    ]
    tracked_paths = []
    for path in REPO_ROOT.rglob("*"):
        if any(part in path.parts for part in (".git", ".pytest_cache")):
            continue
        tracked_paths.append(path.relative_to(REPO_ROOT).as_posix())

    violations = [
        path for path in tracked_paths if any(part in path for part in forbidden)
    ]
    assert not violations


def test_optional_integrations_are_documented_not_bundled():
    root_doc = (REPO_ROOT / "OPTIONAL-INTEGRATIONS.md").read_text(encoding="utf-8")
    ref_doc = (
        SKILLS_ROOT / "pipeline" / "references" / "optional-integrations.md"
    ).read_text(encoding="utf-8")

    for expected in (
        "https://github.com/obra/superpowers",
        "https://github.com/vercel-labs/agent-browser",
        "https://github.com/serejaris/justdoit/tree/main/skills/justdoit",
        "https://github.com/serejaris/personal-corp-skills/tree/main/skills/project-init",
        "https://github.com/serejaris/personal-corp-skills/tree/main/skills/gh-issues",
        "https://github.com/openai/codex-plugin-cc",
        "https://github.com/sburl/CrossCheck",
        "https://developers.openai.com/codex/security",
        "/codex-security-scan",
        "/cross-check",
    ):
        assert expected in root_doc
        assert expected in ref_doc

    bundled_external_skill_dirs = [
        SKILLS_ROOT / name
        for name in (
            "brainstorming",
            "test-driven-development",
            "systematic-debugging",
            "agent-browser",
            "project-init",
            "gh-issues",
            "justdoit",
            "codex-security-scan",
            "cross-check",
        )
    ]

    assert not [path for path in bundled_external_skill_dirs if path.exists()]
