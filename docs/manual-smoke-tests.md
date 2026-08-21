# Manual Cross-Client Smoke Tests

The authoritative row-level evidence is `client-observations.json`, validated by `client-observations-schema.json`. It records exact client versions/builds, tested source commit, artifact SHA-256, prompt, expected and observed activation, resource behavior, result, timestamp, operator, and sanitized evidence reference.

No surface is presumed equivalent to another. A successful CLI test is not Desktop evidence; manifest validation is not discovery evidence; archive acceptance is not invocation evidence.

## Current v0.5 summary

The reasoning-foundation source commit is pinned in `client-observations-v0.5.json`. All six surface suites have the terminal result `blocked` because the exact v0.5 plugin has not yet been installed and exercised in fresh client sessions.

| Surface | Version/build | Passed suites | Blocked suites | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| Codex Desktop | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| ChatGPT Web | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| Claude Code CLI | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| Claude Code Desktop | not freshly observed for v0.5 | 0 | 1 | BLOCKED |
| Claude.ai | not freshly observed for v0.5 | 0 | 1 | BLOCKED |

The focused-reference prompt asks for the native location of `disable-model-invocation` and requires a boundary documented only in the `portable-skill-authoring` client adapter reference. A valid package and generated reference file do not prove that a client loaded it.

## Current v0.4 summary

The operations and catalog-lifecycle source commit is pinned in `client-observations-v0.4.json`. Fresh local observations were recorded on 2026-08-21 without inferring parity between clients.

| Surface | Version/build | Passed observations | Blocked observations | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | 0.145.0 | 7 | 0 | PASS |
| Codex Desktop | 26.818.22352 / 6872 | 0 | 5 | BLOCKED |
| ChatGPT Web | Safari 26.6 / 21624.4.5.11.5 | 0 | 6 | BLOCKED |
| Claude Code CLI | 2.1.220 | 3 | 4 | BLOCKED |
| Claude Code Desktop | 1.34493.1 | 0 | 5 | BLOCKED |
| Claude.ai | not freshly tested for v0.4 | 0 | 5 | BLOCKED |

Totals: 10 `pass`, 0 `fail`, 25 `blocked`, 0 `not_supported`, and 0 `not_run`. The v0.4 acceptance status remains `blocked`.

Passed v0.4 evidence:

- Codex CLI installed all four plugins, discovered all 11 operations skills, produced the expected implicit requirements and decision-status behavior, refused unnamed explicit-only activation, activated namespaced `plan-execution`, and passed remove, absence, reinstall, and restored-state verification.
- Claude Code CLI installed all four plugins, exposed all 46 namespaced skills during initialization, and passed remove, absence, reinstall, and restored-state verification for the operations plugin.

Blocked v0.4 evidence:

- Claude Code CLI model-dependent tests are blocked because the OAuth session expired and could not be refreshed. Plugin initialization is not treated as activation evidence.
- Codex Desktop requires a fresh task after plugin installation. Automated control of the ChatGPT app was unavailable, so no Desktop result was inferred from CLI behavior.
- Claude Code Desktop had an enabled user-scope installation, but no fresh message was submitted and observed.
- ChatGPT Web in Safari reported that the account had no skills. A local Codex marketplace install did not synchronize to the web account, and no workspace or directory publication was authorized.
- Claude.ai v0.4 upload and invocation were not performed. Earlier v0.1 ZIP observations are not reused as v0.4 evidence.

Codex CLI also emitted a skill-description budget warning when all four catalog plugins and other plugins were enabled. Focused installation or disabling unused plugins is recommended. Other client warnings were recorded but were not attributed to this catalog without causal evidence.

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
