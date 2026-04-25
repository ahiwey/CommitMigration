# Codex Integration

This directory contains the optional Codex-specific integration layer for `Commit Migration`.

## What Lives Here

- `.codex-plugin/plugin.json`
- `.mcp.json`
- `skills/commit-migration/`
- `assets/`

## When To Use It

Use this directory only when you want to install `Commit Migration` as a Codex-facing plugin and skill package.

If you only need the generic Python package or CLI, you can ignore this directory and install the repository root package instead.

## Notes

- The core analysis engine still lives in [src/commit_migration](../../src/commit_migration/).
- The plugin manifest in `.codex-plugin/plugin.json` points back to the shared core package and this integration folder.
- The MCP registration in `.mcp.json` assumes the repository root package is available on `PYTHONPATH`.
