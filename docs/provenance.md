# Provenance Policy

Every canonical skill has an entry in `provenance/catalog.json`.

## Dispositions

- `original`: independently authored for this repository
- `clean-room`: independently authored from public requirements or capability descriptions without copying protected expression
- `adapted`: derived from compatible source material with license and attribution recorded
- `vendored`: retained substantially as published, with exact revision and license
- `rejected`: reviewed but not eligible for distribution

## Required evidence

Each entry records source URL, license, pinned revision or an explicit non-applicable value, review date, material reviewed, local changes, security disposition, re-review triggers, and revocation conditions.

Discovery links and community discussions may explain why a capability matters but do not establish a technical fact or a reuse license. Prefer specifications, official product documentation, original publisher material, and repository license files.

## Clean-room boundary

Proprietary or incompatible sources may be used only to identify a capability gap. Do not copy their text, examples, names, structure, scripts, or distinctive expression. Author from public primary sources and Jovani-owned compatible work, and record the resulting disposition.

## Revocation

Remove an item from generated distributions and marketplaces when its license, authorship, security behavior, or provenance cannot be supported. Preserve a migration notice in `deprecated/` when users need a safe replacement path.
