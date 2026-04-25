# Commit Migration

Android commit migration toolkit for AI-assisted branch porting.

`Commit Migration` is a generic Android migration toolkit first. It analyzes a commit, a commit range, or a branch diff and helps an AI apply equivalent changes onto the current branch while adapting Android-specific references such as package roots, class paths, resources, manifest references, and XML wiring.

The Codex plugin, skill, and MCP registration are still supported, but they now live under an optional integration layer instead of defining the repository root.

## Current Scope

- Android projects only
- Java and Kotlin source trees
- `res/`, `AndroidManifest.xml`, navigation XML, provider and authority references
- package-root, path, and resource mapping suggestions
- core CLI and analysis engine, plus optional AI integrations

## What This Repository Provides

- a generic Python package with a shared Android migration analysis engine
- a local CLI for commit, range, and branch analysis
- an MCP server module that can be enabled when needed
- example mapping hints and a schema for repository-specific adaptation
- an optional Codex integration package with plugin manifest, skill, and icons
- publishing and contribution docs for GitHub release prep

## Example User Requests

After installation, users can naturally say:

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

## Installation Notes

For the generic CLI and Python package:

```powershell
cd D:\Project\Android\CommitMigration
pip install -e .
```

After that, these commands should work:

```powershell
commit-migration analyze --help
python -m commit_migration analyze --help
```

If you also want the Codex-specific skill and plugin integration, use the files under [integrations/codex](./integrations/codex/README.md).

See [PUBLISHING.md](./PUBLISHING.md) for the publish checklist.

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

### Initialize hints in a target repository

```powershell
commit-migration init-hints --repo D:\Project\Android\app_android_2025
```

By default this writes:

```text
.commit-migration/mapping_hints.json
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
- [PUBLISHING.md](./PUBLISHING.md)
- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [CHANGELOG.md](./CHANGELOG.md)
