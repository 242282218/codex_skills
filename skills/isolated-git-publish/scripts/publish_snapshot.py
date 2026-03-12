#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Iterable

DEFAULT_EXCLUDES = [
    ".git",
    ".git/**",
    ".hg",
    ".hg/**",
    ".svn",
    ".svn/**",
    ".idea",
    ".idea/**",
    ".vscode",
    ".vscode/**",
    ".DS_Store",
    "Thumbs.db",
    ".env",
    ".env.*",
    ".venv",
    ".venv/**",
    "venv",
    "venv/**",
    "node_modules",
    "node_modules/**",
    "__pycache__",
    "__pycache__/**",
    ".pytest_cache",
    ".pytest_cache/**",
    ".mypy_cache",
    ".mypy_cache/**",
    ".ruff_cache",
    ".ruff_cache/**",
    ".cache",
    ".cache/**",
    "dist",
    "dist/**",
    "build",
    "build/**",
    "coverage",
    "coverage/**",
    "htmlcov",
    "htmlcov/**",
    ".next",
    ".next/**",
    ".nuxt",
    ".nuxt/**",
    "playwright-report",
    "playwright-report/**",
    "test-results",
    "test-results/**",
    "output",
    "output/**",
    ".tmp",
    ".tmp/**",
    "tmp",
    "tmp/**",
    "temp",
    "temp/**",
    "*.log",
    "*.tmp",
    "*.pyc",
    "*.pyo",
    "*.sqlite-shm",
    "*.sqlite-wal",
    "*.db-shm",
    "*.db-wal",
]

DEFAULT_KEEP = [
    ".env.example",
    ".env.sample",
    ".env.template",
    ".gitignore",
    ".gitattributes",
]


@dataclass
class CopyStats:
    copied_files: int = 0
    copied_dirs: int = 0
    excluded: list[str] = field(default_factory=list)

    def remember_exclusion(self, rel_path: str) -> None:
        if len(self.excluded) < 50:
            self.excluded.append(rel_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create an isolated publish directory and optionally push it to a remote branch."
    )
    parser.add_argument("--source", required=True, help="Source directory to publish.")
    parser.add_argument(
        "--mode",
        choices=("copy-snapshot", "git-archive"),
        default="copy-snapshot",
        help="Snapshot mode. copy-snapshot includes uncommitted changes; git-archive uses committed content only.",
    )
    parser.add_argument(
        "--dest-root",
        default=str(Path(tempfile.gettempdir()) / "isolated-git-publish"),
        help="Root directory for generated release directories.",
    )
    parser.add_argument("--name", help="Release directory name prefix. Defaults to source directory name.")
    parser.add_argument("--branch", default="main", help="Target branch name for the release repo.")
    parser.add_argument("--remote-url", help="Remote URL for push.")
    parser.add_argument(
        "--push",
        choices=("skip", "normal", "force"),
        default="skip",
        help="Push mode. skip prepares the release repo without pushing.",
    )
    parser.add_argument(
        "--commit-message",
        default="chore: publish clean snapshot",
        help="Commit message used in the isolated release repo.",
    )
    parser.add_argument("--exclude", action="append", default=[], help="Extra exclusion glob. Repeatable.")
    parser.add_argument("--keep", action="append", default=[], help="Extra keep glob. Repeatable.")
    parser.add_argument("--exclude-file", help="Path to a newline-separated exclusion file.")
    parser.add_argument("--git-user-name", help="Override Git author name for the release repo.")
    parser.add_argument("--git-user-email", help="Override Git author email for the release repo.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the execution plan without creating or pushing the release repo.",
    )
    return parser.parse_args()


