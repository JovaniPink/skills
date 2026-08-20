# Provenance Policy

Every canonical skill has an entry in `provenance/catalog.json`.

## Capability dispositions

- `covered`: a shipped public skill supplies the generic capability
- `partial`: a shipped public skill covers part of the capability and names the remaining gap
- `public_candidate`: independently authorable and useful across unrelated contexts
- `private_overlay`: correct execution depends on a private authority, identity, topology, contract, dataset, customer, or product
- `rejected`: proprietary, unsafe, obsolete, duplicative, unsupported, or without demonstrated use

Capability disposition is separate from implementation method. An implementation method is `original`, `clean-room`, `adapted`, `vendored`, `reference-only`, or `not-applicable`.

## Required evidence

Each public entry records source URL, license, pinned revision or an explicit non-applicable value, review date, material reviewed, local changes, capability disposition, implementation method, security disposition, re-review triggers, and revocation conditions. `provenance/schema.json` is authoritative and rejects unknown fields, wrong types, invalid dates or URLs, unsupported enum values, and missing required evidence.

Discovery links and community discussions may explain why a capability matters but do not establish a technical fact or a reuse license. Prefer specifications, official product documentation, original publisher material, and repository license files.

## Clean-room boundary

Proprietary or incompatible sources may be used only to identify a capability gap. Do not copy their text, examples, names, structure, scripts, or distinctive expression. Author from public primary sources and Jovani-owned compatible work, and record the resulting disposition.

The private inventory ledger records one row per capability with a source snapshot, reviewer, review date, capability-name/path-only material consulted, and required false values for `content_opened`, `text_copied`, and `implementation_reused`. The public repository exposes only the reconciled aggregate in `provenance/inventory-summary.json`; it never exposes the private names or paths.

## Placement policy

A capability belongs in the public core only when it is reusable across independent contexts, independently sourceable, safe to expose, and testable without private facts. It belongs in a private overlay when correct use depends on a private authority, identity, topology, contract, dataset, customer, or product. It belongs in neither when it is proprietary, unsafe, obsolete, duplicative, unsupported, or lacks demonstrated use.

## Revocation

Remove an item from generated distributions and marketplaces when its license, authorship, security behavior, or provenance cannot be supported. Preserve a migration notice in `deprecated/` when users need a safe replacement path.
