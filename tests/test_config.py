from pathlib import Path

import pytest

from mcp_nano_banana.config import AppConfig, load_config
from tests.support import scratch_dir


def test_load_config_prefers_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    with scratch_dir() as tmp_path:
        env_path = tmp_path / ".env"
        env_path.write_text(
            "\n".join(
                [
                    "GEMINI_API_KEY=from-dotenv",
                    "NANO_BANANA_DEFAULT_MODEL=dotenv-model",
                    "NANO_BANANA_REQUEST_TIMEOUT=45",
                ]
            ),
            encoding="utf-8",
        )
        monkeypatch.setenv("GEMINI_API_KEY", "from-env")
        monkeypatch.setenv("NANO_BANANA_DEFAULT_MODEL", "env-model")
        monkeypatch.setenv("NANO_BANANA_REQUEST_TIMEOUT", "30")

        config = load_config(base_dir=tmp_path)

        assert config == AppConfig(
            api_key="from-env",
            default_model="env-model",
            request_timeout=30,
            output_base_dir=tmp_path / "outputs",
            base_dir=tmp_path,
        )


def test_load_config_uses_dotenv_when_environment_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    with scratch_dir() as tmp_path:
        env_path = tmp_path / ".env"
        env_path.write_text(
            "\n".join(
                [
                    "GEMINI_API_KEY=from-dotenv",
                    "NANO_BANANA_DEFAULT_MODEL=dotenv-model",
                    "NANO_BANANA_OUTPUT_DIR=custom-outputs",
                ]
            ),
            encoding="utf-8",
        )
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("NANO_BANANA_DEFAULT_MODEL", raising=False)
        monkeypatch.delenv("NANO_BANANA_OUTPUT_DIR", raising=False)

        config = load_config(base_dir=tmp_path)

        assert config.api_key == "from-dotenv"
        assert config.default_model == "dotenv-model"
        assert config.output_base_dir == tmp_path / "custom-outputs"


def test_load_config_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    with scratch_dir() as tmp_path:
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        (tmp_path / ".env").write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="GEMINI_API_KEY"):
            load_config(base_dir=tmp_path)
