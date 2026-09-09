# Daily agent workflow

Use Codex, Claude Code, or Antigravity for the work each can do in your setup. No client is the required starting point. Pick one based on the files, tools, and permissions the task needs.

## Choose where to work

| Need | What to check before you start |
| --- | --- |
| Research or discuss a decision | The app can reach the sources and show its evidence. |
| Write or review code | The app or CLI can open the right checkout and run its checks. |
| Make a document or other result file | The client can save it where you can find and open it. |
| Resume work elsewhere | The receiving client has the needed files and a short handoff. |

ChatGPT, Claude chat, Cowork, and the coding apps may use different files and tools. Check the exact mode. A shared account does not prove shared skills or memory.

## State the task

Give the agent a clear goal and the checks that define success:

```text
Goal:
Files or repository:
What is already done:
Required checks:
What may change:
Actions already approved:
Open questions:
```

The agent should keep working through brief status questions. If you change the goal, say so. It should carry that change into its next update.

## Match permissions to the work

For reading and review, use a setup that limits edits. For building, allow changes only where the task needs them. For publishing or release work, name the destination and the approved actions.

Check each client's actual settings. Codex sandbox options, Claude permission modes, and Antigravity sandbox and file rules are different controls. Similar names do not prove that they allow the same actions. A plan mode alone does not prove read-only access.

Skill text guides the agent. File access rules, tool permissions, and repository protections enforce limits. Selecting a skill does not grant permission to merge, deploy, use credentials, or contact someone.

## Keep useful updates

Lead with the result or current decision. Keep failures, unknowns, and unfinished work visible. Give detail when it is requested. Name the next action only if there is one.

At a pause or handoff, save this record:

```text
Active goal:
Current branch, commit, and changed files:
Completed work and evidence links:
Checks, results, and when they ran:
Unfinished work and blockers:
Existing approvals and their limits:
Next action:
```

Open those evidence links in the receiving client. Recheck facts that may have changed. A handoff should let work resume without retelling the full conversation.

## Put notes where they belong

- Shared rules belong in repository guidance and docs.
- Project facts belong in project docs or project skills.
- Personal preferences belong in the client's user instructions or rules.
- Current work belongs in a task record, issue, branch, or pull request.
- Secrets belong in approved secret storage, never in skills or memory notes.

Keep each client's memory separate from shared policy. Do not assume a local memory file syncs to a web or remote task. Check the loaded instructions before relying on a preference.

For lab studies, use made-up or public data until a separate private-data plan is approved. In ordinary work, keep connected accounts and tools limited to the task.

Use parallel agents only when the task allows it and their work can stay separate. After a workflow repeats several times, consider a tested script if that would make it more reliable.

See [client support](client-support.md) for setup and use checks across all three CLIs and their apps.
