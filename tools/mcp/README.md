# Safe agent boundary

`renovation_mcp.py` provides a local JSON-lines interface with an explicit
allowlist for canonical validation, IFC generation, and design validation. It
cannot execute arbitrary shell commands, arbitrary Python, network requests,
or uncontrolled file writes. A real MCP transport can wrap this boundary later.
