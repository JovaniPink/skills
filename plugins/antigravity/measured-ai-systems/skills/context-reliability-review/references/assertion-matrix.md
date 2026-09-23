# Assertion Matrix Reference

Use this reference for assertion-level context audits. The model follows provenance relationships described by [W3C PROV](https://www.w3.org/TR/prov-n/) while keeping the review language and status model specific to this catalog.

## Assertion Anatomy

An assertion is a claim used by the consuming agent or workflow. Record:

- the entity or subject the assertion describes;
- the source entity and the activity that collected or transformed it;
- the responsible issuer or authority;
- effective time, recorded time, observation time, and expiration;
- the permitted audience, purpose, environment, and actions;
- derivation, conflict, supersession, and revocation links;
- the behavior or decision affected when the assertion is wrong or unavailable.

## Status Rules

| Status | Meaning |
| --- | --- |
| `RELIABLE` | Current evidence supports the assertion within its authority and permission scope. |
| `QUALIFIED` | The assertion is usable only with an explicit limitation or narrower scope. |
| `STALE` | Its freshness rule is violated or currentness cannot be established. |
| `CONFLICTED` | Relevant sources disagree and no ratified resolution rule settles the conflict. |
| `REVOKED` | An authorized event invalidated the assertion for the reviewed use. |
| `UNVERIFIED` | The source, authority, or supporting evidence cannot be established. |

## Time Discipline

Effective time answers when the assertion was true in the modeled world. Recorded time answers when a system captured it. Observation time answers when the reviewer inspected it. Never substitute one for another. A later recording can describe an earlier effective fact, and a recently observed cache can still contain revoked context.
