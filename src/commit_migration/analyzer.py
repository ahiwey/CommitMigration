from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from .git_ops import current_branch, run_git
from .models import AnalysisSelection, FollowupItem, MappingEntry


PACKAGE_SEGMENT_PATTERN = re.compile(r"^(com|org|io|net)$")
RESOURCE_TOKEN_PATTERN = re.compile(r"R\.(\w+)\.([A-Za-z0-9_]+)|@(\w+)/([A-Za-z0-9_]+)")
VALUE_NAME_PATTERN = re.compile(r'<(?:\w+:)?(?:item|color|string|style|dimen|integer|bool|array|string-array|plurals)\b[^>]*\bname="([A-Za-z0-9_]+)"')
DEFAULT_HINT_LOCATIONS = (
    Path(".commit-migration") / "mapping_hints.json",
    Path(".codex") / "commit-migration" / "mapping_hints.json",
    Path("tools") / "branch_apply" / "mapping_hints.json",
)


def normalize_repo_root(repo: str | Path | None) -> Path:
    return (Path(repo).resolve() if repo else Path.cwd().resolve())


def code_roots(repo_root: Path) -> list[Path]:
    return [
        repo_root / "app" / "src" / "main" / "java",
        repo_root / "app" / "src" / "main" / "kotlin",
    ]


def resource_root(repo_root: Path) -> Path:
    return repo_root / "app" / "src" / "main" / "res"


def unique_sorted(items: list[str]) -> list[str]:
    return sorted({item for item in items if item})


def unique_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def discover_hints_path(repo_root: Path) -> Path | None:
    for rel_path in DEFAULT_HINT_LOCATIONS:
        candidate = repo_root / rel_path
        if candidate.exists():
            return candidate
    return None


def load_hints(repo_root: Path, path: str | Path | None) -> tuple[dict, Path | None]:
    hint_path: Path | None
    if path:
        hint_path = Path(path)
        if not hint_path.is_absolute():
            hint_path = (Path.cwd() / hint_path).resolve()
    else:
        hint_path = discover_hints_path(repo_root)

    if not hint_path:
        return {"package_roots": {}, "path_overrides": {}, "resource_name_map": {}}, None
    if not hint_path.exists():
        return {"package_roots": {}, "path_overrides": {}, "resource_name_map": {}}, None

    with hint_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return {
        "package_roots": data.get("package_roots", {}),
        "path_overrides": data.get("path_overrides", {}),
        "resource_name_map": data.get("resource_name_map", {}),
    }, hint_path


def discover_package_roots(repo_root: Path) -> list[str]:
    counts: Counter[str] = Counter()
    for base in code_roots(repo_root):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.suffix not in {".java", ".kt"}:
                continue
            rel_parts = path.relative_to(base).parts
            if len(rel_parts) < 4:
                continue
            if not PACKAGE_SEGMENT_PATTERN.match(rel_parts[0]):
                continue
            counts["/".join(rel_parts[:3])] += 1
    return [root for root, _ in counts.most_common(12)]


def file_kind(rel_path: str) -> str:
    if rel_path.startswith("app/src/main/java/") or rel_path.startswith("app/src/main/kotlin/"):
        return "code"
    if rel_path.startswith("app/src/main/res/"):
        return "resource"
    if rel_path.endswith("AndroidManifest.xml"):
        return "manifest"
    if rel_path.endswith((".pro", ".txt")):
        return "config"
    return "other"


def source_package_root(rel_path: str) -> str | None:
    for prefix in ("app/src/main/java/", "app/src/main/kotlin/"):
        if not rel_path.startswith(prefix):
            continue
        rest = rel_path[len(prefix) :]
        parts = rest.split("/")
        if len(parts) < 4:
            return None
        if not PACKAGE_SEGMENT_PATTERN.match(parts[0]):
            return None
        return "/".join(parts[:3])
    return None


def suffix_overlap(source: Path, candidate: Path) -> int:
    overlap = 0
    for left, right in zip(reversed(source.parts), reversed(candidate.parts)):
        if left != right:
            break
        overlap += 1
    return overlap


