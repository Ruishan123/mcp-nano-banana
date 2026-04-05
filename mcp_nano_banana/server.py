from __future__ import annotations

from functools import lru_cache

from mcp.server.fastmcp import FastMCP

from mcp_nano_banana.config import load_config
from mcp_nano_banana.gemini_client import GeminiImageClient
from mcp_nano_banana.service import ImageGenerationService

mcp = FastMCP("Nano Banana MCP", json_response=True)


@lru_cache(maxsize=1)
def get_service() -> ImageGenerationService:
    config = load_config()
    client = GeminiImageClient(
        api_key=config.api_key,
        timeout_seconds=config.request_timeout,
    )
    return ImageGenerationService(config=config, client=client)


@mcp.tool()
def generate_image(
    prompt: str,
    model: str | None = None,
    output_dir: str | None = None,
    filename_prefix: str | None = None,
) -> dict:
    """Generate a new image from a text prompt."""
    return get_service().generate_image(
        prompt=prompt,
        model=model,
        output_dir=output_dir,
        filename_prefix=filename_prefix,
    )


@mcp.tool()
def edit_image(
    prompt: str,
    image_path: str,
    model: str | None = None,
    output_dir: str | None = None,
    filename_prefix: str | None = None,
) -> dict:
    """Edit one local image with a prompt."""
    return get_service().edit_image(
        prompt=prompt,
        image_path=image_path,
        model=model,
        output_dir=output_dir,
        filename_prefix=filename_prefix,
    )


@mcp.tool()
def blend_images(
    prompt: str,
    image_paths: list[str],
    model: str | None = None,
    output_dir: str | None = None,
    filename_prefix: str | None = None,
) -> dict:
    """Blend two or more local images into a new result."""
    return get_service().blend_images(
        prompt=prompt,
        image_paths=image_paths,
        model=model,
        output_dir=output_dir,
        filename_prefix=filename_prefix,
    )


def main() -> None:
    mcp.run()
