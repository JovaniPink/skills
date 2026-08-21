---
name: cross-stack-quality-gates
description: Discover and run the repository's real validation gates across Go, Python, Swift, TypeScript or JavaScript, SQL, and Terraform without assuming a universal command. Use after changes, before review, or when asked whether a codebase passes its checks.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.2.0"
  plugin: "jovanipink-skills"
  invocation: "implicit"
  provenance: "adapted"
  risk_class: "bounded-execution"
---

# Cross Stack Quality Gates

Discover the project's contract before running validation. Read [gate discovery](references/gate-discovery.md) only for the stacks present in the target scope.

## Workflow

1. Inspect repository instructions, manifests, CI configuration, and documented scripts.
2. Determine which components changed and which gate owns each relevant invariant.
3. Choose the narrowest useful sequence, normally fast static checks before slower tests and builds.
4. Run commands exactly as the repository defines them. Do not silently substitute package managers, add flags, rewrite snapshots, format files, apply Terraform, or update dependencies.
5. Record command, working directory, exit status, duration when material, and the first actionable failure.
6. Distinguish a missing gate from a passing gate. Do not skip an unavailable command and report the suite green.
7. Report environment restrictions separately from product failures.

## Scope rules

- A monorepo may require multiple component-specific gates; do not run every workspace blindly.
- Builds may create ignored artifacts or caches but must not rewrite tracked source.
- SQL validation must state whether it was syntax/static only or executed against a real engine.
- Terraform validation is not an apply. Plans are proposals and must not be reported as deployed state.
- Simulator or preview checks do not prove device, production, or provider behavior.

## Output

Return a gate table with `Component`, `Command`, `Result`, and `Evidence`, followed by coverage gaps and the overall verdict: `PASS`, `FAIL`, or `INCOMPLETE`.
