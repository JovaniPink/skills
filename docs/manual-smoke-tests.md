# Manual Cross-Client Smoke Tests

The authoritative row-level evidence is `client-observations.json`, validated by `client-observations-schema.json`. It records exact client versions/builds, tested source commit, artifact SHA-256, prompt, expected and observed activation, resource behavior, result, timestamp, operator, and sanitized evidence reference.

No surface is presumed equivalent to another. A successful CLI test is not Desktop evidence; manifest validation is not discovery evidence; archive acceptance is not invocation evidence.

## Current v0.4 summary

The operations and catalog-lifecycle source commit is pinned in client-observations-v0.4.json. All 29 required rows have the terminal result blocked because no fresh client session was authorized or available during the release run. No v0.4 installation, activation, uninstallation, or parity claim is made.

## Current v0.3 summary

The engineering-quality and stack-profile source commit is pinned in client-observations-v0.3.json. All 34 required rows have the terminal result blocked because no fresh client session was authorized or available during the release run. No v0.3 installation, activation, reference-loading, uninstallation, or parity claim is made.

## Current v0.2 summary

The engineering lifecycle source commit is pinned in `client-observations-v0.2.json`. All 29 required rows have the terminal result `blocked` because no fresh client session was authorized or available during the release run. No v0.2 client activation, resource-loading, installation, uninstallation, or parity claim is made.

## Current v0.1 summary

| Surface | Version/build | Passed observations | Blocked observations | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | 0.145.0 | 7 | 0 | PASS |
| Codex Desktop | 26.818.22352 / 6872 | 0 | 5 | BLOCKED |
| Claude Code CLI | 2.1.220 | 7 | 1 | BLOCKED |
| Claude Code Desktop | 1.32885.1 | 0 | 5 | BLOCKED |
| Claude.ai | web application observed 2026-08-20 | 3 | 3 | BLOCKED |

Totals: 17 `pass`, 0 `fail`, 14 `blocked`, 0 `not_supported`, and 0 `not_run`. The v0.1 acceptance status remains `blocked`; this is intentionally narrower than claiming cross-client parity.

## Passed evidence

- Codex CLI: install, discovery, implicit `claim-verification`, explicit-only non-activation, namespaced explicit activation, true installed bundled-reference loading, and uninstall.
- Claude Code CLI: install, discovery, implicit activation, explicit-only non-activation, namespaced explicit activation, installed bundled-reference loading, and uninstall.
- Claude.ai: representative ZIP upload/security acceptance, enabled-skill discovery and metadata, and focused resource preview.
- Automated: strict open-spec, Codex, Claude, schema, link, boundary, package, checksum, trigger, and generated-drift validation.

The Codex reference test prevented web, network, GitHub, and project-checkout access and allowed one read-only local command. It returned facts found only in the installed `gate-discovery.md` reference, proving bundled-resource loading rather than skill-name discovery.

## Blocked evidence

- Codex Desktop requires a fresh task created after plugin installation. The current task predates the refresh, so no Desktop activation or resource result was inferred.
- Claude Code CLI's built-in `plugin eval` command reported early access and exited before activation/output ablation initialization. Manual CLI cases remain passed observations, not a substitute for the blocked built-in eval.
- Claude Code Desktop had an enabled user-scope installation, but no test message was submitted at the external-message confirmation boundary.
- Claude.ai had a signed-in new-chat surface and advertised slash skills, but natural, refusal, and explicit messages were not submitted at the external-message confirmation boundary.

These rows are terminal `blocked` observations, not silent omissions. Clearing them requires new observed evidence on the named surface and an update to the matrix; it does not permit copying a result from another client.
