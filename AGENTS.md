# AGENTS.md - Codex Project Instructions

## Quick Start
1. New here: read [`.codex/core/AGENT.md#quick-start`](./.codex/core/AGENT.md#quick-start).
2. Mandatory rules: read [`.codex/core/RULES.md`](./.codex/core/RULES.md).
3. Engineering conventions: read [`.codex/core/CONVENTIONS.md`](./.codex/core/CONVENTIONS.md).

## Required Flow
- Before execution: propose plan, then implement after confirmation.
- During execution: small steps, verify each step.
- If blocked: switch strategy and continue; do not silently stop.

## Structure Strategy (.codex Standard)
- Git sync scope is `./.codex/` plus this `AGENTS.md`.
- Project framework files are centralized under `./.codex/`: `core/`, `skills/`, `snippets/`, `templates/`.
- Runtime skills are managed at user scope: `%USERPROFILE%\\.codex\\skills`.
- Keep links in this file relative only; never hardcode absolute local paths.

## References
- Execution framework: [`.codex/core/AGENT.md`](./.codex/core/AGENT.md)
- Rule details: [`.codex/core/RULES.md`](./.codex/core/RULES.md)
- Coding conventions: [`.codex/core/CONVENTIONS.md`](./.codex/core/CONVENTIONS.md)
