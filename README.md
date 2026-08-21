# JovaniPink Skills

Portable, evidence-oriented agent skills for software delivery, research, operations, and publication. The canonical source follows the open [Agent Skills specification](https://agentskills.io/specification); generated distributions add native controls for Codex and Claude.

This repository is an independent MIT-licensed work. It does not redistribute proprietary skill text. Public skills remain separate from private, repository-local overlays.

Start with [How to use JovaniPink Skills](docs/README.md) for secure installation, invocation, validation, updating, removal, troubleshooting, and client resource links.

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

Engineering quality reviews in the same plugin cover application security, dependency supply chain, observability, performance and scalability, data migration readiness, API compatibility, test quality, accessibility, and operational readiness. These are implicit, read-only reviews and do not claim compliance or authorize production actions.

### `jovanipink-stack-profiles`

Optional profiles provide focused engineering guidance for Go, Python, Swift and SwiftUI, TypeScript and JavaScript, PostgreSQL and SQL, and Terraform. `cross-stack-quality-gates` remains the command-discovery orchestrator and uses a profile only when installed and applicable.

### `jovanipink-operations`

Eleven generic operating workflows cover requirements, governance records, workshops, outcome measurement, value evidence, adoption, dependencies, stakeholder communication, postlaunch learning, incident analysis, and data-authority migration ratification. They preserve observed, proposed, ratified, rejected, unresolved, measured, estimated, and causal claim states.

## Repository model

- `skills/` is the only authoring source.
- `plugins/codex/<plugin>/` and `plugins/claude/<plugin>/` are generated and committed.
- `incubator/` is intentionally undiscoverable unfinished work.
- `evals/` contains trigger and safety cases.
- `provenance/catalog.json` records the origin and review policy of every skill.
- `provenance/inventory-summary.json` publishes only reconciled aggregate capability-disposition counts.
- `scripts/` contains standard-library-only generation, packaging, and validation, including a guard that rejects mutable third-party GitHub Action references.
- `catalog/` contains strict compatibility, deprecation, revocation, and upstream-pinning records.
- `releases/` contains exact-source release manifests and artifact checksums.

Do not hand-edit generated plugin trees. Change the canonical skill, then run:

```sh
python3 scripts/build_distributions.py
python3 scripts/package_claude_ai.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

## Installation surfaces

### Codex CLI and ChatGPT desktop

Add this repository as a marketplace, then install the focused plugins you need. The Codex distribution uses `agents/openai.yaml`; explicit-only skills set `policy.allow_implicit_invocation: false`. Installed plugin skills are namespaced, so direct invocation uses forms such as `$jovanipink-engineering:plan-execution`.

OpenAI documents plugin-bundled skills for Chat and Work on ChatGPT web, desktop, and mobile, plus Codex in the ChatGPT desktop app and Codex CLI. A repository marketplace added through the CLI is the local desktop testing path; it does not by itself install the plugin into a ChatGPT web account. Workspace or directory installation and publication are separate administrative actions. See the [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills) and [OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).

### Claude Code and desktop

Add the repository's `.claude-plugin/marketplace.json` as a self-hosted marketplace and install the focused plugins you need. Generated explicit-only skills add `disable-model-invocation: true`. Direct plugin invocation uses Claude's namespace, for example `/jovanipink-engineering:plan-execution`.

### Claude.ai

Run `python3 scripts/package_claude_ai.py`. Upload an individual ZIP from `dist/claude-ai/`; each archive contains one correctly nested skill directory.

See [client-surface research](docs/client-surface-research.md) for the official distribution distinctions and current observed limitations.

Client behavior can change independently. See [manual smoke tests](docs/manual-smoke-tests.md) for observed-versus-pending evidence instead of assuming parity.

Private product or organization facts use the repo-local overlay model described in [Private overlays](docs/private-overlays.md); they never enter the public catalog.

## Security and contribution policy

The catalog ships no skill-level executables, hooks, MCP servers, bundled agents, or broad tool grants. Skills coordinate judgment; scripts and host permissions enforce deterministic requirements. CI uses immutable commit pins for third-party Actions and validation rejects mutable replacements. Read [SECURITY.md](SECURITY.md), [the security model](docs/security-model.md), and [the authoring guide](docs/authoring.md) before contributing.

## Status

Version 0.4 adds operating workflows and catalog lifecycle controls. Public-directory submission and cross-client parity claims remain deferred until field testing is recorded.
