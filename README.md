# Nano Banana MCP Server

Portable local MCP server for Gemini image generation, single-image editing, and multi-image blending.

## Features

- `generate_image` for text-to-image
- `edit_image` for prompt-guided edits on one local image
- `blend_images` for prompt-guided generation from two or more local images
- Environment-first config with `.env` fallback
- Local file outputs plus structured metadata for Codex

## Quickstart

### Prerequisites

- Python 3.11+
- A valid `GEMINI_API_KEY`

Set your API key before starting Codex:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

For local development, you can also copy `.env.example` to `.env` and fill in your key there. Treat `.env` as a local secret file and never commit it.

### Codex MCP Registration

Codex should run this MCP server through the installable command `mcp-nano-banana`.

### Install From Public GitHub Repository

If you publish this repository to GitHub before cutting a package release, install directly from the repo:

```powershell
pipx install git+https://github.com/<owner>/<repo>.git
```

Then register the installed command:

```toml
[mcp_servers.nano_banana]
command = "mcp-nano-banana"
startup_timeout_sec = 20
tool_timeout_sec = 120
```

Replace `https://github.com/<owner>/<repo>.git` with the actual public repository URL for this project.

### Packaged Install

This path is available after release.

Use `uvx` if you want Codex to launch the package on demand:

```toml
[mcp_servers.nano_banana]
command = "uvx"
args = ["mcp-nano-banana"]
startup_timeout_sec = 20
tool_timeout_sec = 120
```

If you prefer a one-time install after release:

```powershell
pipx install mcp-nano-banana
```

Then register the installed command:

```toml
[mcp_servers.nano_banana]
command = "mcp-nano-banana"
startup_timeout_sec = 20
tool_timeout_sec = 120
```

## Configuration

The server reads configuration from environment variables first, then from `.env`.

```env
GEMINI_API_KEY=your_api_key_here
NANO_BANANA_DEFAULT_MODEL=gemini-2.5-flash-image
NANO_BANANA_REQUEST_TIMEOUT=60
NANO_BANANA_OUTPUT_DIR=outputs
```

The default `outputs` directory is local build output and is ignored by git.

## Manual Run

After installation, you can start the server directly with:

```powershell
mcp-nano-banana
```

## Tool Return Shape

Each tool returns JSON with:

- `success`
- `tool`
- `model`
- `prompt`
- `output_paths`
- `input_images`
- `mime_types`
- `metadata`

`metadata` includes `output_dir`, `generated_at`, `image_count`, and `text_parts`.

## License

MIT
