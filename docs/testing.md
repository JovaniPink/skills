# Testing and Validation

Run from the repository root:

```sh
python3 scripts/build_distributions.py
python3 scripts/package_claude_ai.py
python3 scripts/check_workflows.py
python3 -m mypy --strict scripts tests
python3 -m ruff check scripts tests
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The Linux CI requirements file pins the workflow parser, its type information, and every type and lint dependency by version and wheel hash. It is not a portable local environment. Use PyYAML 6.0.3 with `scripts/check_workflows.py` on other platforms. `scripts/validate.py` reconciles the Linux lock with reviewed provenance and checks canonical metadata, Codex policy mapping, Claude explicit-invocation mapping, trigger coverage, primary-authority provenance, originality, repository independence, local references, public/private boundary patterns, marketplace structure, ZIP layout, and generated-tree drift.

## External validators

When installed, also run the current official tools:

```sh
skills-ref validate skills/<skill-name>
claude plugin validate plugins/claude/jovanipink-skills --strict
```

Run Codex's bundled skill validator for every canonical skill and the bundled plugin validator for the Codex plugin. Tool availability and observed output belong in `docs/validation-evidence.md`; never silently treat an unavailable validator as passing.

## Trigger evaluations

`evals/cases.json` is a deterministic coverage contract, not a claim that every client model behaves identically. Execute the cases on each supported surface and record observed activation or refusal separately in `docs/manual-smoke-tests.md`.

The current smoke-test introduction, version summary, validation candidate, and client evidence boundary must link to the versioned matrix for the catalog version. `scripts/validate.py` rejects missing links, references to historical matrices in those sections, and a missing or mismatched current matrix. Links inside HTML comments or fenced code examples do not satisfy this requirement. Earlier matrices remain valid historical evidence in their own sections.

## Release gate

A release requires green automated checks, clean generated trees, all required trigger cases, and completed manual evidence for every surface claimed as supported. A pending manual surface blocks parity claims and public-directory submission, not local authoring.
