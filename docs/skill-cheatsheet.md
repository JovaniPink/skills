# JovaniPink Skills Cheatsheet

Use this page to find a skill quickly. The catalog contains 62 skills across five plugins. For installation and client details, read [How to Use JovaniPink Skills](README.md). For fuller explanations, read the [Skill Catalog Reader Guide](skill-catalog-reader-guide.md).

## Invocation legend

- `Implicit`: The client may select the skill when the request clearly matches its description. You can still select it directly when the client supports direct selection.
- `Explicit-only`: The skill must be selected directly. Selecting it does not authorize push, merge, deletion, publication, deployment, credential use, or another protected action.

Common direct-selection forms:

| Client | Form |
| --- | --- |
| ChatGPT | Type `@`, then select the installed skill. |
| Codex | Use `$plugin-name:skill-name`. |
| Claude Code | Use `/plugin-name:skill-name`. |
| Claude.ai | Use a matching request. Direct explicit-only behavior is not claimed for this surface. |

## Core: jovanipink-skills

Use this plugin for verification, research, diagnosis, authority boundaries, publication safety, and agent-package security.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `authority-boundary-review` | Maps authoritative stores, writers, readers, projections, custody, and reconciliation paths. | Implicit |
| `claim-verification` | Checks whether claims such as complete, fixed, merged, deployed, or live have current evidence. | Implicit |
| `cross-stack-quality-gates` | Discovers and runs the validation commands defined by the repository instead of assuming universal commands. | Implicit |
| `prelaunch-readiness` | Reviews repository, provider, deployment, and live evidence before a public launch. | Implicit |
| `public-private-boundary-review` | Finds secrets, private details, proprietary material, and unsupported public claims before publication. | Implicit |
| `publish-change-safely` | Verifies identity, repository, remote, branch, diff, checks, push, and pull request state. | Explicit-only |
| `skill-import-provenance` | Gates Jovani-owned skill transfers and rejects third-party catalog material as an implementation source. | Explicit-only |
| `skill-security-review` | Audits skills and plugins for unsafe instructions, permissions, dependencies, hooks, and data exposure. | Implicit |
| `source-grounded-research` | Researches current questions with primary sources, URLs, dates, provenance, and uncertainty. | Implicit |
| `systematic-diagnosis` | Reproduces and narrows a defect to establish a causal boundary without silently implementing a fix. | Implicit |

## Engineering: jovanipink-engineering

Use this plugin for the software lifecycle, application quality, architecture, review, testing, and controlled execution.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `accessibility-review` | Reviews semantics, keyboard use, assistive technology needs, and visual presentation against WCAG 2.2. | Implicit |
| `acceptance-evidence-ledger` | Tracks substantial work against current evidence, freshness, blockers, and visible abandonments. | Explicit-only |
| `api-contract-compatibility-review` | Checks API, event, schema, and client changes for backward, forward, and rollout compatibility. | Implicit |
| `application-security-review` | Reviews authentication, authorization, input handling, data protection, sessions, configuration, and abuse risks. | Implicit |
| `code-change-review` | Reviews an exact diff for correctness, regressions, security, compatibility, test quality, and maintainability. | Implicit |
| `data-migration-readiness` | Reviews migration authority, sequencing, compatibility, reconciliation, rollback, and operational evidence. | Implicit |
| `dependency-supply-chain-review` | Reviews dependencies, lockfiles, registries, CI actions, artifacts, provenance, and compromise risk. | Implicit |
| `finish-development-branch` | Presents evidence-based pull request, merge, retention, and cleanup choices for a development branch. | Explicit-only |
| `implementation-planning` | Produces a decision-complete plan with interfaces, steps, tests, rollout controls, and stopping conditions. | Implicit |
| `merge-conflict-reconciliation` | Reconciles merge, rebase, or cherry-pick conflicts while preserving both sides' intent. | Explicit-only |
| `module-interface-design` | Designs smaller, clearer, and more stable module boundaries, vocabulary, and contracts. | Implicit |
| `multi-agent-orchestration` | Coordinates authorized, independent tasks with ownership, evidence contracts, cost awareness, and reconciliation. | Explicit-only |
| `observability-design` | Designs logs, metrics, traces, alerts, and user-impact signals around operational decisions. | Implicit |
| `operational-readiness-review` | Reviews monitoring, capacity, failure handling, runbooks, recovery, incidents, and support ownership. | Implicit |
| `performance-scalability-diagnosis` | Diagnoses latency, throughput, resource use, contention, and capacity problems from measurements. | Implicit |
| `plan-execution` | Executes a named approved plan with checkpoints, validation, deviation tracking, and stopping boundaries. | Explicit-only |
| `problem-framing` | Defines users, outcomes, evidence, constraints, unknowns, options, and measurable success before implementation. | Implicit |
| `prototype-spike` | Builds a bounded disposable experiment to answer one technical uncertainty. | Explicit-only |
| `request-code-review` | Prepares an evidence-bounded review packet and sends it only with separate authorization. | Explicit-only |
| `respond-to-code-review` | Verifies review feedback against current code, tests, contracts, and authority before acting on it. | Implicit |
| `test-driven-change` | Guides behavioral changes through red, green, refactor, and documented exception evidence. | Implicit |
| `test-quality-review` | Checks whether tests have meaningful assertions, defect sensitivity, isolation, determinism, and risk coverage. | Implicit |
| `test-strategy` | Selects risk-proportionate unit, integration, contract, end-to-end, property, migration, and manual tests. | Implicit |
| `worktree-isolation` | Assesses whether dirty or concurrent Git work should be isolated before worktree changes are authorized. | Implicit |

## Stack profiles: jovanipink-stack-profiles

