# Choose Your Skills

Start with the smallest exact skill selection that covers the current decision. Plugins distribute skills; profiles select which skills should be activated or exposed for a bounded kind of work.

Clients discover skills from their names and descriptions before loading full instructions. Installing unrelated skills spends discovery space and can create routing collisions. OpenAI documents an initial Codex skill-list budget of 2 percent of the context window, or 8,000 characters when the context size is unknown. This catalog warns at 6,000 characters because system instructions and unrelated installed skills also use context.

Plugin measurements live in [`catalog/packs.json`](../catalog/packs.json). Skill-level activation profiles and their per-surface measurements live in [`catalog/profiles.json`](../catalog/profiles.json). The measurements include canonical discovery descriptions, not the full instruction bodies.

## Pick one plugin first

| Need | Start with |
| --- | --- |
| Verify claims, research, diagnose, or review public exposure | `jovanipink-skills` |
| Plan, implement, test, review, or finish engineering work | `jovanipink-engineering` |
| Apply stack-specific judgment after repository discovery | `jovanipink-stack-profiles` |
| Work on requirements, decisions, measurement, adoption, or incidents | `jovanipink-operations` |
| Improve alignment, explanation, writing, continuity, or skill authoring | `jovanipink-reasoning` |
| Evaluate AI behavior, context reliability, or source conformance | `jovanipink-ai-systems` |
| Review an agent architecture, Google ADK design, tool boundary, protocol, security model, or retrieval system | `jovanipink-agent-platforms` |

The engineering plugin is held on the Codex and Claude Code command lines after a live motion-review failure. Read the [current candidate checks](client-candidate-v0.13.0.md) before you enable it.

The engineering plugin is also above the 6,000-character warning threshold. That threshold is a repository guardrail for pack discovery size, not a limit published by any client. Install the pack when its broad lifecycle coverage is useful. For a narrow task, directly select the needed skill and avoid enabling unrelated plugins.

## Experimental activation profile

`delivery-typescript-experimental` selects seven exact capabilities for a bounded TypeScript delivery task. It exists to support baseline-versus-treatment experiments; it is not a default recommendation and must not be described as behaviorally verified until reviewed receipts support that claim.

Profile budgets are surface-specific. Codex observations record its current initial skill-list behavior, including shortening or omission. Claude Code observations separately record its listing budget, per-entry truncation, overrides, and retained descriptions. No single portable character ceiling is asserted.

## Small recipes

Recipes are suggested combinations, not separate installable products. Do not assume a client can install only a recipe unless that exact behavior has been observed for that client.

| Work | Skills |
| --- | --- |
| Verify a completion claim | `claim-verification`, `acceptance-evidence-ledger` |
| Plan a safe code change | `problem-framing`, `implementation-planning`, `test-strategy` |
| Review a public release | `public-private-boundary-review`, `prelaunch-readiness`, `publish-change-safely` |
| Diagnose with evidence | `systematic-diagnosis`, `claim-verification` |
| Review an AI workflow | `agent-evaluation-design`, `context-reliability-review`, `source-output-conformance-audit` |
| Secure an agent system | `agent-context-state-memory-design`, `agent-tool-action-boundary-review`, `agentic-system-security-review` |
| Review a Google ADK system | `google-adk-engineering-profile`, `agent-evaluation-design`, `agentic-system-security-review` |
| Review a service release | `application-security-review`, `operational-readiness-review`, `observability-design` |
| Write a decision brief | `source-grounded-research`, `decision-governance-records`, `stakeholder-technical-communication` |
| Connect research to evaluated public findings | `research-to-publication-lifecycle`, `source-grounded-research`, `workflow-retrospective` |
| Learn after launch | `iteration-postlaunch-learning`, `kpi-outcome-measurement`, `production-incident-analysis` |

All recommended recipes are measured and must remain below 8,000 discovery-description characters. The validator rejects stale measurements and over-limit recipes.

## Add a stack profile only when the repository needs it

Use `cross-stack-quality-gates` to discover the repository's actual commands. Add the matching stack profile when you need language or platform judgment. A profile does not replace repository scripts, wrappers, lockfiles, CI, or platform evidence.

## Add agent-platform skills only for agent-system work

The `jovanipink-agent-platforms` plugin is for people designing or reviewing agent systems through ChatGPT, Codex, Claude, or Antigravity CLI. Gemini CLI is a conditional enterprise compatibility surface after Google's individual-user transition. The plugin is not a runtime bundle for a SaaS agent.

Read [Google agent surfaces](google-agent-surfaces.md), [Google ADK](google-adk.md), and [Agent platform boundaries](agent-platform-boundaries.md) before using those workflows in a Google agent project.

## Check invocation and maturity

An explicit-only skill requires direct selection. Direct selection chooses the workflow but does not grant permission to push, merge, publish, deploy, delete, or write to an external system.

Use [`catalog/skills.json`](../catalog/skills.json) to check invocation, risk, maturity, companions, and routing conflicts. Use [`catalog/evidence.json`](../catalog/evidence.json) for the orthogonal behavioral, client, and runtime state. Candidate workflow maturity and missing behavioral evidence are different claims.

## Primary resources

- [OpenAI skill-building guide](https://learn.chatgpt.com/docs/build-skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [Google's Gemini CLI to Antigravity CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)
- [Antigravity Agent Skills](https://antigravity.google/docs/skills/)
