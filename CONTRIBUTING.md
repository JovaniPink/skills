# Contributing

Canonical changes begin in `skills/`. Generated plugin trees must not be edited by hand.

1. Read `docs/authoring.md`, `docs/security-model.md`, and `docs/provenance.md`.
2. Add or update a single focused skill.
3. Record provenance in `provenance/catalog.json`.
4. Add at least three positive triggers, three near misses, and one safety/conflict case to `evals/cases.json`.
5. Regenerate distributions and packages.
6. Run the complete local validation commands documented in `docs/testing.md`.
7. Keep observed results separate from assumptions in `docs/manual-smoke-tests.md`.

Contributions must not include secrets, private system identifiers, proprietary language, absolute workstation paths, unsupported outcome claims, hooks, MCP servers, broad tool grants, or skill-level executables.
