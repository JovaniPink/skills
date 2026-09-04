# Google Agent Surfaces

Reviewed: 2026-09-04

Google's models, developer clients, hosted harnesses, application frameworks, lifecycle tools, data tools, and production platform are separate evidence surfaces. Canonical skill semantics may be shared, but compatibility and behavioral claims are recorded independently in [`catalog/google-surfaces.json`](../catalog/google-surfaces.json). Cross-lane aggregation is forbidden.

## Surface map

| Surface | Evidence question | Current catalog position |
| --- | --- | --- |
| Gemini model | Which exact model and effort minimize cost per successful case? | Execution-envelope variable, not a skill-compatibility claim. Availability and pricing come from current API release and deprecation records. |
| Antigravity CLI | Does a focused treatment improve a clean local Google coding agent? | Primary future Google behavioral-portability lane, blocked until the Codex pilot identifies a useful treatment. |
| Gemini CLI Enterprise | Does intentionally licensed enterprise access load the projection? | Conditional compatibility only. Gemini CLI 0.56.0 evidence is historical and does not establish this claim. |
| Antigravity Desktop | Does usefulness survive the visual surface? | Manual observational parity after a useful CLI result. |
| Antigravity SDK | Can the same semantics run safely through Google's Python harness? | Separate runtime-harness lane even if it shares implementation with the CLI. |
| Gemini Managed Agent | Can a mounted skill improve a hosted sandboxed agent? | Separate synthetic/public hosted lane with a preregistered cost ceiling and retention policy. |
| Google ADK | Can an immutable bundle load without granting authority? | Separate runtime-compatibility lane owned by `jovanipink-adk`. |
| Agents CLI | Can a coding agent safely evaluate or prepare Google deployments? | Lifecycle-tool lane. Provider actions require explicit RELEASE authority and readback. |
| Data Agent Kit | Can vendor skills and MCP tools support governed data work? | Preview tool/plugin lane; never product-semantic or evaluation authority. |
| Gemini Enterprise Agent Platform | Can an application meet production identity, governance, runtime, memory, evaluation, and observability requirements? | Product/runtime evidence, never blended with skill behavior. |

## Antigravity precondition and isolation contract

No Antigravity runner belongs in the v0.1 lab until the complete Codex pilot identifies a useful focused treatment or a narrower replacement. The eventual host-specific runner must pin the `agy` version and binary digest, use a disposable Linux container or dedicated clean OS user, inject API authentication as a secret, and start without global skills, plugins, MCP servers, memories, prior conversations, or vendor skill packs.

Each paired run must use fresh pinned worktrees, a natural empty configuration home, fixed model and effort, sandboxed scoped permissions, a fixed network policy, and headless JSON or stream-JSON evidence. The grader must parse terminal result status and tool events; process exit code zero is not sufficient evidence of success.

The current seven-skill Delivery TypeScript profile is blocked on Antigravity because it contains the explicit-only `publish-change-safely` skill. Current reviewed Antigravity documentation exposes implicit discovery and slash invocation but no verified model-invocation disable control equivalent to the Codex or Claude projections. A future Antigravity treatment must either preserve that control or use a separately named experimental profile that excludes the skill.

## Packaging boundary

Agent Plugins 1.0 and Antigravity's native plugin format are not treated as identical. The portable specification uses `plugin.json` with `mcp.json`; the reviewed Antigravity documentation describes its own manifest schema and `mcp_config.json`. A skills-only Agent Plugins proof package is deferred until a selected conformant client accepts a minimal package. Antigravity-native packaging remains a separate projection unless live evidence proves compatibility.

Packaging never establishes installation trust, sandboxing, credential scope, permission safety, provenance, or behavioral improvement.

## Cost, freshness, and authority

Managed Agents are excluded from the first quantitative Google lane because current documentation permits 100,000 to 3 million tokens per interaction. Data Agent Kit is Preview. Neither surface is inferred from Antigravity CLI evidence.

Do not hard-code a preferred Gemini model into a portable skill. Record exact model and effort in each execution envelope, check current Gemini API release and deprecation records, and compare cost per successful case. Documentation reviewed for this release reports Gemini 3.8 Flash as generally available with introductory pricing ending December 31, 2026; that observation is volatile and is not a permanent catalog recommendation.

Do not install, authenticate, deploy, publish, or enable provider actions as part of deterministic catalog validation. Agents CLI `infra`, `deploy`, and `publish` commands require explicit RELEASE authority and post-action provider readback. Managed Agent calls require separate credential, cost, retention, environment-deletion, tool, and network authorization.

## Primary sources

- Google, [Gemini CLI to Antigravity CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)
- Google, [Antigravity Agent Skills](https://antigravity.google/docs/skills/)
- Google, [Antigravity plugins](https://www.antigravity.google/docs/cli/plugins/)
- Agent Plugins, [Agent Plugins 1.0 specification](https://agent-plugins.org/specification)
- Google, [Antigravity headless mode](https://antigravity.google/docs/cli/headless/)
- Google, [Antigravity SDK](https://www.antigravity.google/docs/sdk/overview)
- Google, [Gemini Managed Agents](https://ai.google.dev/gemini-api/docs/agents)
- Google Cloud, [Data Agent Kit overview](https://docs.cloud.google.com/data-agent-kit/overview)
- Google, [Gemini model documentation](https://ai.google.dev/gemini-api/docs/latest-model)
- Google, [Agents CLI](https://developers.googleblog.com/agents-cli-in-agent-platform-create-to-production-in-one-cli/)
- Google Cloud, [Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview)
