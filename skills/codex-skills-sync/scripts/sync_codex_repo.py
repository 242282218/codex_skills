#!/usr/bin/env python3
"""
Sync selected public Codex files between local ~/.codex and a Git repository.

Modes:
- push:    local codex -> repo (commit and push when managed paths changed)
- restore: repo -> local codex

Default strategy: overwrite without delete.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

INCLUDE_DIRS = ["core", "skills", "snippets", "templates", "rules"]
INCLUDE_FILES = ["AGENTS.md"]
REQUIRED_PUBLIC_PATHS = [
    "AGENTS.md",
    "core/AGENT.md",
    "core/RULES.md",
    "core/CONVENTIONS.md",
]
FORBIDDEN_PUBLIC_FILES = ["config.toml"]
EXCLUDE_DIR_NAMES = {"__pycache__", ".git"}
EXCLUDE_FILE_NAMES = {".DS_Store", "Thumbs.db"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def log(msg: str) -> None:
    print(msg)


def run(cmd: list[str], cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
        capture_output=capture,
    )


def is_excluded_file(path: Path) -> bool:
    if path.name in EXCLUDE_FILE_NAMES:
        return True
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    return False


def managed_stage_paths() -> list[str]:
    paths = set(INCLUDE_DIRS)
    for item in INCLUDE_FILES:
        paths.add(Path(item).parts[0])
    return sorted(paths)


def validate_required_paths(root: Path, label: str) -> None:
    missing = [path for path in REQUIRED_PUBLIC_PATHS if not (root / path).is_file()]
    if missing:
        raise RuntimeError(f"Required public Codex paths missing from {label}: {', '.join(missing)}")


def copy_dir(src: Path, dst: Path, *, dry_run: bool = False) -> int:
    copied = 0
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIR_NAMES]
        root_path = Path(root)
        rel = root_path.relative_to(src)
        out_dir = dst / rel
        if not dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
        for fname in files:
            src_file = root_path / fname
            if is_excluded_file(src_file):
                continue
            dst_file = out_dir / fname
            if not dry_run:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
            copied += 1
    return copied


def copy_file(src: Path, dst: Path, *, dry_run: bool = False) -> int:
    if not src.exists() or not src.is_file():
        return 0
    if is_excluded_file(src):
        return 0
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return 1


def sync_selected(src_root: Path, dst_root: Path, *, dry_run: bool = False) -> tuple[int, int, list[str]]:
    copied_dirs = 0
    copied_files = 0
    missing: list[str] = []

    for directory in INCLUDE_DIRS:
        src_dir = src_root / directory
        dst_dir = dst_root / directory
        if src_dir.exists() and src_dir.is_dir():
            copied_files += copy_dir(src_dir, dst_dir, dry_run=dry_run)
            copied_dirs += 1
        else:
            missing.append(directory)

    for file_path in INCLUDE_FILES:
        src_file = src_root / file_path
        dst_file = dst_root / file_path
        if src_file.exists() and src_file.is_file():
            copied_files += copy_file(src_file, dst_file, dry_run=dry_run)
        else:
            missing.append(file_path)

    return copied_dirs, copied_files, missing


def backup_selected(src_root: Path, backup_root: Path) -> tuple[int, int, list[str]]:
    return sync_selected(src_root, backup_root, dry_run=False)


def remove_forbidden_public_files(root: Path) -> list[str]:
    removed: list[str] = []
    for file_path in FORBIDDEN_PUBLIC_FILES:
        target = root / file_path
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            removed.append(file_path)
    return removed


def stage_selected_paths(repo_path: Path, extra_paths: list[str] | None = None) -> list[str]:
    stage_paths = [path for path in managed_stage_paths() if (repo_path / path).exists()]
    if extra_paths:
        for path in extra_paths:
            if path not in stage_paths:
                stage_paths.append(path)
    if stage_paths:
        run(["git", "add", "--", *stage_paths], cwd=repo_path)
    return stage_paths


def prepare_repo(repo_url: str, branch: str, repo_dir: Path | None) -> tuple[Path, Path | None]:
    """Return (repo_path, temp_dir_for_cleanup)."""
    if repo_dir is not None:
        repo_dir.mkdir(parents=True, exist_ok=True)
        if (repo_dir / ".git").exists():
            run(["git", "fetch", "origin"], cwd=repo_dir)
            run(["git", "checkout", branch], cwd=repo_dir)
            run(["git", "pull", "--ff-only", "origin", branch], cwd=repo_dir)
        else:
            run(["git", "clone", "--branch", branch, repo_url, str(repo_dir)])
        return repo_dir, None

    temp_dir = Path(tempfile.mkdtemp(prefix="codex_skills_sync_"))
    repo_path = temp_dir / "repo"
    run(["git", "clone", "--depth", "1", "--branch", branch, repo_url, str(repo_path)])
    return repo_path, temp_dir


def git_has_staged_changes(repo_path: Path) -> bool:
    result = run(["git", "diff", "--cached", "--name-only"], cwd=repo_path, capture=True)
    return bool(result.stdout.strip())


def get_git_config(repo_path: Path, key: str) -> str:
    result = subprocess.run(
        ["git", "config", "--get", key],
        cwd=str(repo_path),
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def ensure_git_identity(repo_path: Path, args: argparse.Namespace) -> None:
    if args.git_user_name:
        run(["git", "config", "user.name", args.git_user_name], cwd=repo_path)
    if args.git_user_email:
        run(["git", "config", "user.email", args.git_user_email], cwd=repo_path)

    user_name = get_git_config(repo_path, "user.name")
    user_email = get_git_config(repo_path, "user.email")
    if user_name and user_email:
        return

    raise RuntimeError(
        "Git user identity is missing. Set global git config or pass "
        "--git-user-name and --git-user-email."
    )


def default_backup_dir(codex_home: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return codex_home / "_restore_backups" / timestamp


def do_push(args: argparse.Namespace) -> int:
    codex_home = Path(args.codex_home).expanduser().resolve()
    if not codex_home.exists():
        raise FileNotFoundError(f"Local codex directory not found: {codex_home}")
    validate_required_paths(codex_home, "local codex home")

    repo_path, temp_dir = prepare_repo(args.repo_url, args.branch, Path(args.repo_dir).resolve() if args.repo_dir else None)
    try:
        copied_dirs, copied_files, missing = sync_selected(codex_home, repo_path)
        removed = remove_forbidden_public_files(repo_path)
        log(f"[INFO] Copied dirs: {copied_dirs}, files: {copied_files}")
        if missing:
            log("[WARN] Missing from source (skipped): " + ", ".join(missing))
        if removed:
            log("[INFO] Removed forbidden public files: " + ", ".join(removed))

        stage_selected_paths(repo_path, removed)
        if not git_has_staged_changes(repo_path):
            log("[INFO] No managed changes detected. Nothing to commit.")
            return 0

        if args.dry_run:
            log("[DRY-RUN] Managed changes detected. Commit/push skipped.")
            return 0

        ensure_git_identity(repo_path, args)
        commit_msg = args.commit_message or "chore: sync public codex files"
        run(["git", "commit", "-m", commit_msg], cwd=repo_path)
        run(["git", "push", "origin", args.branch], cwd=repo_path)
        log(f"[OK] Pushed to {args.repo_url} ({args.branch})")
        return 0
    finally:
        if temp_dir is not None:
            shutil.rmtree(temp_dir, ignore_errors=True)


def do_restore(args: argparse.Namespace) -> int:
    codex_home = Path(args.codex_home).expanduser().resolve()
    codex_home.mkdir(parents=True, exist_ok=True)

    repo_path, temp_dir = prepare_repo(args.repo_url, args.branch, Path(args.repo_dir).resolve() if args.repo_dir else None)
    try:
        validate_required_paths(repo_path, "repo")
        copied_dirs, copied_files, missing = sync_selected(repo_path, codex_home, dry_run=args.dry_run)
        if args.dry_run:
            log(f"[DRY-RUN] Restore preview dirs: {copied_dirs}, files: {copied_files}")
            if missing:
                log("[WARN] Missing from repo (skipped): " + ", ".join(missing))
            return 0

        if not args.no_backup:
            backup_dir = Path(args.backup_dir).expanduser().resolve() if args.backup_dir else default_backup_dir(codex_home)
            backup_dirs, backup_files, _ = backup_selected(codex_home, backup_dir)
            log(f"[INFO] Backed up dirs: {backup_dirs}, files: {backup_files} -> {backup_dir}")

        log(f"[OK] Restored dirs: {copied_dirs}, files: {copied_files}")
        if missing:
            log("[WARN] Missing from repo (skipped): " + ", ".join(missing))
        return 0
    finally:
        if temp_dir is not None:
            shutil.rmtree(temp_dir, ignore_errors=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync selected public Codex files with a Git repo.")
    parser.add_argument("--mode", choices=["push", "restore"], required=True)
    parser.add_argument("--repo-url", default="https://github.com/242282218/codex_skills.git")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--codex-home", default=str(Path.home() / ".codex"))
    parser.add_argument("--repo-dir", help="Use an existing local repo directory (optional).")
    parser.add_argument("--commit-message", help="Commit message for push mode.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying the target or pushing.",
    )
    parser.add_argument("--git-user-name", help="Git user.name for commit (push mode).")
    parser.add_argument("--git-user-email", help="Git user.email for commit (push mode).")
    parser.add_argument("--backup-dir", help="Backup destination for restore mode.")
    parser.add_argument("--no-backup", action="store_true", help="Skip local backup before restore.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log(f"[INFO] mode={args.mode} repo={args.repo_url} branch={args.branch}")
    if args.mode == "push":
        return do_push(args)
    return do_restore(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(f"[ERROR] Command failed: {' '.join(exc.cmd)}\n")
        if exc.stdout:
            sys.stderr.write(exc.stdout + "\n")
        if exc.stderr:
            sys.stderr.write(exc.stderr + "\n")
        raise
    except Exception as exc:
        sys.stderr.write(f"[ERROR] {exc}\n")
        raise
