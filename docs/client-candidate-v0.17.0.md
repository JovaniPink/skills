# Measured Skills candidate

Catalog version: 0.17.0

Updated: 2026-09-21

This candidate retains 79 skills and splits engineering into build, review, and delivery, for nine packs. Publisher metadata is Measured Studios. The source repository has not transferred. See the [migration guide](measured-migration.md).

## Evidence boundaries

Native adapters and package checks do not prove client discovery, behavioral benefit, or sustained-session adherence. No new 0.17.0 client behavior is claimed here. Prior [0.16.0 evidence](client-candidate-v0.16.0.md) retains its original identity and limits. Explicit-only and turn-depth holds remain in effect on unverified surfaces.

## PR 44 disposition

The [independent review](https://github.com/JovaniPink/skills/pull/44) proposes remediation; its documentation-only patch does not implement fixes.

| Finding | Disposition | Evidence |
| --- | --- | --- |
| Explicit-only mapping | Preserved | Native adapters and mapping tests remain authoritative for structure, not observed behavior. |
| Description-only size | Addressed | Discovery estimates include names, repository-relative paths, separators, and descriptions. Absolute install path and client serialization overhead remain unknown. |
| Private pre-commit hook | Deferred | Policy-only repository forbids hooks; its existing validator is not a comprehensive secret scanner. |
| Motion routing length | Addressed | Canonical description shortened; full safety meaning remains in the workflow. Fresh activation requires rechecking. |
| Engineering pack size | Addressed | Three packs; focused activation is tested separately from packaging. |
| Offline security claim | Addressed | SECURITY.md distinguishes offline packaging from opt-in network checks and host tool permissions. |
| Behavioral evidence gap | Partial | Historical observations remain separately dated; unsupported current skill and comparison records stay unobserved. |

No release tag, marketplace update, deployment, or global-default promotion follows from preparing this candidate.
