from mcp_nano_banana.storage import save_generated_images
from tests.support import scratch_dir


def test_save_generated_images_creates_output_dir_and_deterministic_names() -> None:
    with scratch_dir() as tmp_path:
        result = save_generated_images(
            images=[b"image-one", b"image-two"],
            mime_types=["image/png", "image/png"],
            tool_name="generate_image",
            base_output_dir=tmp_path,
            generated_at="20260405T120102Z",
            filename_prefix="bridge",
        )

        output_dir = tmp_path / "2026-04-05"
        assert output_dir.exists()
        assert result == [
            output_dir / "bridge-generate_image-20260405T120102Z-01.png",
            output_dir / "bridge-generate_image-20260405T120102Z-02.png",
        ]
        assert result[0].read_bytes() == b"image-one"
        assert result[1].read_bytes() == b"image-two"
