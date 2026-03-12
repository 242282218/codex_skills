from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sync_codex_repo.py"
MODULE_SPEC = importlib.util.spec_from_file_location("sync_codex_repo", SCRIPT_PATH)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
sync_codex_repo = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(sync_codex_repo)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        capture_output=True,
    )


class SyncCodexRepoTests(unittest.TestCase):
    def test_sync_selected_dry_run_does_not_modify_destination(self) -> None:
        with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as dest_dir:
            source = Path(source_dir)
            destination = Path(dest_dir)
            write_text(source / "AGENTS.md", "source agents")
            write_text(source / "core" / "AGENT.md", "agent")
            write_text(source / "core" / "RULES.md", "rules")
            write_text(source / "core" / "CONVENTIONS.md", "conventions")
            write_text(destination / "AGENTS.md", "destination agents")

            copied_dirs, copied_files, missing = sync_codex_repo.sync_selected(source, destination, dry_run=True)

            self.assertEqual(copied_dirs, 1)
            self.assertEqual(copied_files, 4)
            self.assertIn("skills", missing)
            self.assertEqual((destination / "AGENTS.md").read_text(encoding="utf-8"), "destination agents")

    def test_validate_required_paths_rejects_missing_rule_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_text(root / "AGENTS.md", "agents")
            write_text(root / "core" / "AGENT.md", "agent")

            with self.assertRaises(RuntimeError) as ctx:
                sync_codex_repo.validate_required_paths(root, "source")

            self.assertIn("core/RULES.md", str(ctx.exception))
            self.assertIn("core/CONVENTIONS.md", str(ctx.exception))

    def test_stage_selected_paths_skips_unmanaged_files(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir:
            repo = Path(repo_dir)
            git(repo, "init")
            git(repo, "config", "user.name", "Test User")
            git(repo, "config", "user.email", "test@example.com")
            write_text(repo / "AGENTS.md", "base agents")
            write_text(repo / "core" / "AGENT.md", "base agent")
            write_text(repo / "README.md", "base readme")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "init")

            write_text(repo / "AGENTS.md", "changed agents")
            write_text(repo / "README.md", "changed readme")

            sync_codex_repo.stage_selected_paths(repo)

            staged = set(git(repo, "diff", "--cached", "--name-only").stdout.splitlines())
            unstaged = set(git(repo, "diff", "--name-only").stdout.splitlines())

            self.assertEqual(staged, {"AGENTS.md"})
            self.assertEqual(unstaged, {"README.md"})

    def test_backup_selected_copies_only_managed_paths(self) -> None:
        with tempfile.TemporaryDirectory() as codex_home_dir, tempfile.TemporaryDirectory() as backup_dir:
            codex_home = Path(codex_home_dir)
            backup_root = Path(backup_dir)
            write_text(codex_home / "AGENTS.md", "agents")
            write_text(codex_home / "core" / "AGENT.md", "agent")
            write_text(codex_home / "config.toml", "secret = true")

            copied_dirs, copied_files, missing = sync_codex_repo.backup_selected(codex_home, backup_root)

            self.assertEqual(copied_dirs, 1)
            self.assertEqual(copied_files, 2)
            self.assertIn("skills", missing)
            self.assertTrue((backup_root / "AGENTS.md").exists())
            self.assertFalse((backup_root / "config.toml").exists())

    def test_remove_forbidden_public_files_deletes_config(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir:
            repo = Path(repo_dir)
            write_text(repo / "config.toml", "secret = true")

            removed = sync_codex_repo.remove_forbidden_public_files(repo)

            self.assertEqual(removed, ["config.toml"])
            self.assertFalse((repo / "config.toml").exists())

    def test_stage_selected_paths_can_stage_forbidden_file_deletions(self) -> None:
        with tempfile.TemporaryDirectory() as repo_dir:
            repo = Path(repo_dir)
            git(repo, "init")
            git(repo, "config", "user.name", "Test User")
            git(repo, "config", "user.email", "test@example.com")
            write_text(repo / "AGENTS.md", "agents")
            write_text(repo / "config.toml", "secret = true")
            git(repo, "add", ".")
            git(repo, "commit", "-m", "init")

            removed = sync_codex_repo.remove_forbidden_public_files(repo)
            sync_codex_repo.stage_selected_paths(repo, removed)

            staged = set(git(repo, "diff", "--cached", "--name-only").stdout.splitlines())

            self.assertEqual(staged, {"config.toml"})


if __name__ == "__main__":
    unittest.main()
