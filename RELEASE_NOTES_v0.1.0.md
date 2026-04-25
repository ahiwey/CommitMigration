# Commit Migration v0.1.0

Initial public release of `Commit Migration`.

`Commit Migration` is an Android-focused toolkit for analyzing commit, range, and branch changes before porting them across branches, brand forks, or product variants.

## Highlights

- Added a generic Python package and CLI for Android commit migration analysis.
- Added commit selection support for:
  - single commits
  - multiple commits
  - commit ranges such as `A..B`
  - branch diffs
  - recent commits from a branch
- Added Android-aware mapping analysis for:
  - package roots
  - file paths
  - resource names
  - values-based resources in `values/*.xml`
- Added Android follow-up generation for:
  - manifest references
  - XML component wiring
  - navigation and provider references
  - imports and fully qualified names
  - reflection, routing, and resource-chain checks
- Added repository hints support through `.commit-migration/mapping_hints.json`.
- Added optional MCP support for structured AI tool integration.
- Added an optional Codex integration layer with plugin manifest, skill, and MCP registration.

## Core Commands

```powershell
commit-migration analyze --repo <android-repo> --commit <sha>
commit-migration analyze --repo <android-repo> --range A..B
commit-migration analyze --repo <android-repo> --branch <branch> --recent 3
commit-migration init-hints --repo <android-repo>
commit-migration doctor --repo <android-repo>
```

## Default Behavior

- Works only on the current branch working tree by default.
- Does not modify the source branch by default.
- Does not automatically `checkout`, `cherry-pick`, or `rebase`.
- Prefers equivalent migration plus adaptation over blind patch replay.

## Installation

Base package:

```powershell
pip install -e .
```

Optional MCP support:

```powershell
pip install -e ".[mcp]"
```

## Scope

- Android projects only
- Java and Kotlin source trees
- `res/`, `AndroidManifest.xml`, navigation XML, provider and authority references
- Analysis-first workflow, not blind patch application

## Notes

- The default hints location is `.commit-migration/mapping_hints.json`.
- Legacy Codex-oriented hint paths are still supported for compatibility.
- The Codex-facing plugin and skill bundle is available under `integrations/codex/`.
