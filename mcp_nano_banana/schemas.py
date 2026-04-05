from __future__ import annotations

from typing import TypedDict


class ToolMetadata(TypedDict):
    output_dir: str
    generated_at: str
    image_count: int
    text_parts: list[str]


class ToolResult(TypedDict):
    success: bool
    tool: str
    model: str
    prompt: str
    output_paths: list[str]
    input_images: list[str]
    mime_types: list[str]
    metadata: ToolMetadata
