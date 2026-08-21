# JovaniPink Skills

Portable, evidence-oriented agent skills for software delivery, research, operations, and publication. The canonical source follows the open [Agent Skills specification](https://agentskills.io/specification); generated distributions add native controls for Codex and Claude.

This repository is an independent MIT-licensed work. It does not redistribute proprietary skill text. Public skills remain separate from private, repository-local overlays.

## Catalog

The catalog is split into focused plugins so clients can discover only the workflows a user installs.

### `jovanipink-skills`

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

### `jovanipink-engineering`

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `problem-framing` | Establish outcomes, evidence, constraints, unknowns, and success before implementation | Implicit |
| `implementation-planning` | Produce decision-complete plans with interfaces, tests, rollout, and stopping conditions | Implicit |
| `plan-execution` | Execute an approved plan with checkpoints and deviation controls | Explicit only |
| `test-driven-change` | Capture red, green, refactor, and exception evidence | Implicit |
| `test-strategy` | Select risk-proportionate test layers and evidence | Implicit |
| `worktree-isolation` | Assess dirty and concurrent work before authorized worktree changes | Implicit |
| `request-code-review` | Prepare and, only when authorized, send a bounded review request | Explicit only |
| `respond-to-code-review` | Verify feedback before accepting, rejecting, or deferring it | Implicit |
| `finish-development-branch` | Present integration, retention, and cleanup options without implicit actions | Explicit only |
| `multi-agent-orchestration` | Coordinate authorized independent tasks with ownership and reconciliation | Explicit only |

## Repository model

- `skills/` is the only authoring source.
- `plugins/codex/<plugin>/` and `plugins/claude/<plugin>/` are generated and committed.
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

Add this repository as a marketplace, then install the focused plugins you need. The Codex distribution uses `agents/openai.yaml`; explicit-only skills set `policy.allow_implicit_invocation: false`. Installed plugin skills are namespaced, so direct invocation uses forms such as `$jovanipink-engineering:plan-execution`.

### Claude Code and desktop

Add the repository's `.claude-plugin/marketplace.json` as a self-hosted marketplace and install the focused plugins you need. Generated explicit-only skills add `disable-model-invocation: true`. Direct plugin invocation uses Claude's namespace, for example `/jovanipink-engineering:plan-execution`.

### Claude.ai

Run `python3 scripts/package_claude_ai.py`. Upload an individual ZIP from `dist/claude-ai/`; each archive contains one correctly nested skill directory.

Client behavior can change independently. See [manual smoke tests](docs/manual-smoke-tests.md) for observed-versus-pending evidence instead of assuming parity.

Private product or organization facts use the repo-local overlay model described in [Private overlays](docs/private-overlays.md); they never enter the public catalog.

## Security and contribution policy

The catalog ships no skill-level executables, hooks, MCP servers, bundled agents, or broad tool grants. Skills coordinate judgment; scripts and host permissions enforce deterministic requirements. CI uses immutable commit pins for third-party Actions and validation rejects mutable replacements. Read [SECURITY.md](SECURITY.md), [the security model](docs/security-model.md), and [the authoring guide](docs/authoring.md) before contributing.

## Status

Version 0.2 adds the engineering lifecycle plugin. Public-directory submission and cross-client parity claims remain deferred until field testing is recorded.
