---
name: commit-migration
description: Analyze Android commit or branch changes and help apply equivalent changes onto the current branch with package, class, path, manifest, XML, and resource-aware adaptation. Use this whenever the user asks to apply a commit to the current branch, migrate a commit, port changes from another branch, apply a commit range such as A..B, or bring recent Android changes across brand forks or product variants, even if they do not explicitly mention "migration."
---

# Commit Migration

Use this skill for Android repositories when the user wants to port code changes from one commit or branch context into the current branch.

## Default behavior

- Modify only the current working branch by default.
- Never modify the source branch by default.
- Do not automatically `checkout`, `cherry-pick`, or `rebase`.
- Prefer equivalent migration plus Android-aware adaptation over raw patch replay.
- Pause only when mapping confidence is low or current-branch custom behavior would be overwritten.

## Supported user phrasing

Treat requests like these as triggers:

- `Apply 45959162 to the current branch`
- `Migrate commit 45959162`
- `Apply 45959162,45959163 to the current branch`
- `Apply 45959162..45959199 to the current branch`
- `Apply the latest 3 commits from branch X to the current branch`
- `Bring this branch's changes into the current Android branch`

## Execution order

1. Parse the user's selection.
2. Use MCP tools if available.
3. Fall back to the CLI if MCP tools are not available.
4. Review direct mappings, review candidates, and missing items.
5. Apply equivalent code changes in the user's current repository.
6. Run the Android follow-up checklist before claiming completion.

## Preferred tools

### MCP first

If the plugin MCP server is available, prefer:

- `analyze_android_commit_migration`
- `build_android_mapping`
- `collect_android_followups`

### CLI fallback

If MCP is unavailable, use the CLI:

```powershell
commit-migration analyze --repo <target-repo> --commit <sha>
```

Repeat `--commit` for multiple commits, or use:

```powershell
commit-migration analyze --repo <target-repo> --range A..B
commit-migration analyze --repo <target-repo> --branch origin/feature_x --recent 3
```

## What to adapt

Always consider:

- package roots
- file paths
- same-responsibility classes with different names
- imports and fully qualified class names
- `AndroidManifest.xml`
- custom View references in XML
- navigation XML
- `provider` and `authority`
- resource names and values XML entries
- reflection strings
- routing strings
- serialization model names
- Proguard or R8 class references

## References

- [workflow.md](./references/workflow.md)
- [android-mapping.md](./references/android-mapping.md)
- [android-checklist.md](./references/android-checklist.md)

## Repo-specific hints

If the target repository provides mapping hints, use them first. The expected format is shown in:

- [mapping_hints.example.json](./assets/mapping_hints.example.json)
