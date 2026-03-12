# Governance Gates & Execution Policies

## Severity Model

- `P0`: Critical release blocker — execution halts immediately, circuit breaker fires
- `P1`: High severity, must be fixed before production — blocks current gate
- `P2`: Important, can be scheduled — logged but does not block
- `P3`: Nice-to-have — advisory only

---

## Anti-Hang & Terminal Execution Policy (CRITICAL — ALL AGENTS MUST COMPLY)

> **Source inspiration**: LangGraph's `ToolNode` retry policy, MetaGPT's executable feedback loop, CrewAI's loop detection, and industry subprocess management best practices.

To prevent the Multi-Agent system from hanging indefinitely in the IDE (VSCode/Trae/Cursor) or terminal (CMD/PowerShell) environments, the following execution rules are **mandatory** for ALL Agents (A00–A11):

### Rule 1 — Non-Interactive Enforcement (ZERO tolerance for interactive prompts)

Never run commands that prompt for user input (`Y/N`, passwords, selections, confirmations). Always use headless/silent flags:

| Runtime | Command Pattern | Anti-hang Flag |
| :--- | :--- | :--- |
| Node/NPM | `npm install` | `npm install --no-audit --no-fund --yes` |
| Node/NPX | `npx <pkg>` | `npx --yes <pkg>` |
| Python pip | `pip install` | `pip install -q --no-input` |
| Python runners | `python setup.py` | `PYTHONUNBUFFERED=1 python -u setup.py` |
| Git | `git commit` | `git commit --no-edit -m "msg"` or `git commit --allow-empty` |
| Git merge | `git merge` | `git merge --no-edit` |
| Linux apt | `apt-get install` | `DEBIAN_FRONTEND=noninteractive apt-get install -y` |
| Docker build | `docker build` | `docker build --no-cache --progress=plain` |
| Prisma | `prisma migrate` | `npx prisma migrate deploy` (non-interactive variant) |
| Jest | `jest` | `CI=true jest --passWithNoTests --forceExit` |
| Playwright | `playwright test` | `npx playwright test --reporter=list` (CI mode auto-detects `CI=true`) |
| Vitest | `vitest` | `vitest run --reporter=verbose` |

**PowerShell / Windows CMD specific rules:**
```powershell
# Background job with timeout guard (PowerShell)
$job = Start-Job { npm run build }
$completed = Wait-Job $job -Timeout 120
if (-not $completed) {
    Stop-Job $job; Remove-Job $job
    Write-Error "BUILD TIMEOUT: escalate via HandoffEnvelope with blocking_issues"
    exit 1
}

# Start-Process non-blocking pattern for long-running servers
Start-Process -FilePath "node" -ArgumentList "server.js" -NoNewWindow -PassThru | Out-Null

# Verify port liveness instead of waiting for process end
$ready = $false
for ($i=0; $i -lt 15; $i++) {
  Start-Sleep -Seconds 2
  try { (New-Object Net.Sockets.TcpClient("localhost", 3000)).Close(); $ready=$true; break } catch {}
}
if (-not $ready) { Write-Error "Service failed to start on port 3000"; exit 1 }
```

```cmd
:: CMD background execution + timeout
start /b cmd /c "npm run dev > dev.log 2>&1"
timeout /t 10 /nobreak >nul
curl -s http://localhost:3000/health || (echo STARTUP FAILED && exit /b 1)
```

### Rule 2 — Explicit Timeout Budgets (Per Agent Category)

Every terminal execution MUST declare an expected timeout budget. If exceeded once → escalate immediately.

| Agent | Operation Category | Max Timeout |
| :--- | :--- | :--- |
| A03/A04 | `npm install` / `pip install` | 120s |
| A03/A04 | Build/Compile (`tsc`, `vite build`) | 180s |
| A03/A04 | Unit Test Suite | 90s |
| A05 | DB Migration | 60s |
| A06 | E2E Test Suite (Playwright/Cypress) | 300s |
| A06 | Fuzz/Load test | 120s |
| A07 | Static analysis scan | 90s |
| A08 | Docker build | 300s |
| A08 | `terraform plan` | 120s |
| A09 | Telemetry health check | 30s |
| Any | Port liveness probe (`curl`) | 30s total (15 × 2s retry) |

### Rule 3 — Background Services: Detach + Probe (NOT wait-for-exit)

Long-running watch processes (e.g., `npm run dev`, `uvicorn app:main`, `python app.py`) MUST NOT be awaited synchronously.

**Correct pattern:**
1. Launch process in background / detached state
2. Redirect stdout+stderr to a log file (`> service.log 2>&1`)
3. Poll the health endpoint or port with a timeout loop (max 15 retries × 2s)
4. Read only the TAIL of the log file on success/failure to avoid context overflow
5. If port check fails after timeout → kill process group → escalate

**Anti-pattern (FORBIDDEN):**
```bash
# ❌ NEVER DO THIS — blocks agent context indefinitely
npm run dev
```

### Rule 4 — Output Throttling (Context-Buffer Protection)

For commands that produce massive logs (e.g., recursive `grep`, large test suites, `npm install` verbose):

