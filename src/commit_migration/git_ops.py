from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def current_branch(repo_root: Path) -> str:
    return run_git(repo_root, "rev-parse", "--abbrev-ref", "HEAD").strip()
