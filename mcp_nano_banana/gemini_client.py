from __future__ import annotations

from typing import Any

from google import genai
from google.genai import types

from mcp_nano_banana.tools import ImageInput


class GeminiImageClient:
    def __init__(self, api_key: str, timeout_seconds: int) -> None:
        http_options = types.HttpOptions(timeout=timeout_seconds * 1000)
        self._client = genai.Client(api_key=api_key, http_options=http_options)

    def generate_content(self, *, model: str, contents: list[object]) -> Any:
        request_parts: list[object] = []
        for item in contents:
            if isinstance(item, ImageInput):
                request_parts.append(
                    types.Part.from_bytes(data=item.data, mime_type=item.mime_type)
                )
            else:
                request_parts.append(item)

        return self._client.models.generate_content(
            model=model,
            contents=request_parts,
        )
