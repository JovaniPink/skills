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

Use only Jovani-owned work and primary authorities needed for format, interoperability, or correctness: laws, specifications, standards bodies, and official platform documentation. Discovery links, community discussions, and third-party skill catalogs are not implementation authorities.

## Clean-room boundary

Do not copy external text, examples, names, structure, scripts, or distinctive expression. Third-party skill catalogs are not tracked, cited, mirrored, compared, installed, or used as implementation sources. Any external investigation occurs outside Git and may influence rejection or safety boundaries only. Current skills must remain independently authored from Jovani-owned work and the applicable primary authority.

Repository-independence validation rejects external skill-repository links and install identifiers, repository-to-repository capability mappings, source-specific attribution, and non-primary behavior provenance. Jovani-owned repository links and pinned CI Action dependency provenance are narrow operational exceptions; CI dependencies do not authorize skill behavior.

## Placement policy

A capability belongs in the public core only when it is reusable across independent contexts, independently sourceable, safe to expose, and testable without private facts. It belongs in a private overlay when correct use depends on a private authority, identity, topology, contract, dataset, customer, or product. It belongs in neither when it is proprietary, unsafe, obsolete, duplicative, unsupported, or lacks demonstrated use.

## Revocation

Remove an item from generated distributions and marketplaces through ordinary reviewed commits when its license, authorship, security behavior, or provenance cannot be supported. Preserve Git history and a migration notice in `deprecated/` when users need a safe replacement path.
