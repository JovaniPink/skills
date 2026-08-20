# Validation Evidence

This file records observed validation outcomes for the current working revision. It is updated by maintainers after running the commands; validators do not rewrite it automatically.

## Automated repository checks

- Revision: uncommitted v0.1 foundation
- Date: 2026-08-20
- `scripts/validate.py`: PASS — canonical catalog, adapters, trigger coverage, provenance, links, public boundary, packages, checksums, and generated drift
- unit tests: PASS — 6 tests
- cross-stack fixture evaluation: PASS — six stack-specific discovery contracts, including an evidence-insufficient SQL outcome and forbidden mutating commands
- Codex bundled skill validator: PASS — all 10 canonical skills
- Codex bundled plugin validator: PASS — generated Codex plugin
- `skills-ref`: PASS — all 10 canonical skills using official reference revision `69ef37e9424c0a7ea9dd2293b559e43ec8176379`
- `claude plugin validate . --strict`: PASS — marketplace and its referenced plugin, Claude Code 2.1.220
- `claude plugin validate plugins/claude/jovanipink-skills --strict`: PASS — generated Claude plugin, Claude Code 2.1.220
- Claude Code CLI plugin smoke: PASS — implicit activation, explicit-only non-activation, namespaced explicit activation, and bundled reference loading
- Codex CLI version observed: 0.145.0
- Codex CLI installed-plugin smoke: PASS for implicit activation, explicit-only non-activation from an ambiguous prompt, and namespaced explicit activation; resource loading remains untested
- Claude.ai archives: PASS — 10 reproducible, individually nested ZIPs with SHA-256 checksums
- Claude.ai upload evidence: PASS — three representative archives accepted after security scan; discovery, metadata, explicit-only control, and bundled resource preview observed

## Manual client checks

See `manual-smoke-tests.md`. Claude Code CLI is complete; Codex CLI still lacks resource-loading evidence; Codex desktop, Claude Code desktop, and Claude.ai chat invocation remain incomplete. Manifest validation and package creation are not substituted for client behavior.
