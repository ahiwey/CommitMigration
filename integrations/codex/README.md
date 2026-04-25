# Codex Integration

This directory is the optional Codex-facing plugin root for `Commit Migration`.

Use it when you want three things together:

- a plugin manifest
- a skill that strongly triggers Android commit migration requests
- an MCP registration that exposes the migration analysis tools

## Directory Layout

This directory already matches the expected plugin-root layout:

- `.codex-plugin/plugin.json`
- `.mcp.json`
- `skills/commit-migration/`
- `assets/`

The core Python package still lives in [../../src/commit_migration](../../src/commit_migration/).

## Prerequisites

Before using this integration, install the repository package first.

CLI only:

```powershell
pip install -e .
```

If you want MCP support too:

```powershell
pip install -e ".[mcp]"
```

## Option 1: Install The Skill From GitHub

If you only need the skill, you can install it directly from GitHub with the built-in skill installer flow:

```powershell
python (Join-Path $env:USERPROFILE '.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py') `
  --repo ahiwey/CommitMigration `
  --path integrations/codex/skills/commit-migration
```

After installation, restart Codex to pick up the new skill.

## Option 2: Install As A Local Codex Plugin

If you want the plugin manifest plus the skill and MCP registration together, install this directory as a local plugin.

### Step 1. Place the plugin under your local plugins directory

Recommended target:

```text
~\plugins\commit-migration
```

You can copy or symlink `integrations/codex` to that location.

### Step 2. Add a local marketplace entry

Create or update:

```text
~\.agents\plugins\marketplace.json
```

Example:

```json
{
  "name": "local-tools",
  "interface": {
    "displayName": "Local Tools"
  },
  "plugins": [
    {
      "name": "commit-migration",
      "source": {
        "source": "local",
        "path": "./plugins/commit-migration"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Coding"
    }
  ]
}
```

### Step 3. Restart Codex

Restart Codex so it can discover the local plugin and skill bundle.

## Validation Notes

This plugin layout expects the Python package `commit_migration` to already be importable in the current environment.

That is why `.mcp.json` launches:

```text
python -m commit_migration.mcp_server
```

instead of relying on a repository-relative `PYTHONPATH`.

## Recommended User Requests

Once installed, these are the intended natural-language entry points:

- `Apply 45959162 to the current branch`
- `Migrate commit 45959162`
- `Apply 45959162,45959163 to the current branch`
- `Apply 45959162..45959199 to the current branch`
- `Apply the latest 3 commits from branch origin/feature_x to the current branch`
