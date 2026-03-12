---
name: isolated-git-publish
description: 在不修改当前本地工作目录的前提下，将目录、子项目或当前快照发布到独立 Git 仓库或远端分支。Use when 用户要求上传、发布、推送、同步、镜像或开源项目到 GitHub/GitLab/Gitee/任意 Git 远端，同时强调不要改本地文件、不要污染当前仓库、不要动现有开发环境、先做临时发布目录、临时仓库、独立仓库、隔离发布目录、发布纯净版本、清理敏感文件、清空远端后重传、覆盖远端 main/主分支、把子目录或 monorepo 子项目单独上传、把当前未提交改动打成可推送快照，或出现“临时发布目录 + 独立 git 仓库推送”“上传纯净版”“开源清理后上传”“把这个目录单独传到 GitHub”“不要碰我本地直接发上去”“子项目独立发布”“隔离推送”“纯净快照发布”等需求时使用。
---

# Isolated Git Publish

## Overview

Use this skill to create a disposable publish directory, remove local or sensitive files, initialize an independent Git repository, and optionally push it to a remote branch without touching the source working tree.

## Workflow Decision

- If the published version must include current uncommitted changes, use `copy-snapshot`.
- If the published version must come only from committed content and should respect `.gitattributes` archive rules, use `git-archive`.
- If the user needs to preserve subdirectory history in the target repository, read [references/research.md](./references/research.md) and consider `splitsh/lite` or `git-subsplit` as an advanced alternative.

## Typical Trigger Phrases

- “上传这个项目到 GitHub，但是别改我本地文件”
- “把这个目录单独发布出去”
- “做一个纯净版推到远端”
- “先清理开源版，再上传”
- “把当前快照单独推一个仓库”
- “不要污染现在这个仓库，单独发”
- “清空远端 main 后，把这个子项目传上去”
- “monorepo 里这个子目录单独开源”

## Required Sequence

1. Inspect the source directory and the target remote.
2. Read [references/cleanup-checklist.md](./references/cleanup-checklist.md) and decide whether the default exclusions are enough.
3. Run the publish script with `--dry-run` first.
4. Execute without push first when the repo is high risk or the cleanup rules changed.
5. Inspect the generated release directory and confirm it contains only releasable files.
6. Push only from the isolated release directory. Never run destructive Git operations in the source directory.
7. Verify the remote branch contents after push.

## Script

Use [scripts/publish_snapshot.py](./scripts/publish_snapshot.py) for deterministic execution.

### Quick Start

```bash
python scripts/publish_snapshot.py \
  --source "D:\PROJECT_ZZZZZZZZZ\qsm\movie-wall" \
  --mode copy-snapshot \
  --remote-url "https://github.com/owner/repo.git" \
  --branch main \
  --push force \
  --dry-run
```

```bash
python scripts/publish_snapshot.py \
  --source "D:\PROJECT_ZZZZZZZZZ\qsm\movie-wall" \
  --mode copy-snapshot \
  --remote-url "https://github.com/owner/repo.git" \
  --branch main \
  --push force
```

### Strict Committed Snapshot

When the user explicitly wants the published content to come only from committed files:

```bash
python scripts/publish_snapshot.py \
  --source "D:\PROJECT_ZZZZZZZZZ\qsm\movie-wall" \
  --mode git-archive \
  --remote-url "https://github.com/owner/repo.git" \
  --branch main \
  --push normal \
  --dry-run
```

### Important Flags

- `--dry-run`: Print the execution plan without creating the release repo.
- `--exclude PATTERN`: Add an extra exclusion glob, repeatable.
- `--keep PATTERN`: Re-include a file or path that would otherwise be excluded.
- `--exclude-file PATH`: Load extra exclusion globs from a file.
- `--push skip|normal|force`: Control whether the release repo is pushed. Default is `skip`.
- `--dest-root PATH`: Choose where the isolated release directory is created.
- `--git-user-name` / `--git-user-email`: Override author identity for the release commit.

## Guardrails

- Never delete or rewrite files in the source directory. All cleanup happens in the isolated release directory.
- Prefer `copy-snapshot` when the user wants the exact current state, including uncommitted changes.
- Prefer `git-archive` when the user wants `.gitattributes export-ignore` behavior or a release based only on committed content.
- Force push only when the user clearly intends to replace the remote branch contents.
- If the source contains secrets, review [references/cleanup-checklist.md](./references/cleanup-checklist.md) before pushing even if the defaults look sufficient.

## References

- [references/cleanup-checklist.md](./references/cleanup-checklist.md): Default open-source cleanup review list.
- [references/research.md](./references/research.md): Official Git docs and existing tools that informed this workflow.
