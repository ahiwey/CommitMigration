from __future__ import annotations

from .analyzer import analyze_android_commit_migration as run_analysis
from .analyzer import collect_followups, collect_selection, normalize_repo_root
from .git_ops import current_branch

try:
    from mcp.server.fastmcp import FastMCP
except Exception as exc:  # pragma: no cover - import-time environment guard
    FastMCP = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


def _ensure_server():
    if FastMCP is None:
        raise RuntimeError(
            "FastMCP is unavailable. Install the 'mcp' package before running the Commit Migration MCP server."
        ) from IMPORT_ERROR
    return FastMCP("commit-migration")


def _tool_decorator():
    if FastMCP is None:
        def passthrough(func):
            return func
        return passthrough
    return mcp.tool()


if FastMCP is not None:
    mcp = _ensure_server()
else:  # pragma: no cover - exercised only when dependency is absent
    mcp = None


@_tool_decorator()
def analyze_commit_selection(
    repo: str | None = None,
    commits: list[str] | None = None,
    range_expr: str | None = None,
    branch: str | None = None,
    base: str | None = None,
    recent: int | None = None,
) -> dict:
    """Resolve the user's commit or branch selection and list the affected source files."""
    repo_root = normalize_repo_root(repo)
    selection = collect_selection(
        repo_root,
        commits=commits,
        range_expr=range_expr,
        branch=branch,
        base=base,
        recent=recent,
    )
    return {
        "repo_root": str(repo_root),
        "selection": selection.label,
        "current_branch": current_branch(repo_root),
        "source_files": selection.files,
        "source_file_count": len(selection.files),
    }


@_tool_decorator()
def build_android_mapping(
    repo: str | None = None,
    commits: list[str] | None = None,
    range_expr: str | None = None,
    branch: str | None = None,
    base: str | None = None,
    recent: int | None = None,
    hints_path: str | None = None,
) -> dict:
    """Build Android file and resource mapping suggestions for the selected commit or branch changes."""
    report = run_analysis(
        repo=repo,
        commits=commits,
        range_expr=range_expr,
        branch=branch,
        base=base,
        recent=recent,
        hints_path=hints_path,
    )
    return {
        "repo_root": report["repo_root"],
        "selection": report["selection"],
        "package_roots": report["package_roots"],
        "summary": report["summary"],
        "mappings": report["mappings"],
        "resource_tokens": report["resource_tokens"],
    }


@_tool_decorator()
def collect_android_followups(
    repo: str | None = None,
    commits: list[str] | None = None,
    range_expr: str | None = None,
    branch: str | None = None,
    base: str | None = None,
    recent: int | None = None,
) -> dict:
    """Generate Android-specific follow-up checks after a migration analysis."""
    repo_root = normalize_repo_root(repo)
    selection = collect_selection(
        repo_root,
        commits=commits,
        range_expr=range_expr,
        branch=branch,
        base=base,
        recent=recent,
    )
    return {
        "repo_root": str(repo_root),
        "selection": selection.label,
        "followups": [item.to_dict() for item in collect_followups(selection)],
    }


@_tool_decorator()
def analyze_android_commit_migration(
    repo: str | None = None,
    commits: list[str] | None = None,
    range_expr: str | None = None,
    branch: str | None = None,
    base: str | None = None,
    recent: int | None = None,
    hints_path: str | None = None,
) -> dict:
    """Return the combined Android commit migration report used by the skill."""
    return run_analysis(
        repo=repo,
        commits=commits,
        range_expr=range_expr,
        branch=branch,
        base=base,
        recent=recent,
        hints_path=hints_path,
    )


if __name__ == "__main__":
    if mcp is None:
        raise RuntimeError(
            "FastMCP is unavailable. Install the 'mcp' package before starting the Commit Migration MCP server."
        ) from IMPORT_ERROR
    mcp.run()
