# Security Policy

## Supported version

Only the latest tagged release is supported. Before the first release, report issues against the current default branch.

## Reporting

Do not open a public issue containing credentials, private repository names, customer data, internal infrastructure identifiers, or reproducible exploit details. Contact the repository owner privately through the security-reporting channel listed on their public profile.

Include the affected skill or script, revision, client surface, observed behavior, impact, and the smallest safe reproduction. Remove live secrets and personal data.

## v0.1 boundary

The catalog intentionally ships no skill-level executables, hooks, MCP servers, installation scripts, or broad tool grants. Repository scripts use the Python standard library for deterministic validation and packaging. A skill may recommend an action, but host permissions and explicit user authorization remain authoritative.

See [docs/security-model.md](docs/security-model.md) for the threat model and review criteria.