Use these optional profiles after repository commands and toolchains have been discovered.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `go-engineering-profile` | Adds focused guidance for Go modules, packages, concurrency, APIs, tests, dependencies, and builds. | Implicit |
| `postgresql-sql-engineering-profile` | Adds focused guidance for schemas, queries, transactions, indexes, migrations, and database testing. | Implicit |
| `python-engineering-profile` | Adds focused guidance for packaging, typing, asynchronous behavior, tests, dependencies, and builds. | Implicit |
| `swift-swiftui-engineering-profile` | Adds focused guidance for Swift concurrency, SwiftUI state, tests, compatibility, and Apple builds. | Implicit |
| `terraform-engineering-profile` | Adds focused guidance for modules, providers, state, plans, upgrades, and infrastructure review. | Implicit |
| `typescript-javascript-engineering-profile` | Adds focused guidance for type safety, asynchronous behavior, tests, dependencies, and browser or Node builds. | Implicit |

## Operations: jovanipink-operations

Use this plugin for requirements, governance, measurement, adoption, incidents, and stakeholder decisions.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `change-adoption-planning` | Plans the people, behavior, capability, incentives, support, measurement, and feedback needed for change. | Implicit |
| `cross-capability-dependency-mapping` | Maps dependencies across products, teams, data, platforms, decisions, and operating capabilities. | Implicit |
| `data-authority-migration-ratification` | Prepares authority, cutover, reconciliation, rollback, and acceptance evidence for a decision owner. | Implicit |
| `decision-governance-records` | Records decision context, options, evidence, ownership, status, consequences, and review triggers. | Implicit |
| `iteration-postlaunch-learning` | Uses observed behavior, incidents, feedback, experiments, and measures to decide what changes next. | Implicit |
| `kpi-outcome-measurement` | Defines outcomes with units, populations, baselines, targets, data authority, and decision use. | Implicit |
| `production-incident-analysis` | Reconstructs incidents from timestamped evidence and identifies justified learning without manufacturing blame. | Implicit |
| `requirements-synthesis` | Converts interviews, documents, issues, observations, and constraints into traceable requirements. | Implicit |
| `stakeholder-technical-communication` | Explains technical evidence for a named stakeholder decision without hiding risk or uncertainty. | Implicit |
| `value-attribution-evidence-maturity` | Distinguishes observations, estimates, contribution, attribution, and causal value claims. | Implicit |
| `workshop-planning-synthesis` | Plans decision-focused workshops and records evidence, decisions, actions, and unresolved questions. | Implicit |

## Reasoning: jovanipink-reasoning

Use this plugin for alignment, explanation, impact analysis, technical writing, configuration, and continuity.

| Skill | What it does | Invocation |
| --- | --- | --- |
| `alignment-interview` | Establishes shared understanding by inspecting evidence and asking one material question at a time. | Implicit |
| `change-impact-analysis` | Traces change effects across callers, contracts, storage, jobs, clients, security, rollout, and operations. | Implicit |
| `codebase-explanation` | Explains current code through entry points, ownership, control flow, data flow, state, interfaces, and failures. | Implicit |
| `decision-evidence-trace` | Maintains an auditable decision log without storing hidden reasoning, secrets, or raw transcripts. | Explicit-only |
| `design-rationale-investigation` | Investigates why a design exists using history, current behavior, constraints, and competing hypotheses. | Implicit |
| `domain-vocabulary-modeling` | Builds a proposed vocabulary of concepts, definitions, relationships, invariants, authorities, and contradictions. | Implicit |
| `guided-configuration` | Guides a person through protected configuration steps and verifies each observable result. | Explicit-only |
| `high-signal-technical-writing` | Makes technical writing clearer, more specific, less repetitive, and easier to act on without changing its meaning. | Implicit |
| `portable-skill-authoring` | Designs portable skills with precise routing, invocation policy, provenance, security boundaries, and evaluations. | Implicit |
| `task-handoff` | Creates a continuation record with revisions, evidence, decisions, blockers, and authority boundaries. | Explicit-only |
| `workflow-retrospective` | Reviews completed work to identify what helped, what failed, and which bounded improvement to test next. | Explicit-only |

## Quick selection by need

| If you need to... | Start with... |
| --- | --- |
| Verify whether work is actually complete or live | `claim-verification` |
| Research a current technical question | `source-grounded-research` |
| Diagnose a defect without immediately changing code | `systematic-diagnosis` |
| Clarify a vague request | `problem-framing` or `alignment-interview` |
| Turn an approved direction into executable steps | `implementation-planning` |
| Execute an approved plan | `plan-execution` |
| Track a substantial implementation against current acceptance evidence | `acceptance-evidence-ledger` |
| Review a diff | `code-change-review` |
| Decide what tests are needed | `test-strategy` |
| Review whether existing tests are meaningful | `test-quality-review` |
| Check a change's downstream effects | `change-impact-analysis` |
| Explain an unfamiliar codebase | `codebase-explanation` |
| Check application security | `application-security-review` |
| Check an agent skill or plugin for security risks | `skill-security-review` |
| Prepare a safe repository publication | `publish-change-safely` |
| Prevent private details from entering public work | `public-private-boundary-review` |
| Prepare requirements from several sources | `requirements-synthesis` |
| Record a decision and its evidence | `decision-governance-records` |
| Explain technical evidence to a stakeholder | `stakeholder-technical-communication` |
| Improve technical documentation | `high-signal-technical-writing` |
| Continue work in another session or client | `task-handoff` |

## Safety reminder

A skill guides workflow and judgment. It does not replace repository protections, host permissions, tests, access controls, or human approval. Keep local, committed, pushed, reviewed, merged, deployed, and live states separate.
