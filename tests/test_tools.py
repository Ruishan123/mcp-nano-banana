from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image

from mcp_nano_banana.tools import (
    ensure_prompt,
    load_image_inputs,
    parse_generation_response,
)
from tests.support import scratch_dir


def test_ensure_prompt_rejects_blank_input() -> None:
    with pytest.raises(ValueError, match="prompt"):
        ensure_prompt("   ")


def test_load_image_inputs_rejects_missing_file() -> None:
    with scratch_dir() as tmp_path:
        with pytest.raises(FileNotFoundError):
            load_image_inputs([str(tmp_path / "missing.png")], base_dir=tmp_path)


def test_load_image_inputs_rejects_unsupported_extension() -> None:
    with scratch_dir() as tmp_path:
        source = tmp_path / "input.gif"
        source.write_bytes(b"GIF89a")

        with pytest.raises(ValueError, match="Unsupported image type"):
            load_image_inputs([str(source)], base_dir=tmp_path)


def test_load_image_inputs_accepts_relative_paths_and_validates_images() -> None:
    with scratch_dir() as tmp_path:
        source = tmp_path / "input.png"
        Image.new("RGB", (2, 2), color="red").save(source)

        image_inputs = load_image_inputs(["input.png"], base_dir=tmp_path)

        assert len(image_inputs) == 1
        assert image_inputs[0].path == source.resolve()
        assert image_inputs[0].mime_type == "image/png"


def test_parse_generation_response_collects_text_and_image_parts() -> None:
    response = SimpleNamespace(
        candidates=[
            SimpleNamespace(
                content=SimpleNamespace(
                    parts=[
                        SimpleNamespace(text="first note"),
                        SimpleNamespace(
                            inline_data=SimpleNamespace(
                                data=b"image-a",
                                mime_type="image/png",
                            )
                        ),
                        SimpleNamespace(text="second note"),
                        SimpleNamespace(
                            inline_data=SimpleNamespace(
                                data=b"image-b",
                                mime_type="image/png",
                            )
                        ),
                    ]
                )
            )
        ]
    )

    parsed = parse_generation_response(response)

    assert parsed.text_parts == ["first note", "second note"]
    assert parsed.images == [b"image-a", b"image-b"]
    assert parsed.mime_types == ["image/png", "image/png"]


def test_parse_generation_response_handles_text_only_output() -> None:
    response = SimpleNamespace(
        candidates=[
            SimpleNamespace(
                content=SimpleNamespace(
                    parts=[SimpleNamespace(text="no images were returned")]
                )
            )
        ]
    )

    parsed = parse_generation_response(response)

    assert parsed.text_parts == ["no images were returned"]
    assert parsed.images == []
    assert parsed.mime_types == []
