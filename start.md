请帮我在“当前项目根目录”做 Codex 初次部署。

源仓库：
https://github.com/242282218/codex_skills

要求：
1. 克隆仓库到系统临时目录（不要污染当前项目）。
2. 在当前项目根目录创建 `.codex/`（若已存在则复用）。
3. 将仓库中的以下目录复制到 `.codex/`（覆盖同名文件，但不要删除目标多余文件）：
   - core/
   - skills/
   - snippets/
   - templates/
   - rules/
4. 将仓库中的以下文件复制到 `.codex/`：
   - config.toml
   - AGENTS.md
5. 复制时排除机器产物：
   - `__pycache__/`
   - `*.pyc`
   - `*.pyo`
   - `.DS_Store`
   - `Thumbs.db`
6. 完成后输出结果清单：
   - 实际复制了哪些目录和文件
   - `.codex` 目标路径
   - 是否有缺失项或错误
7. 清理临时目录。

注意：
- 不要修改当前项目中 `.codex/` 之外的文件。
- 全程自动执行，除非遇到无法继续的错误再询问我。