```bash
# Redirect to log file, read only tail
npm install --yes > install.log 2>&1
tail -50 install.log
```

```powershell
# PowerShell equivalent
npm install --yes *> install.log
Get-Content install.log -Tail 50
```

- **Never** stream raw build output directly into agent context
- **Always** store to `<trace_id>_<operation>.log` named files during execution
- **Max lines** to ingest per operation: 100 lines (head OR tail, not both)

### Rule 5 — Circuit Breaker (Exponential Backoff + Fail-Fast)

Inspired by LangGraph's `ToolNode` retry policy and CrewAI's loop detection:

```
Attempt 1: Execute → on failure → wait 2s → retry
Attempt 2: Execute → on failure → wait 4s → retry  
Attempt 3: Execute → on failure → STOP. DO NOT RETRY.
           → Generate HandoffEnvelope with blocking_issues populated
           → Set GlobalState.status = "blocked"
           → Escalate to A00 immediately
```

**Rules:**
- Max retry attempts: **3** (including initial attempt)
- Backoff multiplier: **2× (exponential)**
- On 3rd failure: circuit breaker fires → **never** attempt a 4th silent retry
- If a command timed out on attempt 1: **immediately fire circuit breaker** (no retry for timeout failures)

### Rule 6 — State Integrity on Failure

When a circuit breaker fires or a timeout kills a process:
1. Write a partial result marker to `GlobalState.errors[]` with `severity: "P1"`
2. Include `patch_strategy` field describing exact intent + failure reason
3. The agent MUST NOT silently move to next SOP step
4. Send `HandoffEnvelope` to `A00` with `blocking_issues` fully populated
5. `A00` will decide: re-route to same implementer (with `PatchStrategy`) OR escalate to `User`

---

## Mandatory Gates

### 1 — Scope Gate
- **Owner**: `A01`
- **Condition**: PRD JSON generated; `Acceptance Criteria` defined (minimum 3 items); In-Scope/Out-of-Scope matrix complete.
- **HITL Required**: **YES** — Supervisor MUST set `status: "paused_for_human"`. No autonomous execution until user sends `status: "running"` patch.
- **Artifacts Required**: `artifacts_map.prd` must be non-null.

### 2 — Architecture Gate
- **Owner**: `A02`
- **Condition**: OpenAPI 3.0 spec AND Mermaid DB schema resolved; formal contracts written to `artifacts_map`.
- **HITL Required**: **YES** — Business and Technical owners must accept the system blueprint before any implementation begins.
- **Artifacts Required**: `artifacts_map.api_spec` AND `artifacts_map.db_schema` must be non-null.

### 3 — Test Gate
- **Owner**: `A06`
- **Condition**: Test plan contains unit/integration/e2e strategy; non-interactive execution plan defined; ALL tests runnable in `CI=true` headless mode without blocking.
- **HITL Required**: NO.
- **Artifacts Required**: `artifacts_map.test_plan` must be non-null.

### 4 — Security Gate
- **Owner**: `A07`
- **Condition**: Authentication, authorization, data protection checks complete; zero P0 or P1 findings.
- **HITL Required**: NO.
- **Artifacts Required**: `artifacts_map.security_report` must be non-null.

### 5 — Delivery Gate
- **Owner**: `A08`
- **Condition**: CI/CD, rollback strategy, and headless-build configs defined; all scripts verified non-interactive.
- **HITL Required**: **YES** — Explicit final dry-run confirmation required before `terraform apply` or `kubectl deploy`.
- **Artifacts Required**: `artifacts_map.devops_configs` must be non-null.

### 6 — Review Gate
- **Owner**: `A10`
- **Condition**: No unresolved P0/P1 findings; cyclomatic complexity within acceptable bounds; implementation matches architecture contracts.
- **HITL Required**: NO.
- **Artifacts Required**: `artifacts_map.code_review_report` must be non-null.

### 7 — Observability Gate
- **Owner**: `A09`
- **Condition**: Key signals mapped (SLIs/SLOs); alert ownership defined; trace_id propagation verified across all service boundaries.
- **HITL Required**: NO.
- **Artifacts Required**: `artifacts_map.observability_plan` must be non-null.

---

## Supervisor Enforcement

- `A00` is the **only** agent allowed to mutate `current_stage` in `GlobalState`.
- Any gate with `HITL Required: YES` mandates setting `GlobalState.status = "paused_for_human"`. All further autonomous triggers are blocked until the user submits a `status: "running"` patch.
- Missing mandatory artifacts → `GlobalState.status = "blocked"`.
- `A00` instantly fails the trace if an agent enters a terminal timeout loop (circuit breaker threshold reached).
- `A00` monitors `GlobalState.execution_limits.max_agent_steps` and halts if exceeded.

## Evidence Requirements

- Every gate emits a **machine-readable decision record** (JSON-serializable).
- Every decision record includes: `trace_id`, `gate_name`, `owner_agent`, `decision` (`pass`|`fail`|`blocked`), `timestamp`, `artifact_links[]`, and `blocking_issues[]`.
- Any gate failure updates `GlobalState.errors[]` before handoff to `A00`.
