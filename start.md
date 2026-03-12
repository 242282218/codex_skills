# Codex 公开模板启动提示词

你现在的任务是：在“当前项目根目录”为 Codex 部署公开复用模板。

## 源仓库

- 仓库：`https://github.com/242282218/codex_skills`
- 分支：`main`

## 目标结果

部署完成后，当前项目根目录下必须存在：

- `.codex/AGENTS.md`
- `.codex/core/`
- `.codex/rules/`
- `.codex/skills/`
- `.codex/snippets/`
- `.codex/templates/`

其中 `.codex/AGENTS.md` 是入口文件。后续规则链路为：

- `.codex/AGENTS.md`
- `.codex/core/AGENT.md`
- `.codex/core/RULES.md`
- `.codex/core/CONVENTIONS.md`

## 执行要求

1. 将源仓库克隆到系统临时目录，不要污染当前项目目录。
2. 在当前项目根目录创建 `.codex/`；如果已存在则复用。
3. 从仓库根目录复制以下目录到当前项目的 `.codex/`：
   - `core/`
   - `rules/`
   - `skills/`
   - `snippets/`
   - `templates/`
4. 从仓库根目录复制以下文件到当前项目的 `.codex/`：
   - `AGENTS.md`
5. 复制策略为“覆盖不删除”：
   - 覆盖同名文件
   - 不删除 `.codex/` 中未被本次复制覆盖的其他文件
6. 复制时必须排除机器产物：
   - `__pycache__/`
   - `*.pyc`
   - `*.pyo`
   - `.DS_Store`
   - `Thumbs.db`
7. 不要复制 `config.toml`。
8. 复制完成后，校验以下文件必须存在：
   - `.codex/AGENTS.md`
   - `.codex/core/AGENT.md`
   - `.codex/core/RULES.md`
   - `.codex/core/CONVENTIONS.md`
9. 清理临时目录。

## 约束

- 只允许修改当前项目根目录下的 `.codex/`。
- 不要修改当前项目中 `.codex/` 之外的任何文件。
- 中文文件统一按 UTF-8 读写与输出。
- 除非出现无法继续的阻塞错误，否则直接执行，不要反复询问。

## 完成后输出

完成后请输出一份简明结果，包含：

- `.codex` 的实际目标路径
- 实际复制的目录列表
- 实际复制的文件列表
- 是否发现缺失项
- 是否发现错误
- 提示我从 `.codex/AGENTS.md` 开始使用
