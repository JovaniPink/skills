# JovaniPink Skills

Reusable skills for coding, research, writing, and reviews. Codex, Claude Code, and Antigravity have equal priority for setup and testing. We build native Codex and Claude packages and an offline Antigravity preview. See [client support](docs/client-support.md) for what is ready and what still needs testing. The source uses the open [Agent Skills format](https://agentskills.io/specification).

This repository is an independent MIT-licensed work. It does not redistribute proprietary skill text. Public skills remain separate from private, repository-local overlays.

Start with the [five-minute quickstart](docs/quickstart.md) or [How to use JovaniPink Skills](docs/README.md). Use [Choose Your Skills](docs/choose-your-skills.md), the [skill cheatsheet](docs/skill-cheatsheet.md), or the [skill catalog reader guide](docs/skill-catalog-reader-guide.md) for selection. The [taxonomy](docs/taxonomy.md) explains capability, lifecycle, target, risk, invocation, and maturity facets. The [behavioral evidence model](docs/behavioral-evidence-model.md) separates workflow maturity, observed client behavior, and runtime eligibility. The [daily agent operating model](docs/daily-agent-operating-model.md) explains how to choose a client and pass work between tasks. The [Google agent surfaces](docs/google-agent-surfaces.md) record keeps Antigravity, Gemini enterprise compatibility, hosted agents, ADK, and lifecycle tooling in separate lanes.

## Catalog

A plugin bundles related skills for installation. A profile selects the skills to use for a task. Installing a plugin and enabling all its skills are separate choices.

### `jovanipink-skills`

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `claim-verification` | Test material claims against current authority-class evidence | Implicit |
| `source-grounded-research` | Research with primary sources, dates, provenance, and uncertainty | Implicit |
| `research-to-publication-lifecycle` | Connect sources, forecasts, outcomes, evaluations, retrospectives, and public-safe findings | Explicit-only |
| `systematic-diagnosis` | Establish a causal diagnosis without silently fixing the system | Implicit |
| `authority-boundary-review` | Map authoritative stores, projections, writers, readers, and contracts | Implicit |
| `cross-stack-quality-gates` | Discover and run safe repository-defined gates across supported application, language, data, and infrastructure stacks | Implicit |
| `prelaunch-readiness` | Audit web, service, and application launch readiness | Implicit |
| `publish-change-safely` | Verify identity, scope, checks, push, and PR state | Explicit-only |
| `public-private-boundary-review` | Detect private data, internal identifiers, secrets, and unsupported public claims | Implicit |
| `skill-security-review` | Audit skill instructions, dependencies, permissions, and network behavior | Implicit |
| `skill-import-provenance` | Gate Jovani-owned skill transfers and reject third-party catalog imports | Explicit-only |

### `jovanipink-engineering`

| Skill | Purpose | Invocation |
| --- | --- | --- |
| `acceptance-evidence-ledger` | Track substantial work against current evidence, freshness, blockers, and visible abandonments | Explicit-only |
| `problem-framing` | Establish outcomes, evidence, constraints, unknowns, and success before implementation | Implicit |
| `implementation-planning` | Produce decision-complete plans with interfaces, tests, rollout, and stopping conditions | Implicit |
| `plan-execution` | Execute an approved plan with checkpoints and deviation controls | Explicit-only |
| `test-driven-change` | Capture red, green, refactor, and exception evidence | Implicit |
| `test-strategy` | Select risk-proportionate test layers and evidence | Implicit |
| `worktree-isolation` | Assess dirty and concurrent work before authorized worktree changes | Implicit |
| `request-code-review` | Prepare and, only when authorized, send a bounded review request | Explicit-only |
| `respond-to-code-review` | Verify feedback before accepting, rejecting, or deferring it | Implicit |
| `finish-development-branch` | Present integration, retention, and cleanup options without implicit actions | Explicit-only |
| `multi-agent-orchestration` | Coordinate authorized independent tasks with ownership and reconciliation | Explicit-only |
| `code-change-review` | Review an exact diff for verified actionable defects | Implicit |
| `functional-motion-review` | Check whether motion clarifies a reader task while preserving evidence and control | Implicit |
| `module-interface-design` | Design smaller stable contracts from callers and invariants | Implicit |
| `prototype-spike` | Test one uncertainty with isolated bounded implementation | Explicit-only |
| `merge-conflict-reconciliation` | Reconcile Git conflicts while preserving abort and action gates | Explicit-only |

Engineering quality reviews in the same plugin cover application security, dependency supply chain, observability, performance and scalability, data migration readiness, API compatibility, test quality, accessibility, and operational readiness. These are implicit, read-only reviews and do not claim compliance or authorize production actions.

### `jovanipink-stack-profiles`

Optional profiles provide focused engineering guidance for Adobe AEM, C# and .NET, Go, Java and Spring, PHP and Drupal, Python, Salesforce and Apex, Swift and SwiftUI, TypeScript and JavaScript, PostgreSQL and SQL, and Terraform. `cross-stack-quality-gates` remains the command-discovery orchestrator and uses a profile only when installed and applicable.

### `jovanipink-operations`

Eleven generic operating workflows cover requirements, governance records, workshops, outcome measurement, value evidence, adoption, dependencies, stakeholder communication, postlaunch learning, incident analysis, and data-authority migration ratification. They preserve observed, proposed, ratified, rejected, unresolved, measured, estimated, and causal claim states.

### `jovanipink-reasoning`

Eleven focused workflows cover alignment interviews, domain vocabulary, codebase mechanics, design rationale, change impact, high-signal technical writing, privacy-conscious decision traces, portable skill authoring, guided configuration, task handoffs, and workflow retrospectives. The plugin is optional so these broad reasoning descriptions do not crowd every engineering session.

### `jovanipink-ai-systems`

Three optional AI-reliability workflows cover agent evaluation design, assertion-level context reliability, and exact source-to-output conformance. They are independently authored from Jovani-owned practice with NIST TEVV resources and W3C PROV used only as primary correctness authorities. The plugin launches no external evaluation and contains no private context, hooks, scripts, dependencies, bundled agents, or broad tool grants.

### `jovanipink-agent-platforms`

Six optional human-facing workflows cover Google ADK engineering, agent context and memory, tool and action boundaries, protocol interoperability, agentic-system security, and retrieval-grounding quality. They help people review agent systems through ChatGPT, Codex, Claude, and Antigravity CLI; Gemini CLI is a conditional enterprise compatibility surface after Google's individual-user transition. They are not runtime skill bundles, do not register tools, and do not authorize authentication, infrastructure, release, or deployment.

## Repository model

- `skills/` is the only authoring source.
- `plugins/codex/<plugin>/` and `plugins/claude/<plugin>/` are generated and committed.
- `incubator/` is intentionally undiscoverable unfinished work.
- `evals/` contains trigger and safety cases.
- `provenance/catalog.json` records primary format or correctness authorities and the Jovani-authored implementation boundary for every skill.
- `scripts/` contains standard-library-only generation, packaging, and catalog validation, plus a locked PyYAML gate for GitHub Actions workflow syntax.
- `catalog/` contains strict taxonomy, pack, recipe, profile, compatibility, behavioral-evidence, deprecation, revocation, upstream-review, and upstream-pinning records.
- `releases/` contains exact-source release manifests and artifact checksums.

Do not hand-edit generated plugin trees. Change the canonical skill, then run:

```sh
python3 scripts/build_distributions.py
python3 scripts/package_claude_ai.py
python3 scripts/check_workflows.py
python3 -m mypy --strict scripts tests
python3 -m ruff check scripts tests
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The Linux CI runner installs its reviewed workflow, type, and lint tools from `requirements-ci-linux.txt`. Other platforms should use PyYAML 6.0.3, types-PyYAML 6.0.12.20260815, mypy 1.20.2, and Ruff 0.15.12 from a trusted local environment; the Linux-only wheel lock is not a portable development environment.

## Installation surfaces

### Codex CLI and ChatGPT desktop

Add this repository as a marketplace, then install the focused plugins you need. The Codex distribution uses `agents/openai.yaml`; explicit-only skills set `policy.allow_implicit_invocation: false`. Installed plugin skills are namespaced, so direct invocation uses forms such as `$jovanipink-skills:claim-verification`.

OpenAI documents plugin-bundled skills for Chat and Work on ChatGPT web, desktop, and mobile, plus Codex in the ChatGPT desktop app and Codex CLI. A repository marketplace added through the CLI is the local desktop testing path; it does not by itself install the plugin into a ChatGPT web account. Workspace or directory installation and publication are separate administrative actions. See the [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills) and [OpenAI plugin documentation](https://developers.openai.com/plugins/build/plugins).

### Claude Code and desktop

Add the repository's `.claude-plugin/marketplace.json` as a self-hosted marketplace and install the focused plugins you need. Generated explicit-only skills add `disable-model-invocation: true`. Direct plugin invocation uses Claude's namespace, for example `/jovanipink-skills:claim-verification`.

The install command uses the form `plugin@marketplace`. One pack and the marketplace share the name `jovanipink-skills`. So `jovanipink-skills@jovanipink-skills` is correct, not a repeated word. See [Claude setup](docs/clients/claude.md) for the exact commands.

The `jovanipink-engineering` pack is held on the Codex and Claude Code command lines. A live motion review failed there. Install the other six packs first. Read the [current candidate checks](docs/client-candidate-v0.13.0.md) before you enable it.

### Claude.ai

Run `python3 scripts/package_claude_ai.py`. Upload an individual ZIP from `dist/claude-ai/`; each archive contains one correctly nested skill directory. The 14 explicit-only workflows are held. Do not upload one until the receiving mode has a verified control that stops automatic selection. A metadata field or a working slash command does not prove that control.

See [client-surface research](docs/client-surface-research.md) for the official distribution distinctions and current observed limitations.

Client behavior can change independently. See [manual smoke tests](docs/manual-smoke-tests.md) for observed-versus-pending evidence instead of assuming parity.

Private product or organization facts use the repo-local overlay model described in [Private overlays](docs/private-overlays.md); they never enter the public catalog.

## Security and contribution policy

The catalog ships no skill-level executables, hooks, MCP servers, bundled agents, or broad tool grants. Skills coordinate judgment; scripts and host permissions enforce deterministic requirements. CI uses immutable commit pins for third-party Actions and validation rejects mutable replacements. Read [SECURITY.md](SECURITY.md), [the security model](docs/security-model.md), and [the authoring guide](docs/authoring.md) before contributing.

## Status

The 0.13.0 candidate contains 78 skills across seven plugins. It states where a motion finding must appear. It names what to propose when comprehension evidence is missing. It also separates publication from review requests. See the [current candidate checks](docs/client-candidate-v0.13.0.md) for source review and installation states. These are authored changes, not measured benefits. Package checks, installed versions, and observed behavior are recorded separately for each app and CLI.

Claude Code plugins and Claude account uploads are separate installs. Updating the Code plugins does not update the account library used by Chat. See [Claude setup](docs/clients/claude.md) for the upload checks and explicit-only hold.

The experimental seven-skill Delivery TypeScript profile still has no valid behavioral result. Its corrected Codex pilot and the communication study remain pending. Neither establishes compatibility with other clients or ADK runtimes.
