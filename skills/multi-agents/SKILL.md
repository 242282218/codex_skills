---
name: multi-agents
description: "SOTA Multi-agent software delivery orchestration blueprint (LangGraph x MetaGPT x CrewAI style) with strict State DAG, typed personas, contracts, governance gates, and hardened anti-hang execution policies for CMD/PowerShell/IDE environments."
---

# multi-agents

Use this skill when a request needs complex multi-role decomposition, deterministic phase-gated execution, strict State Graph management, **and zero-tolerance terminal hang prevention** in CMD/PowerShell/VSCode/Cursor IDE environments.

## Quick Start

1. Read `README.md` for architecture and framework theory.
2. Read `governance/gates.md` — especially the **Anti-Hang & Terminal Execution Policy** — before running any commands.
3. Read `playbooks/full-lifecycle.md` to map the DAG and understand circuit breaker branches.
4. Initialize execution by activating `agents/A00_Supervisor.md`.

## Key Assets

| Asset | Purpose |
| :--- | :--- |
| `agents/` | 12 strict persona nodes (`A00`–`A11`). Every agent has an SOP with timeout budgets. |
| `contracts/global-state.schema.json` | Single source of truth — includes `execution_limits` for circuit breaker enforcement. |
| `contracts/skill-invoke.schema.json` | Typed `SkillInvokeRequest`, `SkillInvokeResult`, and `HandoffEnvelope` — includes `retry_policy`, `timeout_seconds`, `handoff_type`. |
| `contracts/task-card.schema.json` | Typed task dispatch — `timeout_seconds` and `require_non_interactive` are REQUIRED fields. |
| `mappings/skills-map.yaml` | RBAC + `timeout_budgets` reference table + `execution_policy`. |
| `playbooks/full-lifecycle.md` | DAG with circuit breaker edges, HITL pause points, and Anti-Hang Quick Reference table. |
| `governance/gates.md` | Mandatory gate rules + per-platform (bash/PowerShell/CMD) non-interactive command patterns. |

## Global Execution Protocol (The SOTA Rules)

All agents (A00–A11) MUST adhere to these rules during execution:

1. **State Persistence**: Do not start logic until required `Input (State Memory)` artifacts exist in `GlobalState.artifacts_map`. A missing artifact = `status: "blocked"`.
2. **SOP Execution**: Execute your defined `Standard Operating Procedure (SOP)` steps sequentially. Never skip steps.
3. **Non-Interactive Enforcement**: Every terminal command MUST include headless flags (`--yes`, `CI=true`, `-y`, `--no-input`). Interactive prompts = immediate circuit breaker.
4. **Explicit Timeout Budgets**: Every terminal command MUST declare a `timeout_seconds` value from `mappings/skills-map.yaml → timeout_budgets`. Budget breach once = circuit breaker fires.
5. **Background Services**: Long-running processes (dev servers, app processes) MUST be launched in background. Verify liveness via port probe — NEVER await process exit.
6. **Output Throttling**: Commands expected to run >10s MUST redirect stdout/stderr to a log file. Ingest only `tail -50` to prevent context-buffer overflow.
7. **Circuit Breaker (Exponential Backoff)**: On failure: wait 2s → retry. On 2nd failure: wait 4s → retry. On 3rd failure: STOP. Emit `HandoffEnvelope(handoff_type="circuit_breaker")` to `A00`. On timeout: immediate circuit breaker, no retry.
8. **Structured Handoff**: Construct a `HandoffEnvelope` with `handoff_type`, `state_patch`, and (on failure) `patch_strategy`. Send to `A00` to approve the transition.
9. **RBAC Isolation**: Never invoke a skill not listed in your `Allowed Skills` (enforced by `mappings/skills-map.yaml`).
10. **Traceability**: Append `trace_id` to all files, log filenames, decisions, and handoff payloads.

## Platform-Specific Anti-Hang Cheatsheet

```powershell
# PowerShell: Run command with timeout guard
$job = Start-Job { npm install --yes }
if (-not (Wait-Job $job -Timeout 120)) {
    Stop-Job $job; Remove-Job $job
    throw "TIMEOUT — emit HandoffEnvelope circuit_breaker"
}
Get-Content install.log -Tail 50
```

```cmd
:: CMD: Run command with output redirect + error check
set CI=true
npm run build > build.log 2>&1
if %errorlevel% neq 0 ( type build.log && exit /b 1 )
type build.log | more /e +999999
```

```bash
# bash: Background server + port probe
nohup node server.js > server.log 2>&1 &
for i in {1..15}; do sleep 2; curl -sf http://localhost:3000/health && break; done \
  || (tail -50 server.log && exit 1)
```

## Notes

- Supervisor (`A00`) holds final authority. If an Implementer (A03/A04) disputes QA (A06), `A00` routes back with a mandatory `PatchStrategy` before retrying.
- `A00` tracks `execution_limits.agent_step_count`. When it reaches `max_agent_steps`, the trace is force-failed and escalated to User.
- Prefer project-level skills under `./.codex/skills` first (e.g., `00_Meta_Dispatcher`), falling back to user-level skills in `%USERPROFILE%/.codex/skills`.
