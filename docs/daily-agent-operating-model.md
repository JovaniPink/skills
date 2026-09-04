# Daily Agent Operating Model

Use the smallest surface and authority envelope that can complete the work. The normal progression is:

```text
ChatGPT Chat
understand -> research -> challenge -> decide
        |
        v
small implementation contract
        |
        v
Codex
inspect -> implement -> test -> review -> exact-head result
        |
        v
ChatGPT when needed
critique -> architecture decision -> next direction
```

Use ChatGPT Work between Chat and Codex when the decision requires heterogeneous sources, browser activity, files, apps, or a substantial artifact. Handoff the resulting decision, not the entire research transcript.

## Implementation contract

Keep a handoff small enough to review and complete enough to execute:

```text
Outcome:

Decision and concise rationale:

Repositories and relevant files:

Constraints and non-goals:

Acceptance criteria:

Required validation:

Permission, Git, PR, deployment, and external-effect boundaries:

Remaining unknowns:
```

The contract does not imply permission to merge, deploy, publish, mutate a provider, use credentials, or contact another person. Name those actions explicitly when they are authorized.

## Trust profiles

| Profile | Codex posture | Claude equivalent | Intended work |
| --- | --- | --- | --- |
| `EXPLORE` | Read-only, on-request approval, human review | `plan` | Research, diagnosis, architecture, and audits |
| `BUILD` | Workspace-write, on-request approval, automated review only for bounded and reversible work | `acceptEdits` with narrow rules | Implementation and test loops |
| `RELEASE` | Workspace-write, on-request approval, human review | `default` with explicit ask and deny rules | Publication, release, credentials, migrations, provider changes, and external effects |

Instructions are context, not enforcement. Filesystem scope, network policy, permission rules, hooks, repository protections, and provider controls enforce boundaries.

## Memory placement

| Information | Durable location |
| --- | --- |
| Universal or team rule | `AGENTS.md` and checked-in documentation |
| Repository or domain fact | Repository documentation or a repository-local skill |
| ChatGPT personal context | ChatGPT memory |
| Codex learned local context | Local Codex memory |
| Claude learned local context | Claude auto memory |
| Current task state | Explicit artifact, issue, branch, or pull request |
| Secret | None of these locations |

Keep client memory systems separate. Disable local Codex memory ingestion for sessions that use external context such as MCP, web search, or tool search. Treat Claude auto memory as machine-local context rather than policy or authority.

## Work data boundary

For behavioral lab experiments, keep the Work Cloud lane synthetic or public until a separate private-data protocol is reviewed. Ordinary Work use may access private connected systems when the task benefits and the account, app, action, retention, network, and confirmation settings are narrowly scoped.

Do not place sensitive private context, untrusted web content, broad connected-account access, and consequential write capability in one ambient trust zone.

## Subagents and deterministic graduation

Use subagents for self-contained, read-heavy exploration, test or failure analysis, security review, and compatibility review. Keep coupled planning, shared-context implementation, integration, and final decisions in the main task.

After the third occurrence of a workflow, review whether it should become a deterministic script or tool. Graduate sooner when reproducibility, compliance, idempotency, or error cost requires it. Repetition triggers review; it does not automatically require automation.
