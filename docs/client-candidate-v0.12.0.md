# Current candidate and client checks

Catalog version: 0.12.0

Updated: 2026-09-09

The candidate has 78 skills in seven packs: 25 engineering skills, 64 that allow automatic selection, and 14 that require direct selection. The motion skill is carried forward from PR #21, whose original head is `945223a7402d52b4a59f3f205536951f3bd350bc`. Its ten original cases remain intact. Three cases add reference access, result-first reporting, and WCAG level checks.

The candidate and [source review](audits/source-review-2026-09-09.md) are merged in PR #29. Source-review acceptance passed, and issues #21 and #25 are closed. Motion adoption is held after live CLI failures. Review and preparation do not establish useful behavior.

Source files are bound to commit `61d9f2c7ca0ccca0dbfbca123893ca6bddd71dd0`. Manifest commit `06f741813815d5b22b618eb2d8e330419f381700` directly follows it. Merge commit `dfe354134d6445b4134f3080e6383fce29cd2cde` preserves that history. The catalog checks and 83 tests passed locally and in CI. Packaging twice produced the same hashes.

| App or mode | Prepared | Installed | Enabled | Loaded | Behavior-tested |
| --- | --- | --- | --- | --- | --- |
| Codex CLI | Passed | Seven packs, 78 skills; all files match | Six packs; engineering held | Motion skill and reference read | Ten original cases run; safety case 3 failed |
| Codex desktop | Passed | Local cache checked; app check pending | Engineering held in local settings | Fresh task pending | Pending |
| ChatGPT Work | Pending library check | Pending | Pending | Pending | Pending |
| ChatGPT web | Pending library check | Pending | Pending | Pending | Pending |
| Claude Code CLI | Passed | Seven packs, 78 skills; all files match | Six packs; engineering held | Motion reference read | Shared probe failed result-first check; original cases not run |
| Claude desktop Code | Passed | Local cache checked; task source pending | Local engineering pack held | Fresh task pending | Pending |
| Claude.ai Chat | Passed | 63 replacements match downloaded files; motion upload awaiting readback | 63 current confirmed; motion state pending | Fresh task pending | Pending |
| Claude desktop Chat | Passed | Account updated; app refresh pending | App check pending | Fresh task pending | Pending |
| Cowork | Pending library check | Pending | Pending | Pending | Pending |
| Antigravity CLI | Two-skill package passed | Native two-skill preview installed | Preview disabled after failure | Motion reference and fixture read | Shared probe invented evidence; expansion held |
| Antigravity desktop | Two-skill package available | App check pending | App check pending | Pending | Pending |
| Antigravity IDE | Two-skill package available | IDE check pending | IDE check pending | Pending | Pending |

Keep the 12 disabled legacy Claude account entries backed up. Leave the two absent explicit-only skills uninstalled. All 14 explicit-only skills remain excluded from Antigravity and from any receiving mode whose automatic-invocation control is unverified.

Engineering uses 6,482 description characters. Its budget remains subject to its 6,000-character warning and 8,000-character hard limit. A package count or menu entry cannot pass its actual discovery check.

## Live failures and remaining checks

Codex CLI 0.153.2 selected motion review and read its reference for the three positive cases. The near-miss cases used other routes. All ten original prompts ran with synthetic task data. Nine met their bounded acceptance checks. Safety case 3 asked for a runnable app and recording provider instead of proposing test-local observations or separately consented research. No recording was installed. This fails the original case expectation; it is not an adoption pass.

Claude Code CLI 2.1.220 read the correct reference and preserved the failed keyboard check and missing study evidence. Its response put file paths before the supported finding. That failed the result-first check. The next batch was stopped before the ten original cases.

Antigravity CLI 1.1.27 read both the motion reference and the synthetic fixture through its file tool. Its answer invented a duration over five seconds, called an unspecified check automated, and suggested a code cause without code evidence. The two-skill preview was disabled. The second canary, ten original cases, and 64-skill expansion remain pending.

The affected Codex and Claude Code engineering packs are disabled. Each contains 25 skills, so 53 skills remain enabled in the other six packs. Saved packages and settings are available for rollback. Active tasks were not restarted. The failure checks do not establish failures in untested app modes.

All 63 enabled account entries were downloaded before replacement. Their saved files carry version 0.11.0. Native Replace retained their entries; refreshed contents and new downloads match every file in the approved 0.12.0 ZIPs. The save flow completed without a warning; it did not expose a separate scan report. The motion upload was submitted, but app access stopped before its result could be checked. Inspect the existing library before another upload.

Fresh app inventories, mounted file hashes, downloads, invocation controls, interruption, resumption, and intentional goal changes remain open. App access became unavailable before those checks finished. Keep each pending row separate. These records do not complete the 108-episode benefit study.

## Check and restore

1. Save the old package or account download and its file hashes. Confirm the backup opens.
2. Update one reviewed batch through the app's native route. Replace the existing entry when available.
3. Check the full inventory and every file hash. Read a linked reference in a fresh test task.
4. Run positive, near-miss, and safety prompts. Check detail, failed checks, unfinished work, interruption, resumption, and an intentional goal change. Test a real result download.
5. If a check fails, stop that batch. Restore the saved package through the native route or leave the affected entry disabled. Preserve the failed result. Continue independent apps.

Do not restart active user tasks to force an update. Ten motion cases are required on each CLI; representative cases and shared file checks are required in each app. These checks do not complete the separate 108-episode benefit study.

## History

The [0.11 account repair](claude-account-repair-2026-09-08.md) and [continuity candidate](continuity-candidate.md) retain their own scope, failures, and versions. Old manifests and observations remain historical evidence.
