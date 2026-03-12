# Sample Project Flow

## Scenario

Build a simple issue tracker web app with auth, dashboard, and CI/CD.

## Trace

1. `A00` creates trace `TRACE-ISSUEAPP-001` and dispatches to `A01`.
2. `A01` returns scope with MVP features and acceptance criteria.
3. `A02` defines API resources, service boundaries, and data model shape.
4. `A03` creates backend task cards (`TASK-API-AUTH`, `TASK-API-ISSUES`).
5. `A04` creates frontend task cards (`TASK-WEB-LOGIN`, `TASK-WEB-BOARD`).
6. `A05` creates database task card (`TASK-DB-SCHEMA`).
7. `A06` attaches test plan and marks `TASK-API-AUTH` as missing rate-limit test.
8. `A07` reports a P1 finding for missing refresh token rotation.
9. `A03` updates plan and returns revised artifacts.
10. `A08` creates pipeline plan with staging and rollback.
11. `A09` adds logs/metrics/alerts plan.
12. `A10` runs review gate and emits `go`.
13. `A11` publishes runbook and ADR summary.
14. `A00` closes trace.

## Example SkillInvokeRequest

```json
{
  "kind": "SkillInvokeRequest",
  "payload": {
    "trace_id": "TRACE-ISSUEAPP-001",
    "agent_id": "A03",
    "skill": "05_Backend_Node",
    "objective": "Design API task cards for auth and issue resources",
    "payload": {
      "api_style": "REST"
    },
    "constraints": ["JWT auth", "pagination", "Output must include acceptance tests"]
  }
}
```

## Example HandoffEnvelope

```json
{
  "kind": "HandoffEnvelope",
  "payload": {
    "from": "A03",
    "to": "A06",
    "reason": "Backend task cards ready for quality gate",
    "context": {
      "task_ids": ["TASK-API-AUTH", "TASK-API-ISSUES"]
    },
    "blocking_issues": [],
    "expected_decision": "test_gate_pass_or_block"
  }
}
```