def load_patterns(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    excludes = list(DEFAULT_EXCLUDES)
    keeps = list(DEFAULT_KEEP)
    excludes.extend(args.exclude)
    keeps.extend(args.keep)

    if args.exclude_file:
        for line in Path(args.exclude_file).read_text(encoding="utf-8").splitlines():
            entry = line.strip()
            if not entry or entry.startswith("#"):
                continue
            excludes.append(entry)

    return normalize_patterns(excludes), normalize_patterns(keeps)


def normalize_patterns(patterns: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for pattern in patterns:
        item = pattern.replace("\\", "/").strip()
        if item:
            normalized.append(item)
    return normalized


def matches_any(rel_path: str, patterns: Iterable[str]) -> bool:
    posix_path = rel_path.replace("\\", "/")
    basename = PurePosixPath(posix_path).name
    for pattern in patterns:
        if fnmatch.fnmatch(posix_path, pattern):
            return True
        if "/" not in pattern and fnmatch.fnmatch(basename, pattern):
            return True
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            if posix_path == prefix or posix_path.startswith(f"{prefix}/"):
                return True
    return False


def should_exclude(rel_path: str, excludes: list[str], keeps: list[str]) -> bool:
    if matches_any(rel_path, keeps):
        return False
    return matches_any(rel_path, excludes)


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_release_dir(dest_root: Path, name: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_name = f"{name}-{timestamp}"
    for suffix in range(0, 1000):
        candidate = dest_root / base_name if suffix == 0 else dest_root / f"{base_name}-{suffix:02d}"
        try:
            candidate.mkdir(parents=True, exist_ok=False)
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError(f"Unable to allocate a unique release directory under {dest_root}")


def copy_snapshot(source_dir: Path, release_dir: Path, excludes: list[str], keeps: list[str]) -> CopyStats:
    stats = CopyStats()

    for current_root, dirs, files in os.walk(source_dir):
        current_root_path = Path(current_root)
        rel_root = current_root_path.relative_to(source_dir)
        rel_root_str = "" if rel_root == Path(".") else rel_root.as_posix()

        kept_dirs: list[str] = []
        for directory in dirs:
            rel_path = directory if not rel_root_str else f"{rel_root_str}/{directory}"
            if should_exclude(rel_path, excludes, keeps):
                stats.remember_exclusion(rel_path)
                continue
            kept_dirs.append(directory)
        dirs[:] = kept_dirs

        target_root = release_dir if rel_root_str == "" else release_dir / rel_root
        ensure_directory(target_root)

        for file_name in files:
            rel_path = file_name if not rel_root_str else f"{rel_root_str}/{file_name}"
            if should_exclude(rel_path, excludes, keeps):
                stats.remember_exclusion(rel_path)
                continue
            source_file = current_root_path / file_name
            target_file = target_root / file_name
            shutil.copy2(source_file, target_file)
            stats.copied_files += 1

    for path in release_dir.rglob("*"):
        if path.is_dir():
            stats.copied_dirs += 1

    return stats


def run_git(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def find_git_root(source_dir: Path) -> Path:
    output = run_git(["rev-parse", "--show-toplevel"], source_dir)
    return Path(output)


def export_git_archive(source_dir: Path, release_dir: Path) -> None:
    repo_root = find_git_root(source_dir)
    relative_source = source_dir.relative_to(repo_root)
    tree_ish = "HEAD" if str(relative_source) == "." else f"HEAD:{relative_source.as_posix()}"
    archive_path = release_dir.parent / f"{release_dir.name}.zip"

    try:
        run_git(["archive", "--format=zip", "--output", str(archive_path), tree_ish], repo_root)
        shutil.unpack_archive(str(archive_path), str(release_dir))
    finally:
        if archive_path.exists():
            archive_path.unlink()


def prune_release_dir(release_dir: Path, excludes: list[str], keeps: list[str], stats: CopyStats) -> None:
    for path in sorted(release_dir.rglob("*"), reverse=True):
        rel_path = path.relative_to(release_dir).as_posix()
        if should_exclude(rel_path, excludes, keeps):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
            stats.remember_exclusion(rel_path)


def detect_git_identity(args: argparse.Namespace, source_dir: Path) -> tuple[str, str]:
    name = args.git_user_name
    email = args.git_user_email

    if not name:
        try:
            name = run_git(["config", "user.name"], source_dir)
        except subprocess.CalledProcessError:
            name = "Codex Publisher"
    if not email:
        try:
            email = run_git(["config", "user.email"], source_dir)
        except subprocess.CalledProcessError:
            email = "codex@example.local"
    return name, email


def init_release_repo(
    release_dir: Path,
    branch: str,
    commit_message: str,
    remote_url: str | None,
    push_mode: str,
    git_user_name: str,
    git_user_email: str,
) -> None:
    run_git(["init"], release_dir)
    run_git(["checkout", "--orphan", branch], release_dir)
    run_git(["add", "-A"], release_dir)
    subprocess.run(
        [
            "git",
            "-c",
            f"user.name={git_user_name}",
            "-c",
            f"user.email={git_user_email}",
            "commit",
            "--allow-empty",
            "-m",
            commit_message,
        ],
        cwd=str(release_dir),
        check=True,
        capture_output=True,
        text=True,
    )

    if remote_url:
        run_git(["remote", "add", "origin", remote_url], release_dir)

    if push_mode == "normal":
        run_git(["push", "origin", f"HEAD:{branch}"], release_dir)
    elif push_mode == "force":
        run_git(["push", "--force", "origin", f"HEAD:{branch}"], release_dir)


def build_plan(args: argparse.Namespace, source_dir: Path, release_dir: Path, excludes: list[str], keeps: list[str]) -> dict:
    return {
        "source": str(source_dir),
        "mode": args.mode,
        "release_dir": str(release_dir),
        "remote_url": args.remote_url,
        "branch": args.branch,
        "push": args.push,
        "exclude_count": len(excludes),
        "keep_count": len(keeps),
    }


def main() -> int:
    args = parse_args()
    source_dir = Path(args.source).expanduser().resolve()

    if not source_dir.exists():
        print(json.dumps({"error": f"Source directory not found: {source_dir}"}, ensure_ascii=False))
        return 1
    if not source_dir.is_dir():
        print(json.dumps({"error": f"Source path is not a directory: {source_dir}"}, ensure_ascii=False))
        return 1
    if args.push != "skip" and not args.remote_url:
        print(json.dumps({"error": "--remote-url is required when --push is not skip"}, ensure_ascii=False))
        return 1

    excludes, keeps = load_patterns(args)
    dest_root = Path(args.dest_root).expanduser().resolve()
    ensure_directory(dest_root)
    release_name = args.name or source_dir.name
    release_dir = create_release_dir(dest_root, release_name)

    plan = build_plan(args, source_dir, release_dir, excludes, keeps)
    if args.dry_run:
        print(json.dumps({"dry_run": True, "plan": plan}, ensure_ascii=False, indent=2))
        return 0

    stats = CopyStats()
    if args.mode == "copy-snapshot":
        stats = copy_snapshot(source_dir, release_dir, excludes, keeps)
    else:
        export_git_archive(source_dir, release_dir)
        prune_release_dir(release_dir, excludes, keeps, stats)
        stats.copied_files = sum(1 for path in release_dir.rglob("*") if path.is_file())
        stats.copied_dirs = sum(1 for path in release_dir.rglob("*") if path.is_dir())

    git_user_name, git_user_email = detect_git_identity(args, source_dir)
    init_release_repo(
        release_dir=release_dir,
        branch=args.branch,
        commit_message=args.commit_message,
        remote_url=args.remote_url,
        push_mode=args.push,
        git_user_name=git_user_name,
        git_user_email=git_user_email,
    )

    result = {
        "dry_run": False,
        "plan": plan,
        "release_dir": str(release_dir),
        "copied_files": stats.copied_files,
        "copied_dirs": stats.copied_dirs,
        "excluded_examples": stats.excluded,
        "git_user_name": git_user_name,
        "git_user_email": git_user_email,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
