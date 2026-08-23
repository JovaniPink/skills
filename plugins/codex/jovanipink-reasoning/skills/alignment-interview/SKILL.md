---
name: alignment-interview
description: "Establish a shared, decision-ready understanding before implementation by inspecting available evidence and asking one material question at a time. Use when goals, constraints, terminology, or success criteria are unclear; do not use to delay an already approved and sufficiently specified change."
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.8.0"
  plugin: "jovanipink-reasoning"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Alignment Interview

Reach decision readiness before implementation starts.

## Workflow

1. Inspect the evidence already available in the request, repository, issue, plan, and named documents before asking the user to repeat facts.
2. State the current understanding as `Goal`, `Users`, `Constraints`, `Known evidence`, `Unknowns`, and `Success criteria`.
3. Rank unknowns by how much their answers could change scope, architecture, authority, safety, cost, or acceptance.
4. Ask one material question at a time. Explain why it matters and recommend a default when current evidence supports one.
5. Update the shared model after each answer and identify contradictions rather than smoothing them over.
6. Stop when the remaining unknowns do not prevent a responsible next decision. Summarize the agreed model, assumptions, rejected options, unresolved questions, and next authorized action.

## Boundaries

- Do not implement, edit files, publish, or create external records while interviewing unless separately authorized.
- Do not ask the user to repeat facts that can be discovered safely from the authorized workspace.
- Do not treat persistence or question count as quality. Stop when the decision is ready.
- Route broad product discovery to problem framing and concrete implementation design to implementation planning.

## Output

Return `Shared understanding`, `Evidence`, `Decisions`, `Assumptions`, `Open questions`, `Readiness`, and `Next authorized action`.