def collect_selection(
    repo_root: Path,
    commits: list[str] | None = None,
    range_expr: str | None = None,
    branch: str | None = None,
    base: str | None = None,
    recent: int | None = None,
) -> AnalysisSelection:
    if commits:
        ordered = unique_preserving_order(commits)
        files: list[str] = []
        for commit in ordered:
            files.extend(run_git(repo_root, "diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines())
        diff_text = "\n".join(
            run_git(repo_root, "show", "--format=", "--no-ext-diff", commit) for commit in ordered
        )
        return AnalysisSelection(label=f"commits: {', '.join(ordered)}", files=unique_sorted(files), diff_text=diff_text)

    if range_expr:
        files = run_git(repo_root, "diff", "--name-only", range_expr).splitlines()
        diff_text = run_git(repo_root, "diff", "--no-ext-diff", range_expr)
        return AnalysisSelection(label=f"range: {range_expr}", files=unique_sorted(files), diff_text=diff_text)

    if branch:
        if recent:
            selected = run_git(repo_root, "rev-list", f"--max-count={recent}", branch).splitlines()
            files = []
            for commit in selected:
                files.extend(run_git(repo_root, "diff-tree", "--no-commit-id", "--name-only", "-r", commit).splitlines())
            diff_text = "\n".join(
                run_git(repo_root, "show", "--format=", "--no-ext-diff", commit) for commit in selected
            )
            return AnalysisSelection(
                label=f"branch recent commits: {branch} x {recent}",
                files=unique_sorted(files),
                diff_text=diff_text,
            )
        base_ref = base or current_branch(repo_root)
        expr = f"{base_ref}..{branch}"
        files = run_git(repo_root, "diff", "--name-only", expr).splitlines()
        diff_text = run_git(repo_root, "diff", "--no-ext-diff", expr)
        return AnalysisSelection(label=f"branch diff: {expr}", files=unique_sorted(files), diff_text=diff_text)

    raise ValueError("One of commits, range_expr, or branch is required.")


def search_code_candidates(repo_root: Path, file_name: str) -> list[str]:
    candidates: list[str] = []
    for base in code_roots(repo_root):
        if not base.exists():
            continue
        for match in base.rglob(file_name):
            candidates.append(match.relative_to(repo_root).as_posix())
    return candidates


def search_resource_candidates(repo_root: Path, name: str) -> list[str]:
    res_root = resource_root(repo_root)
    if not res_root.exists():
        return []

    exact: list[str] = []
    fuzzy: list[str] = []

    for path in res_root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        stem = path.stem
        if stem == name:
            exact.append(rel)
        elif stem.endswith(name) or name.endswith(stem) or name in stem or stem in name:
            fuzzy.append(rel)

        if path.suffix == ".xml" and path.parent.name.startswith("values"):
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for value_name in VALUE_NAME_PATTERN.findall(content):
                ref = f"{rel}#{value_name}"
                if value_name == name:
                    exact.append(ref)
                elif value_name.endswith(name) or name.endswith(value_name) or name in value_name or value_name in name:
                    fuzzy.append(ref)

    return unique_sorted(exact)[:8] if exact else unique_sorted(fuzzy)[:8]


def map_file(repo_root: Path, rel_path: str, package_roots: list[str], hints: dict) -> MappingEntry:
    kind = file_kind(rel_path)

    if rel_path in hints["path_overrides"]:
        override = hints["path_overrides"][rel_path]
        return MappingEntry(
            source=rel_path,
            kind=kind,
            status="override",
            target=override,
            notes=["Path override from mapping hints."],
        )

    if kind in {"manifest", "config", "other"}:
        target = rel_path if (repo_root / rel_path).exists() else None
        return MappingEntry(
            source=rel_path,
            kind=kind,
            status="direct" if target else "review",
            target=target,
            notes=["Same relative path exists."] if target else ["No direct target path."],
        )

    if kind == "resource":
        target = rel_path if (repo_root / rel_path).exists() else None
        if target:
            return MappingEntry(
                source=rel_path,
                kind=kind,
                status="direct",
                target=target,
                notes=["Resource path exists on current branch."],
            )
        name = Path(rel_path).stem
        candidates = search_resource_candidates(repo_root, name)
        return MappingEntry(
            source=rel_path,
            kind=kind,
            status="review" if candidates else "missing",
            candidates=candidates,
            notes=["Resource needs semantic mapping."],
        )

    source_root = source_package_root(rel_path)
    if not source_root:
        return MappingEntry(source=rel_path, kind=kind, status="review", notes=["Cannot infer source package root."])

    suffix = rel_path.split(source_root + "/", 1)[1]
    preferred_roots: list[str] = []
    if source_root in hints["package_roots"]:
        preferred_roots.append(hints["package_roots"][source_root])
    preferred_roots.extend(root for root in package_roots if root not in preferred_roots)

    for root in preferred_roots:
        candidate = rel_path.replace(source_root, root, 1)
        if (repo_root / candidate).exists():
            return MappingEntry(
                source=rel_path,
                kind=kind,
                status="direct",
                target=candidate,
                notes=["Matched by package-root replacement."],
            )

    file_name = Path(rel_path).name
    raw_candidates = search_code_candidates(repo_root, file_name)
    scored = sorted(raw_candidates, key=lambda item: suffix_overlap(Path(suffix), Path(item)), reverse=True)
    candidates = scored[:6]
    return MappingEntry(
        source=rel_path,
        kind=kind,
        status="review" if candidates else "missing",
        candidates=candidates,
        notes=["Need class or path remap."] if candidates else ["No matching filename found in current repository."],
    )


def collect_resource_tokens(repo_root: Path, diff_text: str, hints: dict) -> list[dict]:
    tokens = []
    seen: set[tuple[str, str]] = set()
    for match in RESOURCE_TOKEN_PATTERN.finditer(diff_text):
        groups = match.groups()
        res_type = groups[0] or groups[2]
        name = groups[1] or groups[3]
        if not res_type or not name:
            continue
        mapped_name = hints["resource_name_map"].get(name, name)
        key = (res_type, mapped_name)
        if key in seen:
            continue
        seen.add(key)
        candidates = search_resource_candidates(repo_root, mapped_name)
        has_exact = any(
            candidate.endswith(f"#{mapped_name}") or Path(candidate.split("#", 1)[0]).stem == mapped_name
            for candidate in candidates
        )
        tokens.append(
            {
                "type": res_type,
                "source_name": name,
                "mapped_name": mapped_name,
                "candidates": candidates,
                "status": "direct" if has_exact else ("review" if candidates else "missing"),
            }
        )
    return tokens


def collect_followups(selection: AnalysisSelection) -> list[FollowupItem]:
    files = selection.files
    diff_text = selection.diff_text
    followups: list[FollowupItem] = []

    def add(title: str, reason: str) -> None:
        if any(item.title == title for item in followups):
            return
        followups.append(FollowupItem(title=title, reason=reason))

    if any(path.endswith("AndroidManifest.xml") for path in files) or "AndroidManifest.xml" in diff_text:
        add("Manifest references", "The migration may need package, component, provider, or authority updates in AndroidManifest.xml.")

    if any("/layout/" in path or "/navigation/" in path or path.endswith(".xml") for path in files):
        add("XML component wiring", "Layout or navigation XML may contain custom View names, destination classes, or resource references.")

    if "provider" in diff_text.lower() or "authority" in diff_text.lower():
        add("Provider and authority strings", "Provider declarations and authority names often drift across Android variants.")

    if any(path.endswith((".java", ".kt")) for path in files):
        add("Imports and fully qualified names", "Equivalent migration may require class import and package rewrites across code files.")
        add("Reflection or routing strings", "Search for string-based class names, route paths, or serialized model names tied to the migrated behavior.")

    if re.search(r"proguard|consumer-rules|keep class|keepnames", diff_text, re.IGNORECASE):
        add("R8 or Proguard rules", "Class renames can leave stale keep rules after migration.")

    if re.search(r"R\.\w+\.|@\w+/", diff_text):
        add("Resource chain review", "The source diff references Android resources that may need target-branch equivalents.")

    return followups


def analyze_android_commit_migration(
    repo: str | Path | None = None,
    commits: list[str] | None = None,
    range_expr: str | None = None,
    branch: str | None = None,
    base: str | None = None,
    recent: int | None = None,
    hints_path: str | Path | None = None,
) -> dict:
    repo_root = normalize_repo_root(repo)
    hints, resolved_hints_path = load_hints(repo_root, hints_path)
    selection = collect_selection(
        repo_root,
        commits=commits,
        range_expr=range_expr,
        branch=branch,
        base=base,
        recent=recent,
    )
    package_roots = discover_package_roots(repo_root)
    mappings = [map_file(repo_root, item, package_roots, hints) for item in selection.files]
    summary = Counter(entry.status for entry in mappings)

    return {
        "repo_root": str(repo_root),
        "selection": selection.label,
        "current_branch": current_branch(repo_root),
        "resolved_hints_path": str(resolved_hints_path) if resolved_hints_path else None,
        "package_roots": package_roots,
        "source_file_count": len(selection.files),
        "summary": dict(summary),
        "mappings": [entry.to_dict() for entry in mappings],
        "resource_tokens": collect_resource_tokens(repo_root, selection.diff_text, hints),
        "followups": [item.to_dict() for item in collect_followups(selection)],
    }
