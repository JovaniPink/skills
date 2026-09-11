# Current candidate and client checks

Catalog version: 0.15.0

Updated: 2026-09-10

The candidate has 79 skills in seven packs, one more than 0.14.0. It adds `finding-consolidation` to `jovanipink-skills` and adopts the shared finding vocabulary in seven review skills.

Seven skills now grade each finding `none`, `note`, `warning`, or `error`. Those that review a pinned change also mark each finding `new`, `unchanged`, `updated`, or `absent`; those that review a system or a package report severity alone and say so. `public-private-boundary-review` keeps its `BLOCK`, `REVIEW`, and `CLEAR` dispositions, which state what the reader must do rather than how bad a finding is. `functional-motion-review` is deferred because its 0.13.0 checks are still pending and a third revision would attach pending evidence to a body that no longer exists.

`finding-consolidation` merges findings that several completed reviews already produced. It assigns one owner per root cause, regrades onto the one scale, ranks by reader impact, and discloses what it held back. It reads findings; it does not run a review.

Source binding, manifest commit, and merge commit are pending.

| App or mode | Prepared | Installed | Enabled | Loaded | Behavior-tested |
| --- | --- | --- | --- | --- | --- |
| Codex CLI | Pending | Pending | Pending | Pending | Pending |
| Codex desktop | Pending | Pending | Pending | Pending | Pending |
| ChatGPT Work | Pending | Pending | Pending | Pending | Pending |
| ChatGPT web | Pending | Pending | Pending | Pending | Pending |
| Claude Code CLI | Pending | Pending | Pending | Pending | Pending |
| Claude desktop Code | Pending | Pending | Pending | Pending | Pending |
| Claude.ai Chat | Pending | Pending | Pending | Pending | Pending |
| Claude desktop Chat | Pending | Pending | Pending | Pending | Pending |
| Cowork | Pending | Pending | Pending | Pending | Pending |
| Antigravity CLI (1.2.0, 5-skill preview) | Done | Done | Done | Done | Done |
| Antigravity desktop | Pending | Pending | Pending | Pending | Pending |
| Antigravity IDE | Pending | Pending | Pending | Pending | Pending |

All 14 explicit-only skills remain excluded from Antigravity and from any receiving mode whose automatic-invocation control is unverified. The new skill is implicit, so the explicit-only count is unchanged. The Claude account upload hold is unchanged.

`jovanipink-skills` moves from 2,952 to 3,319 description characters and stays within budget. `jovanipink-engineering` is unchanged at 6,665 and stays in warning.

## Holds carried forward

Both command-line engineering holds were lifted at 0.14.0 and stay lifted. The Antigravity expansion stays held. No app or IDE mode has been tested on any client.

## A stated limit of this release

`finding-consolidation` ships in the same release as the seven skills whose output it consumes. No adopting skill has yet been observed emitting a severity on a real client, so the consolidator's input format is authored rather than observed.

That is a deliberate choice, and it has a cost: if a later client observation fails, the wording change and the new skill cannot be separated by bisecting this release. Record which of the two produced a failure by testing an adopting skill on its own before testing consolidation.

## Required before behavior can be claimed

1. Install 0.15.0 through each client's native route and record the exact client version.
2. Confirm every installed file matches the generated source.
3. Run an adopting skill on its own and confirm the reply carries a severity from the four words, and a finding state only where a change was pinned.
4. Run two reviews on one artifact, then confirm consolidation returns one owned finding per root cause with every location inside it.
5. Confirm the three near-miss cases do not select consolidation, especially the single-review case.
6. Record the full execution envelope: client and version, model and reasoning setting, skill content identity, loaded instructions, tools, permission mode, and fresh-session status.

A pass on one client does not establish another. These checks do not complete the separate 108-episode benefit study.

## Antigravity CLI 1.2.0 observation (5-skill preview)

Tested on 2026-09-10 against Antigravity CLI 1.2.0 (`agy`), self-updated past 1.1.26 Homebrew cask metadata. The 5-skill preview (`accessibility-review`, `code-change-review`, `finding-consolidation`, `functional-motion-review`, `performance-scalability-diagnosis`) was built with `scripts/build_antigravity.py` into `dist/antigravity-eval-0.15.0/plugin`, installed via `agy plugin install`, and enabled with `agy plugin enable jovanipink-antigravity-preview`.

### Observations:
1. **Permission resolution on near-miss case 3 (`functional-motion-review-near-miss-3`)**:
   - Prompt: "Diagnose server query latency without interactive presentation; use performance-scalability-diagnosis."
   - Executed with `agy --dangerously-skip-permissions --print`.
   - Result: Completed successfully (exit 0). Selected and executed `performance-scalability-diagnosis`, emitting all named output sections (`## Hypotheses`, `## Measurements`, `## Causal Diagnosis`, `## Capacity Estimate`, `## Next Experiment`). This resolves the 0.14.0 unscored near-miss case where non-interactive permission was denied.

2. **0.15.0 finding vocabulary adoption check (`code-change-review`)**:
   - Tested positive case 1 against a pinned Go authentication session diff.
   - Result: Completed with exit 0. Emitted `## Findings` with findings ordered by severity (`error`, `warning`, `note`), all matching SARIF severity values, and marked `State: new` against the base revision. Emitted `## Questions`, `## Validation`, and `## Review Boundary`.

3. **`finding-consolidation` (Skill #79) multi-review consolidation**:
   - Tested positive case 1 (merging 3 review inputs across `application-security-review`, `code-change-review`, `accessibility-review` with an overlapping auth vulnerability).
   - Result: Completed with exit 0. Grouped the overlapping defect under a single owner (`application-security-review`), preserved both locations, resolved the severity disagreement (`warning` vs `error`) to `error` with stated justification in `## Disagreements`, preserved `accessibility-review` finding as a separate owned item, and disclosed `## Sources`, `## Held Back: None`, and `## Uncovered Scope`.

4. **`finding-consolidation` single-review near-miss check (`finding-consolidation-near-miss-3`)**:
   - Prompt: "Only one review has run so far. Summarize its findings."
   - Result: Refused multi-source consolidation explicitly ("multi-source consolidation is not applicable (which requires two or more completed reviews)"), adhering to precondition boundaries and summarizing the single review.

## History

The [0.14.0 checks](client-candidate-v0.14.0.md), [0.13.0 checks](client-candidate-v0.13.0.md), [0.12.0 checks](client-candidate-v0.12.0.md), and [0.11 account repair](claude-account-repair-2026-09-08.md) retain their own scope, failures, and versions. Old manifests and observations remain historical evidence.
