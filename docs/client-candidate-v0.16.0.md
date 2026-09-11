# Current candidate and client checks

Catalog version: 0.16.0

Updated: 2026-09-11

The candidate has 79 skills in seven packs, the same set as 0.15.0. No skill was added or removed. `skill-security-review` gained two review domains, and the observation records gained a session-depth field.

## What changed

`skill-security-review` now inspects two surfaces it previously skipped. The first is agent-facing configuration shipped inside a reviewed package, meaning `AGENTS.md`, `CLAUDE.md`, and their subtree variants. Those files are instructions the agent loads, and a review that reads only the skill body misses them. The second is client-shipped behavior overrides, meaning output styles, hooks, commands, and bundled agents, with attention to any that apply without asking the user first.

The observation schema gained `session_depth`, `turn_index`, and a per-file `surfaces_covered` declaration. Records at catalog 0.10.0 or later must declare session depth.

## Structured observations were restored

Machine-checked observation records stopped at 0.9.0. Six releases recorded their client checks only in prose. `docs/release-process.md` already required separate observation records; the step was skipped.

Three matrices are restored from the candidate documents that recorded them at the time: [0.13](client-observations-v0.13.json), [0.14](client-observations-v0.14.json), and [0.15](client-observations-v0.15.json). Each record cites the candidate document and section it came from, so a transcribed record is distinguishable from a live capture. Records reconstructed this way are marked `historical`.

0.10, 0.11, and 0.12 are not restored. `client-candidate-v0.12.0.md` records its checks as prose without a per-case table, and 0.10 and 0.11 have no candidate record at all. Filing a record for them would mean inventing per-case detail that was never written down.

The old surface rule demanded a fixed set of six surfaces per matrix and rejected any partial one. That rule is the likeliest reason recording stopped: after 0.9 no release was tested on all six, so nothing could be filed at all. Each matrix now declares the surfaces it covers, and the validator checks the records against that declaration.

## Holds carried forward

Both command-line engineering holds were lifted at 0.14.0 and stay lifted. `functional-motion-review` was not edited at 0.15.0 or 0.16.0, so that lift still rests on the bytes it was observed against.

The Antigravity CLI expansion is installed and enabled across all 65 eligible implicit skills on CLI 1.2.0, with behavioral testing sampled across five skills. The Claude account upload hold on the 14 explicit-only skills is unchanged. No app or IDE mode has been tested on any client.

## What these observations do not cover

Every record in every matrix was captured at the first turn of a fresh session. The restored matrices say so explicitly; the nine older ones were taken the same way but predate the field.

That is the condition under which instruction adherence is strongest. Published benchmarks find it falls as a conversation grows: Li and others report significant instruction drift within eight rounds ([arXiv:2402.10962](https://arxiv.org/abs/2402.10962), COLM 2024), and MMMT-IF measures instruction following dropping from 0.81 at turn 1 to 0.64 at turn 20 across three frontier models ([arXiv:2409.18216](https://arxiv.org/abs/2409.18216)).

Neither studies Agent Skills on any client this catalog targets. Applying them here is an extrapolation and is labeled as one.

**HOLD-TURN-DEPTH.** No skill in this catalog may be described as governing a working session. Current records support a narrower claim: that a skill routes correctly and returns its output contract at the start of a fresh session.

The hold lifts when the ten `functional-motion-review` cases have been run at a recorded turn index inside a continued session on one client, scored by whether the reply still carries the skill's named output sections, and filed as records with `session_depth` set to `continued_session`. [The study design](turn-depth-study.md) states the method, the scoring, and the limits it cannot escape.

## A stated limit carried from 0.15.0

`finding-consolidation` ships beside the seven skills whose output it consumes. On Antigravity CLI 1.2.0, `code-change-review` was observed emitting three of the four SARIF severity grades and a finding state on a pinned diff. The remaining six adopting skills are still unobserved on a live client.

## Required before behavior can be claimed

1. Install 0.16.0 through each client's native route and record the exact client version.
2. Confirm every installed file matches the generated source.
3. Run `skill-security-review` against a package that ships agent-facing configuration and a behavior override, and confirm both appear as findings rather than passing unmentioned.
4. Run an adopting skill and confirm the reply carries a severity from the four words, and a finding state only where a change was pinned.
5. Record the full execution envelope, including session depth.

A pass on one client does not establish another. These checks do not complete the separate 108-episode benefit study.

## History

The [0.15.0 checks](client-candidate-v0.15.0.md), [0.14.0 checks](client-candidate-v0.14.0.md), [0.13.0 checks](client-candidate-v0.13.0.md), [0.12.0 checks](client-candidate-v0.12.0.md), and [0.11 account repair](claude-account-repair-2026-09-08.md) retain their own scope, failures, and versions. Old manifests and observations remain historical evidence.
