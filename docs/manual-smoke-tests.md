# Manual Cross-Client Smoke Tests

## Local package follow-up, 2026-09-08

This was a setup check, not a behavioral study. Source: `61a269a`; public skill payloads match the 0.11.0 generated packages.

| Check | Observed result | Limit |
| --- | --- | --- |
| Codex CLI 0.153.2 | Two stale packs refreshed; all seven installed packs match generated files | Existing-task behavior not retested |
| Claude Code CLI 2.1.220 | Seven packs updated from 0.9.0 to 0.11.0; all 77 skills and package files match | One synthetic live check stopped on expired authentication; zero model cost reported |
| Claude desktop 1.46388.4 | Each of seven plugin pages shows 0.11.0, totaling 77 skills | Personal copies remain separate; task behavior and cloud sync not proved |
| Antigravity CLI 1.1.26 | One-skill preview installed; native validation and file hashes pass; namespaced skill appears in a fresh CLI menu | No model prompt submitted; full-catalog use and explicit-only controls unverified |
| Antigravity plugin lifecycle | Disable, enable, remove, and reinstall states verified | Removal checked by files and native import list, not a separate post-removal skill-menu session |
| Running Antigravity desktop | Previous skill list still shown after revisiting settings | Preview loading not established; no app restart performed |

A final check found that Antigravity CLI had changed to 1.1.27 without an update command in this task. Native package validation, the import list, and a fresh skill-menu check were repeated successfully on 1.1.27. The disable/enable and removal cycle above remains evidence for 1.1.26 only.

No personal preference was activated. Private paths, backups, account details, and detailed receipts remain outside this public record. Earlier observations below keep their original scope.

## Current client setup policy

Codex, Claude Code, and Antigravity setup checks can proceed independently. Use the [client support checklist](client-support.md) for each CLI and app. Historical observations below keep their original scope and dates; they do not prove that a current install works.

The authoritative row-level evidence is `client-observations.json`, validated by `client-observations-schema.json`. It records exact client versions/builds, tested source commit, artifact SHA-256, prompt, expected and observed activation, resource behavior, result, timestamp, operator, and sanitized evidence reference.

No surface is presumed equivalent to another. A successful CLI test is not Desktop evidence; manifest validation is not discovery evidence; archive acceptance is not invocation evidence.

## Current v0.9 summary

The v0.9 candidate source and representative archive are pinned in `client-observations-v0.9.json`. The matrix records only behavior observed on the exact named client version or service surface.

| Surface | Passed observations | Failed observations | Blocked observations | Surface status |
| --- | ---: | ---: | ---: | --- |
| Codex CLI | 3 | 0 | 0 | PASS |
| Codex Desktop | 0 | 0 | 1 | BLOCKED |
| ChatGPT Desktop | 0 | 0 | 1 | BLOCKED |
| ChatGPT Web | 0 | 1 | 0 | FAIL |
| Claude Code CLI | 2 | 0 | 1 | BLOCKED |
| Claude Code Desktop | 0 | 0 | 1 | BLOCKED |
| Claude.ai | 0 | 1 | 0 | FAIL |
| Gemini CLI 0.56.0 (historical) | 1 | 0 | 1 | BLOCKED |
| OpenAI Skills API | 0 | 0 | 1 | BLOCKED |
| Anthropic Skills API | 0 | 0 | 1 | BLOCKED |
| Anthropic Managed Agents | 0 | 0 | 1 | BLOCKED |

Totals: 6 `pass`, 2 `fail`, 8 `blocked`, 0 `not_supported`, and 0 `not_run`. The catalog remains blocked for v0.9 acceptance.

Codex CLI installed all seven plugins, resolved the named agent security skill, and loaded a fact available only in its focused reference. Claude Code CLI discovered all seven plugins and all 76 skills, but its model invocation stopped because authentication had expired. ChatGPT Web and Claude.ai did not contain the new v0.9 skill. Historical Gemini CLI 0.56.0 testing linked all 76 skills in a disposable workspace, but authenticated discovery was not performed; that result does not establish Antigravity or enterprise Gemini CLI compatibility. No API credential, new OAuth grant, deployment, release, or production access was created for these tests.

## Current v0.8 summary

The v0.8 source and representative archive are pinned in `client-observations-v0.8.json`. Each surface has separate installation, discovery, implicit-activation, focused-reference, refusal, update, and removal rows. No receiving-client operation was authorized, so every observation is terminal `blocked` rather than `not_run`.

| Surface | Version/build | Passed observations | Blocked observations | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | not observed | 0 | 7 | BLOCKED |
| ChatGPT Desktop | not observed | 0 | 7 | BLOCKED |
| ChatGPT Web | not observed | 0 | 7 | BLOCKED |
| Claude Code CLI | not observed | 0 | 7 | BLOCKED |
| Claude Code Desktop | not observed | 0 | 7 | BLOCKED |
| Claude.ai | not observed | 0 | 7 | BLOCKED |

Totals: 0 `pass`, 0 `fail`, 42 `blocked`, 0 `not_supported`, and 0 `not_run`. Strict generated-plugin and archive validation does not establish receiving-client behavior.

## Current v0.6 summary

The engineering-depth and continuity source commit is pinned in `client-observations-v0.6.json`. Fresh command-line observations were recorded on 2026-08-21 without inferring behavior on another surface.

| Surface | Version/build | Passed observations | Blocked observations | Surface status |
| --- | --- | ---: | ---: | --- |
| Codex CLI | 0.145.0 | 7 | 1 | BLOCKED |
| Codex Desktop | fresh task not created | 0 | 1 | BLOCKED |
| ChatGPT Web | not freshly observed for v0.6 | 0 | 1 | BLOCKED |
| Claude Code CLI | 2.1.220 | 3 | 2 | BLOCKED |
| Claude Code Desktop | not freshly observed for v0.6 | 0 | 1 | BLOCKED |
| Claude.ai | not freshly observed for v0.6 | 0 | 1 | BLOCKED |

Totals: 10 `pass`, 0 `fail`, 7 `blocked`, 0 `not_supported`, and 0 `not_run`. The v0.6 acceptance status remains `blocked`.

Passed v0.6 evidence:

- Codex CLI updated or installed all five plugins, discovered their installed state, implicitly activated `code-change-review`, kept `prototype-spike` inactive without a name, activated it when named, loaded the installed focused decision-map reference, and passed remove, absence, reinstall, and restored-state checks.
- Claude Code CLI updated or installed all five plugins, reported the reasoning plugin's 11 skills with no agents, hooks, MCP servers, or language servers, and passed remove, absence, reinstall, and restored-state checks.

Blocked v0.6 evidence:

- Downgrade testing is blocked on both command-line clients because the local directory marketplace exposes the current checkout rather than immutable accepted versions, and no release tag was authorized.
- Claude Code activation and focused-reference loading are blocked because its OAuth session expired and could not be refreshed. Package installation and component discovery are not treated as invocation evidence.
- Codex Desktop requires a fresh task created after v0.6 installation. This task predates that installation.
- ChatGPT Web does not receive local Codex marketplace installations. Claude Code Desktop and Claude.ai still require fresh authenticated observations.

Codex CLI warned that enabled skill descriptions exceeded its discovery-context budget after all five JovaniPink plugins and unrelated plugins were enabled. This is an observed reason to enable only the plugins needed for a task; it is not evidence that a particular skill failed. Other client warnings were not attributed to this catalog without causal evidence.

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
