from __future__ import annotations

from importlib import import_module


def test_package_server_exposes_main_and_mcp_name() -> None:
    module = import_module("mcp_nano_banana.server")

    assert module.mcp.name == "Nano Banana MCP"
    assert callable(module.main)
