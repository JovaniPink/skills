# Review domains

## Instruction influence

- attempts to override higher-priority instructions or hide actions
- absolute behavioral directives, impersonation, misleading UI, or false completion claims
- untrusted content copied into prompts or lifecycle context

## Command and filesystem behavior

- shell interpolation, destructive commands, unsafe temporary paths, traversal, symlinks
- reads outside the declared scope, credential locations, dotfiles, and broad recursive writes
- scripts whose behavior differs from their description

## Network and supply chain

- outbound destinations, authentication handling, downloads, package installation, update channels
- unpinned revisions, mutable releases, transitive dependencies, binaries, generated assets
- install-time, startup, background, and update-time execution

## Permissions and lifecycle

- tool grants broader than the workflow needs
- hooks, scheduled tasks, subagents, monitors, or services that run without current consent
- capability differences across hosts and sandbox modes

## Data handling

- secret, source, prompt, log, telemetry, and user-data exposure
- retention, cache, archive, and cleanup behavior
- output that could disclose private repository or operational context

## Rereview triggers

At minimum, flag changes to hooks, scripts, dependencies, manifests, tool grants, network destinations, activation instructions, and packaging logic.
