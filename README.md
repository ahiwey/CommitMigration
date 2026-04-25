[![Release](https://img.shields.io/github/v/release/ahiwey/CommitMigration)](https://github.com/ahiwey/CommitMigration/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/ahiwey/CommitMigration)](./LICENSE)

# Commit Migration

Android commit migration toolkit for AI-assisted branch porting.

`Commit Migration` helps developers and AI agents analyze a commit, a commit range, or a branch diff and then port the equivalent Android changes onto the current branch with package-aware, class-aware, and resource-aware adaptation.

It is built as a generic toolkit first:

- use the core package and CLI for repository analysis
- enable the MCP server only when you need AI tool integration
- opt into the Codex-facing plugin and skill bundle only when your environment supports it

## Why It Exists

Applying changes across Android brand forks is rarely a clean `cherry-pick`.

Common migration blockers include:

- different package roots
- same-responsibility classes with different names
- different resource names
- manifest, navigation, provider, and XML references that need follow-up adaptation

`Commit Migration` is designed to surface those mappings early so the final migration can be deliberate instead of patch-first.

## Current Scope

- Android projects only
- Java and Kotlin source trees
- `res/`, `AndroidManifest.xml`, navigation XML, provider and authority references
- package-root, path, and resource mapping suggestions
- core CLI and analysis engine, plus optional AI integrations

## Quick Start

### 1. Install the package

```powershell
git clone https://github.com/ahiwey/CommitMigration.git
cd CommitMigration
pip install -e .
```

### 2. Analyze a commit against a target Android repository

```powershell
commit-migration analyze --repo D:\Project\Android\app_android_2025 --commit 45959162
```

### 3. Initialize repository hints if your project has brand-specific mappings

```powershell
commit-migration init-hints --repo D:\Project\Android\app_android_2025
```

This creates:

```text
.commit-migration/mapping_hints.json
```

### 4. Optional: install MCP support

```powershell
pip install -e ".[mcp]"
```

## What This Repository Provides

- a generic Python package with a shared Android migration analysis engine
- a local CLI for commit, range, and branch analysis
- an MCP server module that can be enabled when needed
- example mapping hints and a schema for repository-specific adaptation
- an optional Codex integration package with plugin manifest, skill, and icons
- publishing and contribution docs for GitHub release prep

## Natural-Language Requests

After the integration layer is installed in an AI environment, users can naturally say:

- `Apply 45959162 to the current branch`
- `Migrate commit 45959162`
- `Apply 45959162,45959163 to the current branch`
- `Apply 45959162..45959199 to the current branch`
- `Apply the latest 3 commits from branch origin/feature_x to the current branch`

The default behavior should be:

- modify only the current working branch
- never modify the source branch by default
- do not automatically `checkout`, `cherry-pick`, or `rebase`
- prefer equivalent migration plus adaptation over raw patch replay

## Choose Your Mode

### CLI only

Use this if you want repository analysis and reports without AI-specific integration.

### CLI + MCP

Use this if your AI environment can call MCP tools and you want structured read-only analysis results.

### Codex integration

Use this if you want the optional plugin manifest, skill, and MCP registration bundle under [integrations/codex](./integrations/codex/README.md).

## Repository Layout

```text
src/commit_migration/                 Shared Python engine, CLI, MCP module, and templates
examples/                             Repository hint examples
schemas/                              Mapping hint schema
integrations/codex/                   Optional Codex-specific integration layer
integrations/codex/.codex-plugin/     Codex plugin manifest
integrations/codex/.mcp.json          Codex MCP registration
integrations/codex/skills/            Codex skill and references
integrations/codex/assets/            Codex plugin icons
```

## CLI Usage

Use the tool against the target Android repository, not this repository's source tree.

### Analyze a single commit

```powershell
commit-migration analyze --repo D:\Project\Android\app_android_2025 --commit 45959162
```

### Analyze multiple commits

```powershell
commit-migration analyze --repo D:\Project\Android\app_android_2025 --commit 45959162 --commit 45959163
```

### Analyze a range

```powershell
commit-migration analyze --repo D:\Project\Android\app_android_2025 --range 45959162..45959199
```

### Analyze branch recent commits

```powershell
commit-migration analyze --repo D:\Project\Android\app_android_2025 --branch origin/Fascine --recent 3
```

### Export JSON

```powershell
commit-migration analyze --repo D:\Project\Android\app_android_2025 --commit 45959162 --json --output report.json
```

You can also invoke the package module directly:

```powershell
python -m commit_migration analyze --repo D:\Project\Android\app_android_2025 --commit 45959162
```

### Run a basic repository doctor check

```powershell
commit-migration doctor --repo D:\Project\Android\app_android_2025
```

## Repo-Specific Hints

You can optionally provide a JSON hints file, or let the tool auto-discover one from the target repository.

Auto-discovery checks these locations inside the target repository:

- `.commit-migration/mapping_hints.json`
- `.codex/commit-migration/mapping_hints.json`
- `tools/branch_apply/mapping_hints.json`

The hint file format is:

```json
{
  "package_roots": {
    "com/qcwireless/smart": "com/fitpaddy/smart"
  },
  "path_overrides": {
    "app/src/main/java/com/source/Old.kt": "app/src/main/java/com/target/New.kt"
  },
  "resource_name_map": {
    "old_ring_primary": "ring_main"
  }
}
```

See [examples/mapping_hints.android_brand.json](./examples/mapping_hints.android_brand.json) for a starting point.
Schema: [schemas/mapping_hints.schema.json](./schemas/mapping_hints.schema.json)

## MCP Tools

The MCP server exposes these read-only tools:

- `analyze_commit_selection`
- `build_android_mapping`
- `collect_android_followups`
- `analyze_android_commit_migration`

These tools are designed to help an AI agent do the final migration safely rather than blindly applying patches.

## Additional Docs

- [INSTALL.md](./INSTALL.md)
- [USAGE.md](./USAGE.md)
- [PUBLISHING.md](./PUBLISHING.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [CHANGELOG.md](./CHANGELOG.md)
