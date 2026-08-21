# Client mapping

Client capabilities change independently. Verify current official documentation and record the exact client and version before claiming support.

## Portable invariants

- Delegation requires host and user authorization.
- Each worker receives a bounded task, ownership boundary, evidence contract, and stop condition.
- Parallel tasks must be independent enough to reconcile safely.
- Worker completion is an input to integration review, not proof of correctness.
- Publication, deletion, deployment, and merge decisions stay with the authorized integration owner.

## Codex

Codex can expose subagents, threads, and worktree-based isolation depending on the surface and version. Use only the mechanisms available in the current host. Consult the current [OpenAI Codex documentation](https://learn.chatgpt.com/docs) before describing behavior.

## Claude

Claude Code can expose subagents, and some versions can expose experimental agent teams with different coordination behavior. Consult the current [Claude subagent documentation](https://code.claude.com/docs/en/sub-agents) and [Claude agent team documentation](https://code.claude.com/docs/en/agent-teams). Record unsupported behavior as unsupported rather than inferring parity.
