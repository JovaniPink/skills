---
name: plan-execution
description: Execute a named, approved implementation plan with checkpoints, validation, deviation tracking, and strict stopping boundaries. Invoke explicitly when the user authorizes implementation against an identified plan.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.4.0"
  plugin: "jovanipink-engineering"
  invocation: "explicit"
  provenance: "original"
  risk_class: "bounded-execution"
disable-model-invocation: true
---

# Plan Execution

Implement an approved plan without silently changing its scope or authority.

## Preconditions

Confirm the exact plan, repository, branch, authorized actions, excluded actions, and required checkpoints. If the plan is missing, materially ambiguous, or no longer matches the system, stop and report the gap.

## Workflow

1. Establish a clean evidence baseline: branch, revision, worktree state, relevant checks, and known unrelated changes.
2. Translate the plan into a tracked sequence and mark only one dependent step active at a time.
3. Implement the smallest coherent change while preserving unrelated work.
4. Run the planned validation after each risk-bearing checkpoint.
5. Record deviations with cause, impact, evidence, and whether they remain within authority.
6. Stop for approval when a deviation changes scope, interface, data authority, security posture, cost, publication, deployment, or destructive behavior.
7. Reconcile completed steps, remaining work, validation, and unresolved risk against the original plan.

## Boundaries

- Explicit invocation authorizes plan execution only, not push, PR creation, merge, deployment, deletion, or external communication unless those actions were separately authorized.
- Do not repair unrelated failures or absorb adjacent work without approval.
- Do not mark a step complete from worker reports alone; verify integration evidence.

## Output

Report `Plan`, `Completed`, `Deviations`, `Validation`, `Unresolved`, `Stopped actions`, and `Next authorized step`.
