# Usage Guide

## Who This Is For

Use `Commit Migration` if you need to move Android changes across branches, product variants, or brand forks and you want a structured mapping report before editing code.

## Typical Team Workflow

1. Install the package locally.
2. Run `doctor` against the target Android repository.
3. Create `.commit-migration/mapping_hints.json` if your repository has known package, class, or resource mappings.
4. Analyze the commit, range, or branch selection.
5. Use the analysis result to perform the final code migration in your editor or AI workflow.

## CLI Workflow

### Install

```powershell
git clone https://github.com/ahiwey/CommitMigration.git
cd CommitMigration
pip install -e .
```

### Check a target repository

```powershell
commit-migration doctor --repo D:\Project\Android\app_android_2025
```

### Create a starter hints file

```powershell
commit-migration init-hints --repo D:\Project\Android\app_android_2025
```

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

### Analyze recent branch commits

```powershell
commit-migration analyze --repo D:\Project\Android\app_android_2025 --branch origin/Fascine --recent 3
```

## Hints Strategy

Start with `.commit-migration/mapping_hints.json` when your repository already has known adaptation rules.

Use hints for:

- package root remapping
- file path overrides
- resource name replacement

Keep hints narrow and explicit. Prefer only the mappings that are stable across migrations.

## Working With AI

If your AI environment supports MCP or a plugin-style integration, install the optional bundle under [integrations/codex](./integrations/codex/README.md).

After that, the natural-language entry points are meant to look like:

- `Apply 45959162 to the current branch`
- `Migrate commit 45959162`
- `Apply 45959162..45959199 to the current branch`
- `Apply the latest 3 commits from branch origin/feature_x to the current branch`

## Recommended Migration Rules

- Work only on the current branch working tree by default.
- Do not modify the source branch by default.
- Do not rely on raw patch replay when package or resource structure differs.
- Always review manifest, XML, navigation, provider, and resource follow-ups before finalizing the migration.

## What The Tool Does Not Do

- It does not promise safe blind patch application.
- It does not replace Android-specific review judgment.
- It does not currently target iOS or backend repositories.
