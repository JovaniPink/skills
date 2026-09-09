# Claude account repair check

Catalog version: 0.11.0

Observed on September 8, 2026, US Eastern time. The web receipt was created on September 9 in UTC. This is a bounded install and use check, not a study of workflow benefit.

## Account repair

The account library began with 61 catalog entries. The Code plugins were already at 0.11.0, but most account uploads were older. Updating Code had not updated those uploads.

All 61 entries were downloaded and backed up before replacement or disabling. The two files in claim-verification already matched the approved package and were kept. We replaced 48 entries and added 14 missing skills. Twelve old explicit-only entries were disabled after backup; two missing explicit-only skills remain uninstalled. No entries were deleted.

The refreshed web library has 75 unique catalog entries: 63 enabled and 12 disabled. Downloads of all 63 enabled skills match the complete file sets in the generated 0.11.0 packages. The 77 prepared ZIPs also match their checksum file. Preparation does not approve the 14 held workflows for Chat.

## Separate observations

| App or CLI | Prepared and installed | Enabled and loaded | Behavior tested |
| --- | --- | --- | --- |
| Claude account library in Chrome | 63 approved skills match downloaded files; 12 legacy entries backed up and held; 2 holds uninstalled | Refreshed list shows 63 enabled and 12 disabled | Replacement, addition, disable, and library refresh observed |
| Fresh Claude.ai Chat | Same approved 0.11.0 files | Runtime receipt has 63 unique skills and 99 files, all matching; no held skill mounted | Requested references read; status, resumption, and changed objective observed; artifact download failed |
| Claude Code CLI 2.1.220 | Seven 0.11.0 packs; 132 packaged files match the generated source | Fresh process lists 77 namespaced catalog skills and commands; requested files read from the local marketplace checkout | Direct invocation, linked references, status, resumption, changed objective, and one near-miss prompt observed |
| Claude desktop Chat | Pre-repair library inspected; post-repair check pending | Fresh desktop session not checked | Not established by the web result |
| Claude desktop Code mode | Prior package-page observation only | Fresh task check pending | Not established by the CLI result |
| Cowork | No new observation in this repair | Not checked | Not established |

## Evidence limits

The web check used Sonnet 5 Medium. Its execution tool inspected actual mounted files and produced a JSON receipt and inspection script. We copied the receipt from the file viewer and compared the sorted file paths and SHA-256 hashes locally. All 99 files matched. The inspection reported no read errors. The expected file manifest was not uploaded.

Runtime artifact downloads failed through both the individual controls and Download all. Copying the receipt allowed file comparison, but does not pass the artifact-download check. Account skill archive downloads worked; those are a different download path.

The CLI used its configured Opus 5 model and read-only tools in plan permission mode. A sandboxed attempt could not access the saved login. A separate host-level run succeeded. Both results are retained. The successful synthetic task kept a failed required check and an unrun integration check through status and resumption. A direct handoff request read the installed skill and reference. A related conceptual question used no tools. These observations do not prove every invocation case.

Keep the 14 explicit-only account workflows held. Their metadata is not proof that Chat enforces direct selection. Desktop and Cowork need their own checks. The 108-episode communication study remains unrun, and no adoption benefit is claimed.

Private backups, account entry IDs, prompts, runtime receipts, and per-file comparisons are kept outside the public catalog.
