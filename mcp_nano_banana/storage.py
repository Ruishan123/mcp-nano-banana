from __future__ import annotations

from pathlib import Path


def save_generated_images(
    images: list[bytes],
    mime_types: list[str] | None,
    tool_name: str,
    base_output_dir: Path,
    generated_at: str,
    filename_prefix: str | None = None,
) -> list[Path]:
    date_dir = generated_at[:8]
    output_dir = base_output_dir / f"{date_dir[:4]}-{date_dir[4:6]}-{date_dir[6:8]}"
    output_dir.mkdir(parents=True, exist_ok=True)

    prefix = filename_prefix.strip() if filename_prefix else "image"
    saved_paths: list[Path] = []
    for index, image in enumerate(images, start=1):
        extension = _extension_for_mime_type((mime_types or [])[index - 1] if mime_types and len(mime_types) >= index else "image/png")
        path = output_dir / f"{prefix}-{tool_name}-{generated_at}-{index:02d}{extension}"
        path.write_bytes(image)
        saved_paths.append(path)
    return saved_paths


def _extension_for_mime_type(mime_type: str) -> str:
    if mime_type == "image/jpeg":
        return ".jpg"
    if mime_type == "image/webp":
        return ".webp"
    return ".png"
