---
name: test-driven-change
description: Guide feature and defect work through red, green, and refactor evidence while preserving a clear exception path when test-first work is unsuitable. Use for behavior changes where an executable test can prove the defect or desired outcome before implementation.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.3.0"
  plugin: "jovanipink-engineering"
  invocation: "implicit"
  provenance: "original"
  risk_class: "bounded-execution"
---

# Test Driven Change

Use executable evidence to prove that a change addresses the intended behavior.

## Workflow

1. State the behavior, observable boundary, and smallest failing example.
2. Confirm that the failure is meaningful and caused by the target gap rather than a broken fixture or environment.
3. Add or identify a test that fails for the expected reason. Record the red evidence.
4. Implement the smallest change that makes the targeted test pass.
5. Run the focused test and relevant regression gates. Record the green evidence.
6. Refactor only while the tests remain green, then rerun the appropriate gate set.
7. Report any behavior not covered by executable tests and the required manual or platform observation.

## Exception path

If test-first is unsuitable, state why before changing code. Valid reasons can include inaccessible hardware, nondeterministic external systems, a missing safe harness, or a purely investigative spike. Define the replacement evidence and a follow-up test obligation where practical.

## Boundaries

- A test that never failed does not prove it detects the target defect.
- Do not weaken assertions, delete coverage, regenerate broad snapshots, or alter production data merely to obtain green output.
- Passing focused tests do not prove deployment or live behavior.

## Output

Report `Behavior`, `Red evidence`, `Implementation`, `Green evidence`, `Refactor`, `Regression coverage`, and `Unverified behavior`.
