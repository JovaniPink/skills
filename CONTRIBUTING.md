# Contributing

Write skills in `skills/`. The `plugins/` folders are generated, so do not edit them by hand.

Before you start, read [the authoring guide](docs/authoring.md), [the security model](docs/security-model.md), and [the provenance policy](docs/provenance.md).

Then, for one skill at a time:

1. Add or update a single focused skill.
2. Record where its content came from in `provenance/catalog.json`.
3. Add test cases to `evals/cases.json`: three that should start the skill, three near misses that should not, and one safety case.
4. Regenerate the client packages.
5. Run the checks listed in [the testing guide](docs/testing.md).
6. Keep observed results separate from assumptions in `docs/manual-smoke-tests.md`.

## What a contribution must not contain

- secrets or credentials
- private system names or identifiers
- proprietary text
- absolute paths from your own machine
- claims about results we have not measured
- hooks, MCP servers, broad tool grants, or skill-level programs

The [glossary](docs/glossary.md) defines the terms used here. The [editorial style guide](docs/editorial-style.md) covers the writing rules.
