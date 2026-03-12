# 同步范围与策略

## 固定同步范围

- 目录：
  - `core`
  - `skills`
  - `snippets`
  - `templates`
  - `rules`
- 文件：
  - `AGENTS.md`

## 公开模板校验

- 推送和恢复前必须存在：
  - `AGENTS.md`
  - `core/AGENT.md`
  - `core/RULES.md`
  - `core/CONVENTIONS.md`

## 非同步但需要注意的仓库文件

- `README.md`、`start.md` 等仓库说明文件可以保留在公开仓库中单独维护。
- `config.toml` 不属于公开模板同步范围；若目标仓库存在该文件，`push` 会将其移除。

## 默认策略

- 覆盖不删除（overwrite without delete）
- 忽略机器产物：
  - 目录：`__pycache__`
  - 文件后缀：`.pyc`、`.pyo`
  - 文件名：`.DS_Store`、`Thumbs.db`

## Git 提交策略

- `push` 模式下：
  - 只 stage 白名单路径：`core/`、`skills/`、`snippets/`、`templates/`、`rules/`、`AGENTS.md`
  - 若无已 stage 的受管变更，不提交不推送
  - 若有变更，默认提交信息：`chore: sync public codex files`
  - 推送目标：`origin/<branch>`

## 恢复策略

- `restore` 模式从 GitHub 拉取后，复制到本机 `%USERPROFILE%\\.codex`
- 支持 `--dry-run` 预演，不改本机文件
- 默认先备份本机已管理路径，可用 `--backup-dir` 指定位置，或用 `--no-backup` 跳过
- 默认仅覆盖已同步范围，不删除本机其他文件
