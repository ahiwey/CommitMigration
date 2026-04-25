# Contributing

Thanks for contributing to `Commit Migration`.

## Scope

This project currently focuses on Android repository migration analysis:

- commit selection analysis
- package and path mapping
- Android resource discovery
- migration follow-up generation
- Skill + MCP + CLI integration

Please keep pull requests aligned with that scope unless a broader roadmap change has already been discussed.

## Development Setup

```powershell
cd D:\Project\Android\CommitMigration
pip install -e .
```

If you want to run the MCP server locally, also make sure the `mcp` dependency is installed from `pyproject.toml`.

## Useful Commands

### CLI help

```powershell
python -m commit_migration analyze --help
python -m commit_migration init-hints --help
python -m commit_migration doctor --help
```

### Syntax check

```powershell
@'
import py_compile
from pathlib import Path
for path in Path("src/commit_migration").rglob("*.py"):
    py_compile.compile(str(path), doraise=True)
print("py_compile_ok")
'@ | python -
```

## Contribution Guidelines

- Preserve the default safety model: current branch only, no automatic source-branch mutation.
- Keep Android-specific follow-up logic explicit and readable.
- Prefer improving the shared analyzer instead of duplicating logic between CLI and MCP.
- Add docs when you add behavior.
- Avoid turning the tool into a blind patch applier unless that behavior is intentionally gated and reviewed.

## Pull Request Checklist

- Explain the user-facing problem.
- Explain whether the change affects Skill behavior, MCP behavior, or CLI behavior.
- Mention any new assumptions about Android repository layout.
- Update docs if usage changed.
