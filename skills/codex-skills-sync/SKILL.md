---
name: codex-skills-sync
description: 同步和恢复公开复用的 Codex 模板配置。用于将 `%USERPROFILE%\\.codex` 下的 `core`、`skills`、`snippets`、`templates`、`rules` 与 `AGENTS.md` 推送到 GitHub 仓库，或从 GitHub 云端恢复到本机（覆盖不删除）。当用户提出“同步到 GitHub”“云端备份”“从仓库恢复本地 Codex 配置”时使用。
---

# codex-skills-sync

## 目标

统一管理公开复用的 Codex 模板仓库：
- `push`：本机 `%USERPROFILE%\\.codex` -> GitHub 仓库
- `restore`：GitHub 仓库 -> 本机 `%USERPROFILE%\\.codex`

默认策略是**覆盖不删除**。

## 同步范围

- 目录：`core`、`skills`、`snippets`、`templates`、`rules`
- 文件：`AGENTS.md`

说明：
- `config.toml` 不再同步，且 `push` 时会从目标仓库中移除。
- `README.md`、`start.md` 等仓库说明文件可在仓库中单独维护，不属于默认同步范围。
- 同步前会校验公开模板的规则链路：`AGENTS.md`、`core/AGENT.md`、`core/RULES.md`、`core/CONVENTIONS.md`。

## 使用步骤

1. 确认目标仓库 URL（例如：`https://github.com/242282218/codex_skills.git`）和分支（默认 `main`）。
2. 运行脚本：`scripts/sync_codex_repo.py`。
3. 根据模式选择：
   - 推送：`--mode push`
   - 恢复：`--mode restore`
4. 如需先预览，使用 `--dry-run`。
5. `restore` 默认先备份本机已管理路径；如需跳过，使用 `--no-backup`。

## 常用命令

```bash
# 推送到 GitHub（公开模板模式）
python scripts/sync_codex_repo.py --mode push --repo-url https://github.com/242282218/codex_skills.git --branch main

# 若本机未设置 Git 提交身份，可临时指定：
python scripts/sync_codex_repo.py --mode push --repo-url https://github.com/242282218/codex_skills.git --git-user-name "Your Name" --git-user-email "you@example.com"

# 从 GitHub 恢复到本机（默认先备份）
python scripts/sync_codex_repo.py --mode restore --repo-url https://github.com/242282218/codex_skills.git --branch main

# 预演 push（不提交不推送）
python scripts/sync_codex_repo.py --mode push --repo-url https://github.com/242282218/codex_skills.git --dry-run

# 预演 restore（不改本机）
python scripts/sync_codex_repo.py --mode restore --repo-url https://github.com/242282218/codex_skills.git --dry-run

# 指定 restore 备份目录
python scripts/sync_codex_repo.py --mode restore --repo-url https://github.com/242282218/codex_skills.git --backup-dir D:\\codex-backups\\public-template
```

## 默认规则

- 覆盖不删除：只复制和覆盖目标文件，不主动删除目标多余文件。
- 自动忽略机器产物：`__pycache__/`、`*.pyc`、`*.pyo`、`.DS_Store`、`Thumbs.db`。
- `push` 仅 stage 白名单路径，不再整仓 `git add -A`。
- `push` 会移除目标仓库中的 `config.toml`，避免公开仓库残留本机配置。
- `restore` 支持 `--dry-run`，默认先备份本机已管理路径。
- 若未配置 Git 身份，需传入 `--git-user-name` 和 `--git-user-email`。

## 资源

- 详细范围说明：`references/sync-scope.md`
- 执行脚本：`scripts/sync_codex_repo.py`
