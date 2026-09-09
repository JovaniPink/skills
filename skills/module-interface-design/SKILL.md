---
name: module-interface-design
description: "Design or review a module boundary, vocabulary, interface, and hidden implementation so callers face a smaller and more stable contract. Use when code is coupled, concepts leak across layers, responsibilities are unclear, or a redesign needs concrete options before implementation."
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.11.0"
  plugin: "jovanipink-engineering"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Module Interface Design

Propose a coherent boundary that reduces caller knowledge without hiding important authority or failure behavior.

## Workflow

1. Establish the user outcome, current modules, callers, dependencies, vocabulary, invariants, and change pressure.
2. Identify knowledge duplicated across callers, unstable details that leak through interfaces, and state or authority that lacks a clear owner.
3. Define the smallest useful contract: inputs, outputs, errors, state transitions, compatibility promises, and operational signals.
4. Compare at least two viable boundaries when the tradeoff is material. Include the cost of keeping the current design.
5. Test each option against common use, difficult use, invalid use, migration, partial rollout, and future change.
6. Recommend a boundary with explicit reasons, rejected alternatives, and unresolved decisions.
7. Describe a staged migration and verification approach without performing the redesign.

## Boundaries

- Prefer evidence from actual callers over abstract purity.
- A deeper module is not permission to conceal data authority, security decisions, or failure modes.
- Do not force one architecture pattern across unrelated stacks.
- Treat redesign, deletion, migration, and compatibility breaks as proposals until separately approved.

## Output

Return `Current pressure`, `Vocabulary`, `Invariants`, `Candidate boundaries`, `Recommended interface`, `Hidden implementation`, `Compatibility`, `Migration`, `Tradeoffs`, and `Open decisions`.
