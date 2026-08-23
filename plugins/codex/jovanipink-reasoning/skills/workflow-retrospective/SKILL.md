---
name: workflow-retrospective
description: "Review a completed or paused workflow using supplied artifacts and current task evidence to identify what helped, what failed, why, and which bounded improvement to test next. Invoke explicitly after meaningful work; do not mine private histories or automatically rewrite policy or skills."
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.7.0"
  plugin: "jovanipink-reasoning"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Workflow Retrospective

Turn observed execution evidence into a small, testable workflow improvement.

## Workflow

1. Define the reviewed interval, objective, expected workflow, supplied artifacts, and evidence boundary.
2. Reconstruct observable events, decisions, delays, rework, failures, recoveries, and outcomes without inferring private motives.
3. Identify contributing conditions across problem framing, information, tools, ownership, sequencing, validation, and authority.
4. Separate causal evidence from correlation, hindsight, preference, and unsupported explanation.
5. Preserve useful behavior and name the smallest material friction or risk worth changing.
6. Propose one bounded experiment with an owner, success signal, guardrail, review date, and rollback or rejection condition.
7. Record what remains unknown and what evidence would change the conclusion.

## Boundaries

- Use the current task and explicitly supplied artifacts. Do not search raw chats, private histories, unrelated repositories, or broad connector data by default.
- Do not expose chain-of-thought or treat a transcript as an objective record of causality.
- Do not automatically edit skills, repository policy, automation, or configuration.
- Do not turn one event into a universal rule without repeated evidence.

## Output

Return `Scope`, `Observed timeline`, `What helped`, `What hindered`, `Contributing conditions`, `Evidence limits`, `Improvement experiment`, `Owner and review date`, and `Rejected generalizations`.
