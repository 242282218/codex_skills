# Multi-Agents Full Lifecycle System

This directory contains a strictly typed, production-ready blueprint for a 12-agent software delivery lifecycle.

## Objective

Build an autonomous software factory that bridges the gap between single-agent chatbots (like simple code generation) and full-scale engineering teams. By strictly defining **State, Nodes, and Edges**, we guarantee deterministic delivery across intake, design, implementation, testing, and operations.

## Architecture & Baselines

This architecture takes heavy inspiration from State-of-the-Art (SOTA) open-source multi-agent frameworks:

| Inspiration Source | Feature Integrated Here | Implementation Proof |
| :--- | :--- | :--- |
| **MetaGPT** | Explicit **SOPs** (Standard Operating Procedures) for Agents. | Each `A*.md` file requires a strict sequential step-by-step SOP execution. |
| **CrewAI** | Role-playing primitives. Agents aren't just LLM prompts; they are explicitly modeled personas. | Every `agents/` card defines a distinct `Profile`, `Backstory`, and `Role`. |
| **LangGraph** | Directed Acyclic Graphs (DAGs) and explicit state transition routing. | The `playbooks/full-lifecycle.md` and `HandoffTargets` rigorously map State Nodes (Agents) and Edges. |
| **AutoGen** | Group chat mechanics, but replaced with heavily structured request payloads. | `contracts/` directory ensures all inter-agent communication is typed. |

## Platform Layout

- `agents/`: 12 strict persona nodes (`A00` to `A11`). Every agent adheres to `contracts/agent-spec.schema.json`.
- `contracts/`: JSON schemas for typed JSON payloads bridging agents, restricting handoff hallucinations.
- `mappings/`: RBAC (Role-Based Access Control) for tools (`skills-map.yaml`). No agent can call a tool outside its mapped permissions.
- `playbooks/`: State machine definition. What is the DAG structure of the lifecycle?
- `governance/`: The explicit security/quality release gates required to exit a phase.
- `examples/`: Trace histories of previous successful execution loops.

## The State Workflow

1. **Intake (A00, A01)**: Triage, PRD scoping, freezing boundaries.
2. **Architecture (A02)**: API definition, tech stack lockdown, DB Schema modeling.
3. **Parallel Implementation (A03, A04, A05)**: Backend, Frontend, and Persistence code generation.
4. **Quality & Security (A06, A07)**: Automated SDET testing, static analysis, vulnerability blocking.
5. **Delivery Planning (A08, A09)**: Terraform/Docker pipelines, Datadog/ELK telemetry configuration.
6. **Code Review Gate (A10)**: Line-by-line static evaluation of A03 and A04 output.
7. **Knowledge Closure (A11)**: Archiving traces and generating Architecture Decision Records (ADRs).

## First Run Protocol

1. Read `playbooks/full-lifecycle.md` to map the DAG.
2. Invoke `A00_Supervisor` to initialize the global state memory.
3. The Supervisor must route execution using the `contracts/` structures.
