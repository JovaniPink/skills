# Behavioral Evidence Model

This repository is the canonical public source for skill semantics and generated host projections. It is not the raw evidence store for private product experiments.

## Evidence dimensions

Four independent dimensions prevent one kind of evidence from standing in for another:

- `workflow_maturity` records whether the semantic workflow is incubating, a candidate, stable, or deprecated.
- `behavioral_evidence` records whether current observations are absent, partial, or verified, plus the version and observation date.
- `client_compatibility` records a status for an exact client, version, and model envelope.
- `runtime_eligibility` records whether a reviewed immutable bundle may enter a restricted runtime lifecycle.

A changed skill can remain semantically stable while behavioral evidence for its changed bytes becomes stale. Package generation does not prove client behavior. A runtime compatibility pass does not prove that a skill improves agent behavior.

## Evidence lanes

Do not blend success rates across these lanes:

- Codex behavioral evidence asks whether a focused treatment improves coding-agent behavior.
- Work/Desktop parity evidence is manual or observational and asks whether the capability remains useful on conversational or heterogeneous-task surfaces.
- Claude Code portability evidence asks whether canonical semantics survive Claude-specific discovery, invocation, instructions, memory, and permissions.
- ADK runtime evidence asks whether an immutable bundle can be loaded without expanding tools, identity, permissions, or release authority.

Each observation must preserve its execution envelope: exact client and version, model and reasoning setting, repository and skill content identities, activated profile, loaded instructions, memory state, tools, filesystem and network scope, permission mode, fresh-session status, session depth, and collection method.

Session depth is the turn the observation was taken at. Every record this repository holds was captured at the first turn of a fresh session. That is the condition where instruction adherence is strongest, so these records describe a skill's behavior at the start of a session and say nothing about its behavior later in one. See [the turn-depth study design](turn-depth-study.md).

## Profiles and budgets

[`catalog/profiles.json`](../catalog/profiles.json) contains exact ordered skill selections. Profiles do not replace plugins and are not automatically installable on every client. Their recorded description measurements are surface-specific.

Codex and Claude have different discovery budgets and truncation behavior. The catalog therefore records a separate policy and separate observations for each surface in `catalog/profiles.json`. It does not treat one client's published limit as a portable rule. A profile becomes a default only after behavior supports that decision.

Two measurements here look similar but mean different things. The first is a repository guardrail. [`catalog/packs.json`](../catalog/packs.json) warns at 6,000 characters and stops at 8,000. It counts the skill descriptions in one pack. That pair of numbers came from documented Codex behavior, and the catalog applies it to every pack so the packs stay comparable. No client publishes those numbers as a shared limit, and they say nothing about Claude. The second measurement is per surface. Those figures belong in the profile discovery measurements, where each one names the app or CLI it came from.

## Public/private boundary

Private prompts, case IDs, exact failure patterns, product catalog evolution, raw traces, and architecture details remain in private product repositories and the private lab. Public findings must be manually reviewed and deliberately generalized. A public statement may describe a broad finding, such as focused activation reducing inappropriate routing, without naming the private product or exposing its evidence.

## Repository instructions

The root `AGENTS.md` is short but sufficient for cross-cutting work. Before modifying a subtree, inspect its local `AGENTS.md`; for specialized work, launch Codex with that subtree as the working directory so the applicable instruction chain is loaded.

`CLAUDE.md` imports the shared `AGENTS.md`. Local Claude projections import colocated rules. These files provide context, not enforcement; sandbox, permission rules, and hooks own hard controls.
