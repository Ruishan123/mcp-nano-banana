from __future__ import annotations

from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_PATH = ROOT / "pyproject.toml"
GITIGNORE_PATH = ROOT / ".gitignore"
LICENSE_PATH = ROOT / "LICENSE"
CI_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "ci.yml"


def test_gitignore_covers_local_secrets_and_dev_artifacts() -> None:
    gitignore = GITIGNORE_PATH.read_text(encoding="utf-8")

    for expected in [
        ".env",
        ".venv/",
        "__pycache__/",
        ".pytest_cache/",
        ".tmp/",
        ".tmp_pytest/",
        ".test_tmp/",
        "dist/",
        "build/",
    ]:
        assert expected in gitignore


def test_project_metadata_supports_public_distribution() -> None:
    data = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    project = data["project"]

    assert project["name"] == "mcp-nano-banana"
    assert "license" in project
    assert "classifiers" in project
    assert "keywords" in project
    assert "mcp-nano-banana" in project["scripts"]


def test_repository_includes_open_source_license() -> None:
    license_text = LICENSE_PATH.read_text(encoding="utf-8")

    assert "MIT License" in license_text


def test_repository_includes_ci_workflow_for_push_and_pull_request() -> None:
    workflow = CI_WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "push:" in workflow
    assert "pull_request:" in workflow
    assert "python-version: [\"3.11\", \"3.12\", \"3.13\"]" in workflow
    assert "pip install .[dev]" in workflow
    assert "python -m pytest" in workflow
    assert "python -m hatchling build" in workflow
