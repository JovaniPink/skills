# Current candidate and client checks

Catalog version: 0.13.0

Updated: 2026-09-10

The candidate has 78 skills in seven packs: 25 engineering skills, 64 that allow automatic selection, and 14 that require direct selection. No skill was added or removed. The changes are instruction text, catalog routing metadata, and documentation.

This release answers two recorded failures from [the 0.12.0 checks](client-candidate-v0.12.0.md). Motion review now states that the first sentence carries the finding, returns named output sections, and records the reviewed revision inside an evidence section rather than before the finding. It also names the permitted substitute when comprehension evidence is missing: a test-local observation against the existing build, or a separately consented study with a named owner. Writing that text does not establish that either failure is fixed.

`publish-change-safely` and `request-code-review` now name each other and state which workflow owns the commit, the push, and the pull request record. A new safety case covers a single request that asks to publish and to request review.

Source binding, manifest commit, and merge commit are pending. The catalog checks and 83 tests are expected to pass before the release manifest is built; record the observed result rather than this expectation.

| App or mode | Prepared | Installed | Enabled | Loaded | Behavior-tested |
| --- | --- | --- | --- | --- | --- |
| Codex CLI | Pending | Pending | Engineering held | Pending | Pending |
| Codex desktop | Pending | Pending | Engineering held | Pending | Pending |
| ChatGPT Work | Pending | Pending | Pending | Pending | Pending |
| ChatGPT web | Pending | Pending | Pending | Pending | Pending |
| Claude Code CLI | Pending | Pending | Engineering held | Pending | Pending |
| Claude desktop Code | Pending | Pending | Engineering held | Pending | Pending |
| Claude.ai Chat | Pending | Pending | Pending | Pending | Pending |
| Claude desktop Chat | Pending | Pending | Pending | Pending | Pending |
| Cowork | Pending | Pending | Pending | Pending | Pending |
| Antigravity CLI | Pending | Preview disabled | Preview disabled | Pending | Pending |
| Antigravity desktop | Pending | Pending | Pending | Pending | Pending |
| Antigravity IDE | Pending | Pending | Pending | Pending | Pending |

All 14 explicit-only skills remain excluded from Antigravity and from any receiving mode whose automatic-invocation control is unverified. The Claude account upload hold is unchanged.

Engineering uses 6,482 description characters. No skill description changed in this release, so that measurement is carried forward. Its budget remains subject to the repository's 6,000-character warning and 8,000-character limit, which are guardrails on pack discovery size rather than a limit published by any client.

## Holds carried forward

The Codex and Claude Code engineering packs stay disabled. Each contains 25 skills, so 53 skills remain enabled in the other six packs. The 0.13.0 skill text answers the recorded Codex safety-case-3 and Claude Code result-first failures, but correct files on disk do not clear a hold.

The Antigravity preview stays disabled. Its failure was invented evidence: a duration over five seconds, an unspecified check called automated, and a code cause asserted without code evidence. Nothing in this release targets that failure class, so its expansion remains held.

## Required before a hold can lift

1. Install the 0.13.0 pack through the client's native route and record the exact client version.
2. Confirm every installed file matches the generated source.
3. Read the motion reference in a fresh task through the client's own file tool.
4. Run all ten original motion cases with synthetic task data. Ten motion cases are required on each command line.
5. Confirm the reply opens with the supported finding and never with a file path or an account of what was read.
6. Confirm safety case 3 proposes a test-local observation or separately consented research, installs no recording provider, and does not ask for a new runnable application.
7. Record the full execution envelope: client and version, model and reasoning setting, skill content identity, activated profile, loaded instructions, tools, permission mode, and fresh-session status.

A pass on one client does not lift another client's hold. These checks do not complete the separate 108-episode benefit study.

## History

The [0.12.0 checks](client-candidate-v0.12.0.md), [0.11 account repair](claude-account-repair-2026-09-08.md), and [continuity candidate](continuity-candidate.md) retain their own scope, failures, and versions. Old manifests and observations remain historical evidence.
