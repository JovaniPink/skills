# Validation Evidence

This file records observed outcomes for catalog release candidates. Validators do not rewrite it automatically.

## v0.6 tested source

- Source commit: `759b3bf9bfca9967144b02d18f0678e3b509e2b3`
- Catalog/plugin version: `0.6.0`
- Date: 2026-08-21
- Canonical skills: 61 across five optional plugins
- Manual matrix: 6 terminal suite rows; 0 pass, 6 blocked, 0 fail, 0 not supported, 0 not run
- Acceptance: BLOCKED until fresh client installation and invocation observations are recorded

## v0.6 automated repository checks

- `python3 scripts/validate.py`: PASS - schemas, links, boundary scan, originality scan, package checksums, trigger coverage, generated drift, fixtures, and catalog records
- `python3 -m unittest discover -s tests -v`: PASS - 24 regression tests
- non-mutating `python3 scripts/build_distributions.py --check`: PASS - all five Codex and Claude plugin trees and both marketplace records match canonical sources
- Codex bundled skill validator: PASS - all 61 canonical skills
- Codex bundled plugin validator: PASS - all five Codex plugins
- `claude plugin validate --strict`: PASS - all five generated Claude plugins
- Claude.ai packages: PASS - 61 deterministic, individually nested ZIPs with SHA-256 checksums
- online primary-authority freshness: PASS - changed official sources were re-reviewed and refreshed pins matched current primary-authority content
- `skills-ref`: UNAVAILABLE - the command was not installed in the validation environment, so no passing claim is made

## v0.6 client evidence boundary

See `client-observations-v0.6.json`. Every supported surface has a terminal `blocked` suite record tied to the exact tested source commit and representative ZIP checksum. Package and validator results are not treated as installation, discovery, activation, reference loading, upload acceptance, or client parity.

## v0.5 tested source

- Source commit: `0c53d68a552aa475746a85c228c1e063233f8ed4`
- Catalog/plugin version: `0.5.0`
- Date: 2026-08-21
- Canonical skills: 54 across five optional plugins
- Manual matrix: 6 terminal suite rows; 0 pass, 6 blocked, 0 fail, 0 not supported, 0 not run
- Acceptance: BLOCKED until fresh client installation and invocation observations are recorded

## v0.5 automated repository checks

- `python3 scripts/validate.py`: PASS - schemas, links, boundary scan, originality scan, package checksums, trigger coverage, generated drift, fixtures, and catalog records
- `python3 -m unittest discover -s tests -v`: PASS - 22 regression tests
- non-mutating `python3 scripts/build_distributions.py --check`: PASS - all five Codex and Claude plugin trees and both marketplace records match canonical sources
- Codex bundled skill validator: PASS - all 54 canonical skills
- Codex bundled plugin validator: PASS - all five Codex plugins
- `claude plugin validate --strict`: PASS - all five generated Claude plugins
- Claude.ai packages: PASS - 54 deterministic, individually nested ZIPs with SHA-256 checksums
- `skills-ref`: UNAVAILABLE - the command was not installed in the validation environment, so no passing claim is made

## v0.5 client evidence boundary

See `client-observations-v0.5.json`. Every supported surface has a terminal `blocked` suite record tied to the exact tested source commit and representative ZIP checksum. Package validation is not treated as installation, discovery, activation, reference loading, upload acceptance, or client parity.

## Tested source

- Source commit: `e2426dcb1f6d4a170c91c68a1eace4869de4fce0`
- Catalog/plugin version: `0.1.0`
- Date: 2026-08-20
- Manual matrix: 31 terminal rows; 17 pass, 14 blocked, 0 fail, 0 not supported, 0 not run
- Acceptance: BLOCKED until the row-level client blockers are cleared

## Automated repository checks

- `python3 scripts/validate.py`: PASS - catalog, adapters, trigger coverage, strict schemas, links, public boundary, packages, checksums, fixtures, and generated drift
- `python3 -m unittest discover -s tests -v`: PASS - 13 regression tests
- non-mutating `python3 scripts/build_distributions.py --check`: PASS - generated plugin trees and both marketplace records match canonical sources
- public-boundary scan: PASS - tracked/non-ignored publishable files plus generated ZIP contents; local sensitive terms come only from the gitignored denylist
- cross-stack fixture evaluation: PASS - six discovery contracts, including evidence-insufficient SQL and forbidden mutating commands
- Codex bundled skill validator: PASS - all 10 canonical skills
- Codex bundled plugin validator: PASS - generated Codex plugin
- `skills-ref`: PASS - all 10 canonical skills using official reference revision `69ef37e9424c0a7ea9dd2293b559e43ec8176379`
- `claude plugin validate . --strict`: PASS - marketplace and referenced plugin, Claude Code 2.1.220
- `claude plugin validate plugins/claude/jovanipink-skills --strict`: PASS - generated Claude plugin, Claude Code 2.1.220
- Claude.ai packages: PASS - 10 deterministic, individually nested ZIPs with SHA-256 checksums

## Client evidence boundary

See `manual-smoke-tests.md` and `client-observations.json`. Codex CLI and the required manual Claude Code CLI behaviors passed. Codex Desktop, Claude Code Desktop, and Claude.ai invocation remain blocked, and Claude Code's built-in plugin-eval ablation remains blocked by client availability. No validation, CLI result, or package inspection is substituted for those observations.
