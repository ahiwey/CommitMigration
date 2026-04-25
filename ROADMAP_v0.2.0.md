# Commit Migration v0.2.0 Roadmap

## Goals

The next version should move beyond file-path and package-root mapping and improve semantic matching for real Android brand-fork migrations.

## Priority Themes

### 1. Stronger class mapping

Current behavior is strongest when file names or package structure are still close.

Next version should improve:

- same-responsibility classes with different names
- sibling component discovery through imports and XML usage
- ranking candidates by confidence instead of a flat candidate list

Suggested implementation ideas:

- score file-name similarity
- score package suffix overlap
- score shared import patterns
- score shared referenced resources and layouts
- combine these into a confidence value per candidate

### 2. Stronger resource mapping

Current behavior handles direct and fuzzy resource-name matches, but not enough semantic adaptation.

Next version should improve:

- resource aliases across brand forks
- grouped replacements for related drawables, colors, and dimensions
- better value-resource matching in `values/*.xml`

Suggested implementation ideas:

- support resource prefix and suffix families
- allow hint groups, not just one-to-one names
- rank `values` entries by XML type plus name similarity

### 3. Patch preview and migration review

The tool is analysis-first today. The next useful step is to help the user review likely edits before final application.

Suggested implementation ideas:

- generate a patch preview report
- separate direct-apply, review-first, and missing buckets more clearly
- output per-file adaptation reasons

### 4. Better repository onboarding

Repository-specific hints are powerful, but the tool should make onboarding easier.

Suggested implementation ideas:

- scaffold richer hints from an existing repository
- detect likely package-root mappings automatically
- emit hint suggestions from past analyses

### 5. Integration polish

The Codex integration is now optional and valid as a plugin root, but installation can still be smoother.

Suggested implementation ideas:

- add a helper script to prepare a local plugin install
- document non-Codex AI installation paths
- add a release checklist for plugin validation

## Proposed Milestone Order

1. confidence-based class mapping
2. richer resource matching
3. patch preview output
4. hints suggestion workflow
5. install helper automation

## Non-Goals For v0.2.0

- blind patch application
- iOS migration support
- backend or general monorepo migration support
