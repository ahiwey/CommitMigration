# Install

## Local Development Install

```powershell
cd D:\Project\Android\CommitMigration
pip install -e .
```

After that, these commands should work:

```powershell
commit-migration analyze --help
python -m commit_migration analyze --help
```

## Optional MCP Dependency

The generic CLI works with the base package install.

If you want to run the MCP server, install the optional extra from [pyproject.toml](./pyproject.toml):

```powershell
pip install -e ".[mcp]"
```

If you only want the CLI, importing the MCP module is not required.

## Optional Codex Integration

Codex-specific files now live under [integrations/codex](./integrations/codex/README.md).

Use that integration layer only if you want the repository to expose a Codex plugin manifest, skill, and MCP registration.

## Example Usage

```powershell
commit-migration analyze --repo D:\Project\Android\app_android_2025 --commit 45959162
```

## Initialize Repo Hints

You can scaffold a default hints file into a target Android repository:

```powershell
commit-migration init-hints --repo D:\Project\Android\app_android_2025
```

By default this writes:

```text
.commit-migration/mapping_hints.json
```

## Environment Check

```powershell
commit-migration doctor --repo D:\Project\Android\app_android_2025
```
