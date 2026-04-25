from __future__ import annotations

import argparse
import importlib.resources
import json
import shutil
from pathlib import Path

from .analyzer import analyze_android_commit_migration, discover_hints_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Android commit migration analysis.")
    subparsers = parser.add_subparsers(dest="command")

    analyze = subparsers.add_parser("analyze", help="Analyze commit or branch changes for Android migration.")
    analyze.add_argument("--repo", type=Path, help="Target Android repository path. Defaults to the current directory.")
    analyze.add_argument("--commit", dest="commits", action="append", help="Commit SHA to analyze. Repeat for multiple commits.")
    analyze.add_argument("--range", dest="range_expr", help="Git range such as A..B.")
    analyze.add_argument("--branch", help="Branch to analyze against the current branch or --base.")
    analyze.add_argument("--base", help="Base ref for branch diff analysis.")
    analyze.add_argument("--recent", type=int, help="Analyze the most recent N commits from --branch.")
    analyze.add_argument("--hints", type=Path, help="Optional mapping hints JSON.")
    analyze.add_argument("--json", action="store_true", help="Print JSON.")
    analyze.add_argument("--output", type=Path, help="Write JSON output to a file.")

    init_hints = subparsers.add_parser("init-hints", help="Create a default mapping hints file in a target repository.")
    init_hints.add_argument("--repo", type=Path, required=True, help="Target Android repository path.")
    init_hints.add_argument(
        "--output",
        type=Path,
        help="Custom output path. Defaults to <repo>/.commit-migration/mapping_hints.json.",
    )
    init_hints.add_argument("--force", action="store_true", help="Overwrite the hints file if it already exists.")

    doctor = subparsers.add_parser("doctor", help="Run a basic environment and repository readiness check.")
    doctor.add_argument("--repo", type=Path, required=True, help="Target Android repository path.")
    doctor.add_argument("--json", action="store_true", help="Print JSON.")

    return parser


def validate_selection(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    count = sum(bool(value) for value in (args.commits, args.range_expr, args.branch))
    if count != 1:
        parser.error("Provide exactly one of --commit, --range, or --branch.")
    if args.recent and not args.branch:
        parser.error("--recent requires --branch.")


def render_text(report: dict) -> str:
    lines: list[str] = []
    lines.append(f"Selection: {report['selection']}")
    lines.append(f"Repo: {report['repo_root']}")
    lines.append(f"Current branch: {report['current_branch']}")
    lines.append(f"Package roots: {', '.join(report['package_roots']) or 'n/a'}")
    lines.append(f"Files: {report['source_file_count']}")
    lines.append("Summary:")
    for key in ("direct", "override", "review", "missing"):
        if key in report["summary"]:
            lines.append(f"  - {key}: {report['summary'][key]}")

    lines.append("")
    lines.append("Mappings:")
    for item in report["mappings"]:
        lines.append(f"- [{item['status']}] {item['source']}")
        if item["target"]:
            lines.append(f"    target: {item['target']}")
        if item.get("candidate_details"):
            for candidate in item["candidate_details"]:
                lines.append(
                    f"    candidate: {candidate['path']} (score={candidate['score']}, confidence={candidate['confidence']})"
                )
                for reason in candidate["reasons"]:
                    lines.append(f"      reason: {reason}")
        else:
            for candidate in item["candidates"]:
                lines.append(f"    candidate: {candidate}")
        for note in item["notes"]:
            lines.append(f"    note: {note}")

    if report["resource_tokens"]:
        lines.append("")
        lines.append("Resource tokens:")
        for token in report["resource_tokens"]:
            lines.append(f"- [{token['status']}] {token['type']}/{token['source_name']}")
            if token["mapped_name"] != token["source_name"]:
                lines.append(f"    mapped: {token['mapped_name']}")
            for candidate in token["candidates"]:
                lines.append(f"    candidate: {candidate}")

    if report["followups"]:
        lines.append("")
        lines.append("Follow-ups:")
        for item in report["followups"]:
            lines.append(f"- {item['title']}: {item['reason']}")

    return "\n".join(lines)


def default_hints_output(repo: Path) -> Path:
    return repo / ".commit-migration" / "mapping_hints.json"


def run_init_hints(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    output = args.output.resolve() if args.output else default_hints_output(repo)
    source = importlib.resources.files("commit_migration").joinpath("templates").joinpath("mapping_hints.example.json")

    if output.exists() and not args.force:
        raise FileExistsError(f"Hints file already exists: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with importlib.resources.as_file(source) as source_path:
        shutil.copyfile(source_path, output)
    print(f"Created hints file: {output}")
    return 0


def run_doctor(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    discovered_hints = discover_hints_path(repo)
    default_path = default_hints_output(repo)
    report = {
        "repo_root": str(repo),
        "exists": repo.exists(),
        "git_dir_exists": (repo / ".git").exists(),
        "manifest_exists": (repo / "app" / "src" / "main" / "AndroidManifest.xml").exists(),
        "java_root_exists": (repo / "app" / "src" / "main" / "java").exists(),
        "kotlin_root_exists": (repo / "app" / "src" / "main" / "kotlin").exists(),
        "res_root_exists": (repo / "app" / "src" / "main" / "res").exists(),
        "default_hints_path": str(default_path),
        "discovered_hints_path": str(discovered_hints) if discovered_hints else None,
        "discovered_hints_exists": bool(discovered_hints and discovered_hints.exists()),
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for key, value in report.items():
            print(f"{key}: {value}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init-hints":
        return run_init_hints(args)
    if args.command == "doctor":
        return run_doctor(args)
    if args.command != "analyze":
        parser.print_help()
        return 1

    validate_selection(args, parser)
    report = analyze_android_commit_migration(
        repo=args.repo,
        commits=args.commits,
        range_expr=args.range_expr,
        branch=args.branch,
        base=args.base,
        recent=args.recent,
        hints_path=args.hints,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
