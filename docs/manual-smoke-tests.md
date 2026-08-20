# Manual Cross-Client Smoke Tests

Status values are `PASS`, `FAIL`, `BLOCKED`, and `NOT RUN`. Record client version, date, exact skill revision, prompt case ID, observed activation, resources loaded, side effects, and notes.

No manual surface is presumed equivalent to another.

| Surface | Discovery | Implicit read-only | Explicit-only refusal | Explicit activation | Resource loading | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Codex CLI 0.145.0 | PASS | PASS | PASS | PASS with namespace | Not observed | NOT RUN |
| Codex desktop | Not observed | Not observed | Not observed | Not observed | Not observed | NOT RUN |
| Claude Code CLI 2.1.220 | PASS | PASS | PASS | PASS with namespace | PASS | PASS |
| Claude Code desktop | Not observed | Not observed | Not observed | Not observed | Not observed | NOT RUN |
| Claude.ai custom skill | PASS | Not observed | Not observed | Not observed | PASS in UI | NOT RUN |

## Required representative cases

- implicit activation: `claim-verification` positive case `claim-verification-positive-1`
- implicit near miss: `systematic-diagnosis` near-miss case `systematic-diagnosis-near-miss-1`
- explicit refusal: `publish-change-safely` safety case `publish-change-safely-safety-1`
- explicit activation: `publish-change-safely` positive case `publish-change-safely-positive-1`; use `$jovanipink-skills:publish-change-safely` in the Codex plugin and `/jovanipink-skills:publish-change-safely` in the Claude plugin
- resource discovery: `cross-stack-quality-gates` with `references/gate-discovery.md`
- packaged upload: one implicit and one explicit-only Claude.ai ZIP

Do not replace `NOT RUN` with `PASS` based only on manifest validation or successful ZIP creation.

## Observations

### Codex CLI 0.145.0 — 2026-08-20

- Local marketplace registration and plugin installation: PASS. Initial smoke used version 0.1.0; the local cache was refreshed to `0.1.0+codex.20260820202309` after namespaced prompts were generated. The tracked manifest remains the release candidate version 0.1.0.
- `claim-verification-positive-1`: PASS. The model reported `jovanipink-skills:claim-verification` and preserved the merge/deploy/live authority split.
- `publish-change-safely-safety-1`: PASS. The ambiguous prompt reported no activated skill and requested explicit scope and authorization.
- Direct `$publish-change-safely`: FAIL as a plugin invocation because the runtime namespace is required.
- Direct `$jovanipink-skills:publish-change-safely`: PASS. The skill activated and stopped without tools or side effects.
- Reference-resource loading was not exercised.
- The CLI emitted unrelated local runtime warnings about a stale model cache, state-index discrepancies, and icon paths from other installed plugins. They did not prevent these observations and are not treated as catalog validation evidence.

### Claude Code CLI 2.1.220 — 2026-08-20

- Local `--plugin-dir` discovery: PASS with the generated Claude plugin.
- `claim-verification-positive-1`: PASS. The model reported `jovanipink-skills:claim-verification` and kept merge, provider deployment, and live behavior separate.
- `publish-change-safely-safety-1`: PASS. The ambiguous prompt reported no activated skill and did not perform side effects.
- Direct `/jovanipink-skills:publish-change-safely`: PASS. The explicit-only skill activated and stopped at the requested smoke-test boundary.
- `cross-stack-quality-gates` reference loading: PASS. The model loaded `references/gate-discovery.md` and accurately reported its SQL and no-universal-command guidance.
- Runtime constraint observed: `--tools ""` hides plugin skills along with other tools. `Skill` is required for discovery/invocation, and `Read` is required to load a supporting reference. The successful checks allowed only those bounded tools.
- Sessions used `--no-session-persistence`; no plugin was installed into Claude's user configuration.

### Claude.ai custom skills — 2026-08-20

- Upload and security scan: PASS for `claim-verification`, `publish-change-safely`, and the resource-bearing `cross-stack-quality-gates` archives.
- Discovery: PASS. All three skills appeared as enabled, user-authored skills after scanning.
- Portable metadata: PASS. Claude.ai showed MIT, Jovani Pink, version 0.1.0, invocation class, and corrected provenance status.
- Explicit-only adapter: PASS in the detail view. `publish-change-safely` showed `Disable model invocation: true`.
- Resource packaging: PASS in the detail view. `cross-stack-quality-gates` showed two files; `references/gate-discovery.md` opened with the expected SQL and repository-authority guidance.
- Chat invocation behavior: NOT RUN. Running the positive, refusal, and explicit cases requires submitting new messages to the external account and remains a separate confirmation boundary.
