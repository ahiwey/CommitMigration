# Commit Migration v0.1.0

Initial public release of `Commit Migration`.

## Highlights

- Added an Android-focused commit migration workflow for AI-assisted branch porting
- Shaped the repository as a generic toolkit first, with Codex plugin and skill files kept in an optional integration layer
- Added a strongly-triggered skill for requests like applying a commit or branch changes to the current branch
- Added a shared Python analyzer for:
  - single commits
  - multiple commits
  - commit ranges
  - branch diffs
  - recent commits from a branch
- Added Android-aware mapping support for:
  - package roots
  - file paths
  - resources under `res/`
  - values-based resources in `values/*.xml`
- Added Android follow-up generation for:
  - manifest references
  - XML component wiring
  - providers and authorities
  - imports and fully qualified names
  - reflection, routing, and resource-chain checks
- Added MCP server entry points for read-only migration analysis tools
- Added CLI commands:
  - `analyze`
  - `init-hints`
  - `doctor`
- Added schema, examples, publishing docs, contribution docs, and GitHub templates

## Notes

- Current scope is Android only
- The tool is analysis-first and does not blindly apply patches
- Default behavior is to work only on the current branch working tree and avoid modifying the source branch
- The default hints location is `.commit-migration/mapping_hints.json`, while legacy Codex-oriented hint paths remain supported
