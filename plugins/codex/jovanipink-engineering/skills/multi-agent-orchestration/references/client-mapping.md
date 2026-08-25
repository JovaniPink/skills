# Client mapping

Client capabilities change independently. Verify current official documentation and record the exact client and version before claiming support.

## Portable invariants

- Delegation requires host and user authorization.
- Each worker receives a bounded task, ownership boundary, evidence contract, and stop condition.
- Parallel tasks must be independent enough to reconcile safely.
- Worker completion is an input to integration review, not proof of correctness.
- Publication, deletion, deployment, and merge decisions stay with the authorized integration owner.

## Codex

Codex can expose subagents and inspectable threads depending on the surface and version. Current OpenAI documentation describes delegation after a direct request or applicable project or skill instruction in local Codex clients. ChatGPT Work availability and triggering differ by account and intelligence level; eligible Ultra sessions can delegate suitable work proactively. Record the exact surface, account capability, model, reasoning level, permission mode, and version. Do not treat one trigger path as proof for another. Consult the current [OpenAI subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) before describing behavior.

Each subagent performs its own model and tool work, so parallel work uses more tokens than a comparable single-agent run. Use the smallest useful fanout and keep write-heavy work isolated. A child model or reasoning configuration may inherit from the parent or be explicitly configured; verify the actual configuration instead of assuming it.

## Claude

Claude Code can expose subagents, and some versions can expose experimental agent teams with different coordination behavior. Consult the current [Claude subagent documentation](https://code.claude.com/docs/en/sub-agents) and [Claude agent team documentation](https://code.claude.com/docs/en/agent-teams). Record unsupported behavior as unsupported rather than inferring parity.
