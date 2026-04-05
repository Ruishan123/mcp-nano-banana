from __future__ import annotations

from pathlib import Path


README_PATH = Path(__file__).resolve().parents[1] / "README.md"


def test_readme_keeps_end_user_install_focus() -> None:
    readme = README_PATH.read_text(encoding="utf-8")

    assert "## Quickstart" in readme
    assert "GEMINI_API_KEY" in readme
    assert "[mcp_servers.nano_banana]" in readme
    assert "available after release" in readme
    assert "uvx" in readme
    assert "pipx install git+" in readme


def test_readme_hides_maintainer_local_bootstrap_from_main_flow() -> None:
    readme = README_PATH.read_text(encoding="utf-8")

    assert "server.py" not in readme
    assert ".venv" not in readme
    assert "git clone" not in readme
    assert "E:\\" not in readme
    assert "C:\\" not in readme


def test_readme_explains_safe_local_secret_setup() -> None:
    readme = README_PATH.read_text(encoding="utf-8")

    assert ".env.example" in readme
    assert "never commit" in readme.lower()
