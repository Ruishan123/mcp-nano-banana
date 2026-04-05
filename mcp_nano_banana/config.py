from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

DEFAULT_MODEL = "gemini-2.5-flash-image"
DEFAULT_TIMEOUT = 60


@dataclass(frozen=True)
class AppConfig:
    api_key: str
    default_model: str
    request_timeout: int
    output_base_dir: Path
    base_dir: Path


def load_config(base_dir: Path | None = None) -> AppConfig:
    resolved_base_dir = (base_dir or Path(__file__).resolve().parents[1]).resolve()
    env_path = resolved_base_dir / ".env"
    dotenv_config = {
        key: value
        for key, value in dotenv_values(env_path).items()
        if value is not None
    }

    def get_value(name: str, default: str | None = None) -> str | None:
        value = os.getenv(name)
        if value not in (None, ""):
            return value
        return dotenv_config.get(name, default)

    api_key = get_value("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY must be set via environment or .env")

    default_model = get_value("NANO_BANANA_DEFAULT_MODEL", DEFAULT_MODEL) or DEFAULT_MODEL
    request_timeout = int(get_value("NANO_BANANA_REQUEST_TIMEOUT", str(DEFAULT_TIMEOUT)) or DEFAULT_TIMEOUT)
    output_dir_value = get_value("NANO_BANANA_OUTPUT_DIR", "outputs") or "outputs"
    output_base_dir = (resolved_base_dir / output_dir_value).resolve()

    return AppConfig(
        api_key=api_key,
        default_model=default_model,
        request_timeout=request_timeout,
        output_base_dir=output_base_dir,
        base_dir=resolved_base_dir,
    )
