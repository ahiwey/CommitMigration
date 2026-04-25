# Publishing Guide

## Before pushing to GitHub

Replace placeholder values in:

- [integrations/codex/.codex-plugin/plugin.json](./integrations/codex/.codex-plugin/plugin.json)
- [README.md](./README.md)
- [schemas/mapping_hints.schema.json](./schemas/mapping_hints.schema.json)

In particular, update:

- GitHub organization or username
- repository URL
- maintainer email
- website, privacy, and terms links

## Recommended repository setup

1. Create the GitHub repository.
2. Push the contents of this folder.
3. Add a short release tag such as `v0.1.0`.
4. Keep the first release scoped to Android-only migration analysis.
5. Describe the repository as a generic toolkit first, with Codex integration presented as optional.

## Suggested installation story for users

Tell users to install the generic package first, then optionally wire up the Codex integration if they want natural-language triggering inside Codex.

Core install:

```powershell
pip install -e .
```

Optional MCP support:

```powershell
pip install -e ".[mcp]"
```

Once installed, users can use natural requests such as:

- `Apply 45959162 to the current branch`
- `Migrate commit 45959162`
- `Apply 45959162..45959199 to the current branch`

## Dependency note

The CLI works once Python can import the package from `src/`.

The MCP server additionally requires the optional `mcp` dependency from [pyproject.toml](./pyproject.toml).

## Repo-specific hints

Users can optionally create one of these files in their Android repository:

- `.commit-migration/mapping_hints.json`
- `.codex/commit-migration/mapping_hints.json`
- `tools/branch_apply/mapping_hints.json`

If any of these exist, `Commit Migration` will automatically discover them.
