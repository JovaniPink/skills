# JovaniPink Skills

Portable, evidence-oriented agent skills for software delivery, research, operations, and publication. The canonical source follows the open [Agent Skills specification](https://agentskills.io/specification); generated distributions add native controls for Codex and Claude.

This repository is an independent MIT-licensed work. It does not redistribute proprietary skill text. Public skills remain separate from private, repository-local overlays.

## Catalog

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `claim-verification` | Test material claims against current authority-class evidence | Implicit |
| `source-grounded-research` | Research with primary sources, dates, provenance, and uncertainty | Implicit |
| `systematic-diagnosis` | Establish a causal diagnosis without silently fixing the system | Implicit |
| `authority-boundary-review` | Map authoritative stores, projections, writers, readers, and contracts | Implicit |
| `cross-stack-quality-gates` | Discover and run safe gates for Go, Python, Swift, TypeScript/JavaScript, SQL, and Terraform | Implicit |
| `prelaunch-readiness` | Audit web, service, and application launch readiness | Implicit |
| `publish-change-safely` | Verify identity, scope, checks, push, and PR state | Explicit only |
| `public-private-boundary-review` | Detect private data, internal identifiers, secrets, and unsupported public claims | Implicit |
| `skill-security-review` | Audit skill instructions, dependencies, permissions, and network behavior | Implicit |
| `skill-import-provenance` | Review licensing, revisions, provenance, and revocation triggers | Explicit only |

## Repository model

- `skills/` is the only authoring source.
- `plugins/codex/jovanipink-skills/` and `plugins/claude/jovanipink-skills/` are generated and committed.
- `incubator/` is intentionally undiscoverable unfinished work.
- `evals/` contains trigger and safety cases.
- `provenance/catalog.json` records the origin and review policy of every skill.
- `provenance/inventory-summary.json` publishes only reconciled aggregate capability-disposition counts.
- `scripts/` contains standard-library-only generation, packaging, and validation, including a guard that rejects mutable third-party GitHub Action references.

Do not hand-edit generated plugin trees. Change the canonical skill, then run:

```sh
python3 scripts/build_distributions.py
python3 scripts/package_claude_ai.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

## Installation surfaces

### Codex CLI and desktop

Add this repository as a marketplace, then install the `jovanipink-skills` plugin. The Codex distribution uses `agents/openai.yaml`; explicit-only skills set `policy.allow_implicit_invocation: false`. Installed plugin skills are namespaced, so direct invocation uses forms such as `$jovanipink-skills:publish-change-safely`.

### Claude Code and desktop

Add the repository's `.claude-plugin/marketplace.json` as a self-hosted marketplace and install `jovanipink-skills`. Generated explicit-only skills add `disable-model-invocation: true`. Direct plugin invocation uses Claude's namespace, for example `/jovanipink-skills:publish-change-safely`.

### Claude.ai

Run `python3 scripts/package_claude_ai.py`. Upload an individual ZIP from `dist/claude-ai/`; each archive contains one correctly nested skill directory.

Client behavior can change independently. See [manual smoke tests](docs/manual-smoke-tests.md) for observed-versus-pending evidence instead of assuming parity.

Private product or organization facts use the repo-local overlay model described in [Private overlays](docs/private-overlays.md); they never enter the public catalog.

## Security and contribution policy

Version 0.1 ships no skill-level executables, hooks, MCP servers, or broad tool grants. Skills coordinate judgment; scripts and host permissions enforce deterministic requirements. CI uses immutable commit pins for third-party Actions and validation rejects mutable replacements. Read [SECURITY.md](SECURITY.md), [the security model](docs/security-model.md), and [the authoring guide](docs/authoring.md) before contributing.

## Status

This branch is a v0.1 foundation under validation. Public-directory submission and cross-client parity claims are deferred until field testing is recorded.
