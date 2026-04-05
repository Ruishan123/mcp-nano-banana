from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image

SUPPORTED_SUFFIXES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


@dataclass(frozen=True)
class ImageInput:
    path: Path
    mime_type: str
    data: bytes


@dataclass(frozen=True)
class ParsedResponse:
    images: list[bytes]
    mime_types: list[str]
    text_parts: list[str]


def ensure_prompt(prompt: str) -> str:
    normalized = prompt.strip()
    if not normalized:
        raise ValueError("prompt must not be blank")
    return normalized


def load_image_inputs(paths: list[str], base_dir: Path) -> list[ImageInput]:
    image_inputs: list[ImageInput] = []
    for raw_path in paths:
        path = Path(raw_path)
        resolved_path = path.resolve() if path.is_absolute() else (base_dir / path).resolve()
        if not resolved_path.exists():
            raise FileNotFoundError(resolved_path)

        suffix = resolved_path.suffix.lower()
        mime_type = SUPPORTED_SUFFIXES.get(suffix)
        if mime_type is None:
            raise ValueError(f"Unsupported image type: {resolved_path.suffix}")

        with Image.open(resolved_path) as image:
            image.verify()

        image_inputs.append(
            ImageInput(
                path=resolved_path,
                mime_type=mime_type,
                data=resolved_path.read_bytes(),
            )
        )
    return image_inputs


def parse_generation_response(response: Any) -> ParsedResponse:
    images: list[bytes] = []
    mime_types: list[str] = []
    text_parts: list[str] = []

    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            text = getattr(part, "text", None)
            if text:
                text_parts.append(text)

            inline_data = getattr(part, "inline_data", None)
            if inline_data and getattr(inline_data, "data", None):
                images.append(inline_data.data)
                mime_types.append(getattr(inline_data, "mime_type", "image/png"))

    return ParsedResponse(images=images, mime_types=mime_types, text_parts=text_parts)
