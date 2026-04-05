from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from mcp_nano_banana.config import AppConfig
from mcp_nano_banana.schemas import ToolMetadata, ToolResult
from mcp_nano_banana.storage import save_generated_images
from mcp_nano_banana.tools import ImageInput, ensure_prompt, load_image_inputs, parse_generation_response


class SupportsGenerateContent(Protocol):
    def generate_content(self, *, model: str, contents: list[object]) -> object: ...


class ImageGenerationService:
    def __init__(self, config: AppConfig, client: SupportsGenerateContent) -> None:
        self._config = config
        self._client = client

    def generate_image(
        self,
        *,
        prompt: str,
        model: str | None = None,
        output_dir: str | None = None,
        filename_prefix: str | None = None,
    ) -> ToolResult:
        return self._run(
            tool_name="generate_image",
            prompt=prompt,
            image_paths=[],
            model=model,
            output_dir=output_dir,
            filename_prefix=filename_prefix,
            minimum_images=0,
        )

    def edit_image(
        self,
        *,
        prompt: str,
        image_path: str,
        model: str | None = None,
        output_dir: str | None = None,
        filename_prefix: str | None = None,
    ) -> ToolResult:
        return self._run(
            tool_name="edit_image",
            prompt=prompt,
            image_paths=[image_path],
            model=model,
            output_dir=output_dir,
            filename_prefix=filename_prefix,
            minimum_images=1,
        )

    def blend_images(
        self,
        *,
        prompt: str,
        image_paths: list[str],
        model: str | None = None,
        output_dir: str | None = None,
        filename_prefix: str | None = None,
    ) -> ToolResult:
        return self._run(
            tool_name="blend_images",
            prompt=prompt,
            image_paths=image_paths,
            model=model,
            output_dir=output_dir,
            filename_prefix=filename_prefix,
            minimum_images=2,
        )

    def _run(
        self,
        *,
        tool_name: str,
        prompt: str,
        image_paths: list[str],
        model: str | None,
        output_dir: str | None,
        filename_prefix: str | None,
        minimum_images: int,
    ) -> ToolResult:
        normalized_prompt = ensure_prompt(prompt)
        if minimum_images and len(image_paths) < minimum_images:
            raise ValueError(f"{tool_name} requires at least {minimum_images} images")

        image_inputs = load_image_inputs(image_paths, base_dir=Path.cwd()) if image_paths else []
        contents: list[object] = [*image_inputs, normalized_prompt]
        resolved_model = model or self._config.default_model
        response = self._client.generate_content(model=resolved_model, contents=contents)
        parsed = parse_generation_response(response)

        generated_at = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        base_output_dir = self._resolve_output_dir(output_dir)
        saved_paths = save_generated_images(
            images=parsed.images,
            mime_types=parsed.mime_types,
            tool_name=tool_name,
            base_output_dir=base_output_dir,
            generated_at=generated_at,
            filename_prefix=filename_prefix,
        )

        metadata: ToolMetadata = {
            "output_dir": str(base_output_dir),
            "generated_at": generated_at,
            "image_count": len(saved_paths),
            "text_parts": parsed.text_parts,
        }
        return {
            "success": True,
            "tool": tool_name,
            "model": resolved_model,
            "prompt": normalized_prompt,
            "output_paths": [str(path) for path in saved_paths],
            "input_images": [str(image.path) for image in image_inputs],
            "mime_types": parsed.mime_types,
            "metadata": metadata,
        }

    def _resolve_output_dir(self, output_dir: str | None) -> Path:
        if not output_dir:
            return self._config.output_base_dir

        candidate = Path(output_dir)
        if candidate.is_absolute():
            return candidate.resolve()
        return (Path.cwd() / candidate).resolve()
