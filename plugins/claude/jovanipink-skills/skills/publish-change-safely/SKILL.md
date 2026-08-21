---
name: publish-change-safely
description: Publish an authorized repository change by verifying identity, remote, branch, diff scope, checks, commit, push, PR state, and repository visibility. Use only when the user explicitly asks to commit, push, publish, or open a pull request.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.5.0"
  plugin: "jovanipink-skills"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "external-write"
disable-model-invocation: true
---

# Publish Change Safely

Perform only the publication actions the user authorized. Repository identity, transport identity, review state, merge, deployment, and live behavior are separate facts.

## Workflow

1. Restate the authorized action and stopping point: commit, push, PR, or another named boundary.
2. Inspect working-tree status, current branch, remotes, upstream, and recent history.
3. Verify the account or credential used by the publishing channel. Do not assume Git transport and hosting API identities match.
4. Review the exact staged and unstaged scope. Preserve unrelated user changes. Never stage everything without first resolving new, deleted, secret-like, generated, or binary files.
5. Run the relevant repository gates or report why they remain incomplete.
6. Create a focused commit using the repository's real convention. Do not invent attribution or coauthor trailers.
7. Re-read the remote before pushing when concurrent changes are plausible. Never force-push, rewrite shared history, change visibility, or alter branch protection without explicit authorization.
8. Push only the intended branch and verify the resulting remote revision.
9. If authorized, open or update a PR with evidence-bounded claims. Do not merge unless the user separately authorized merge.
10. Report exact commit, remote branch, PR/check state, and all actions not performed.

## Stop conditions

Stop before mutation when identity, target repository, branch, staged scope, secret exposure, history divergence, or requested authority is unclear. A rejected push is not permission to rebase, merge, or force.
