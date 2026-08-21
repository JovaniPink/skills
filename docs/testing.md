# Testing and Validation

Run from the repository root:

```sh
python3 scripts/build_distributions.py
python3 scripts/package_claude_ai.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

`scripts/validate.py` checks canonical metadata, Codex policy mapping, Claude explicit-invocation mapping, trigger coverage, provenance coverage, the public-source audit, clean-room originality, local references, public/private boundary patterns, marketplace structure, ZIP layout, and generated-tree drift.

## External validators

When installed, also run the current official tools:

```sh
skills-ref validate skills/<skill-name>
claude plugin validate plugins/claude/jovanipink-skills --strict
```

Run Codex's bundled skill validator for every canonical skill and the bundled plugin validator for the Codex plugin. Tool availability and observed output belong in `docs/validation-evidence.md`; never silently treat an unavailable validator as passing.

## Trigger evaluations

`evals/cases.json` is a deterministic coverage contract, not a claim that every client model behaves identically. Execute the cases on each supported surface and record observed activation or refusal separately in `docs/manual-smoke-tests.md`.

## Release gate

A release requires green automated checks, clean generated trees, all required trigger cases, and completed manual evidence for every surface claimed as supported. A pending manual surface blocks parity claims and public-directory submission, not local authoring.
