from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

from mcp_nano_banana.config import AppConfig
from mcp_nano_banana.service import ImageGenerationService
from tests.support import scratch_dir


class FakeGeminiClient:
    def __init__(self, response: object) -> None:
        self.response = response
        self.calls: list[dict[str, object]] = []

    def generate_content(self, *, model: str, contents: list[object]) -> object:
        self.calls.append({"model": model, "contents": contents})
        return self.response


def make_response() -> object:
    return SimpleNamespace(
        candidates=[
            SimpleNamespace(
                content=SimpleNamespace(
                    parts=[
                        SimpleNamespace(text="generated successfully"),
                        SimpleNamespace(
                            inline_data=SimpleNamespace(
                                data=b"image-a",
                                mime_type="image/png",
                            )
                        ),
                    ]
                )
            )
        ]
    )


def make_config(base_dir: Path) -> AppConfig:
    return AppConfig(
        api_key="test-key",
        default_model="gemini-2.5-flash-image",
        request_timeout=60,
        output_base_dir=base_dir / "outputs",
        base_dir=base_dir,
    )


def test_generate_image_returns_structured_payload_and_saves_outputs() -> None:
    with scratch_dir() as tmp_path:
        config = make_config(tmp_path)
        client = FakeGeminiClient(make_response())
        service = ImageGenerationService(config=config, client=client)

        result = service.generate_image(
            prompt="A suspension bridge at sunrise",
            filename_prefix="bridge",
        )

        assert result["success"] is True
        assert result["tool"] == "generate_image"
        assert result["model"] == "gemini-2.5-flash-image"
        assert result["input_images"] == []
        assert result["mime_types"] == ["image/png"]
        assert result["metadata"]["image_count"] == 1
        assert result["metadata"]["text_parts"] == ["generated successfully"]
        assert len(result["output_paths"]) == 1
        assert Path(result["output_paths"][0]).exists()
        assert client.calls[0]["contents"] == ["A suspension bridge at sunrise"]


def test_blend_images_requires_at_least_two_input_images() -> None:
    with scratch_dir() as tmp_path:
        source = tmp_path / "input.png"
        Image.new("RGB", (2, 2), color="blue").save(source)
        config = make_config(tmp_path)
        client = FakeGeminiClient(make_response())
        service = ImageGenerationService(config=config, client=client)

        with pytest.raises(ValueError, match="at least 2 images"):
            service.blend_images(
                prompt="Combine these images",
                image_paths=[str(source)],
            )
