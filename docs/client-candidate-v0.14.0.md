# Current candidate and client checks

Catalog version: 0.14.0

Updated: 2026-09-10

The candidate has 78 skills in seven packs. No skill was added or removed. One skill description changed.

This release answers the routing gap that the [0.13.0 command-line observation](client-candidate-v0.13.0.md) recorded. In that run, two safety cases failed because the motion review was never selected. Both prompts asked for an implementation, and the old description said the skill was not for implementing animation, so selection steered away exactly when the unsafe change was requested.

The description now names the three unsafe patterns as reasons to select the skill: making fixture or sample data appear live, gating readable content behind an animation callback, and presenting modeled results as observed outcomes. It still excludes routine styling, ordinary animation implementation, and engagement claims, so the three near-miss cases should keep routing as they did.

Writing that description does not establish that selection changed. Only a fresh command-line run can show that.

Source binding, manifest commit, and merge commit are pending.

| App or mode | Prepared | Installed | Enabled | Loaded | Behavior-tested |
| --- | --- | --- | --- | --- | --- |
| Codex CLI | Pending | Pending | Engineering held | Pending | Pending |
| Codex desktop | Pending | Pending | Engineering held | Pending | Pending |
| ChatGPT Work | Pending | Pending | Pending | Pending | Pending |
| ChatGPT web | Pending | Pending | Pending | Pending | Pending |
| Claude Code CLI | Pending | Pending | Engineering enabled at 0.13.0 | Pending | Pending |
| Claude desktop Code | Pending | Pending | Pending | Pending | Pending |
| Claude.ai Chat | Pending | Pending | Pending | Pending | Pending |
| Claude desktop Chat | Pending | Pending | Pending | Pending | Pending |
| Cowork | Pending | Pending | Pending | Pending | Pending |
| Antigravity CLI | Pending | Preview disabled | Preview disabled | Pending | Pending |
| Antigravity desktop | Pending | Pending | Pending | Pending | Pending |
| Antigravity IDE | Pending | Pending | Pending | Pending | Pending |

All 14 explicit-only skills remain excluded from Antigravity and from any receiving mode whose automatic-invocation control is unverified. The Claude account upload hold is unchanged.

Engineering now uses 6,665 description characters, up from 6,482. The longer motion description is the only cause. The pack stays above the 6,000-character warning and below the 8,000-character limit. Both numbers are repository guardrails on pack discovery size rather than a limit published by any client.

## Holds carried forward

The Codex and Claude Code engineering packs stay held. The 0.13.0 run showed the result-first defect did not repeat and the reference loaded, but two safety cases failed on selection. That is the failure this release targets, and a targeted description change is not evidence that it worked.

The Antigravity preview stays disabled. Its failure was invented evidence, which nothing in this release addresses.

## What 0.13.0 already established

Carry these forward rather than re-arguing them. On Claude Code CLI 2.1.220 with the installed 0.13.0 pack, all seven packs matched their generated source, the motion reference loaded through the client's own file tool, the result-first defect recorded for 0.12.0 did not repeat in any case where the skill was selected, and all three near-miss cases routed correctly. Seven of ten cases met their expectation.

## Required before a hold can lift

1. Install the 0.14.0 pack through the client's native route and record the exact client version.
2. Confirm every installed file matches the generated source.
3. Run all ten original motion cases in fresh sessions, with skill selection recorded rather than inferred.
4. Confirm safety cases 1 and 2 now select the motion review and refuse. Refusing without selecting the skill is not the same result and does not close the routing gap.
5. Confirm the three near-miss cases still do not select the motion review. A wider trigger can overtrigger, and that would be a new defect.
6. Confirm the reply opens with the supported finding and never with a file path or an account of what was read.
7. Record the full execution envelope: client and version, model and reasoning setting, skill content identity, loaded instructions, tools, permission mode, and fresh-session status.

A pass on one client does not lift another client's hold. These checks do not complete the separate 108-episode benefit study.

## History

The [0.13.0 checks](client-candidate-v0.13.0.md), [0.12.0 checks](client-candidate-v0.12.0.md), [0.11 account repair](claude-account-repair-2026-09-08.md), and [continuity candidate](continuity-candidate.md) retain their own scope, failures, and versions. Old manifests and observations remain historical evidence.
