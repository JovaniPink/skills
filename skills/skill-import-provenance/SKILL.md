---
name: skill-import-provenance
description: Import or adapt an agent skill only after verifying license, source, revision, authorship, security review, local changes, and rereview or revocation policy. Use only when the user explicitly asks to add, vendor, mirror, or adapt a skill from another source.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.5.0"
  plugin: "jovanipink-skills"
  invocation: "explicit"
  provenance: "clean-room"
  risk_class: "trust-decision"
---

# Skill Import Provenance

Do not copy first and investigate later. Read [provenance record](references/provenance-record.md) before proposing an import.

## Workflow

1. Resolve the canonical upstream repository, exact revision, artifact, author, and license.
2. Confirm the license permits the intended copying, modification, redistribution, and commercial or internal use. Missing or proprietary permission blocks public import.
3. Inventory the exact files proposed for import and their dependencies, scripts, assets, hooks, and network behavior.
4. Run or obtain a security review appropriate to the package's influence and execution surface.
5. Choose one capability disposition used throughout the catalog:
   - `covered`: an accepted public capability already satisfies the need
   - `partial`: existing public coverage leaves a named gap
   - `public_candidate`: the capability is reusable and can be independently supported
   - `private_overlay`: correct use depends on private context or authority
   - `rejected`: the capability is unsafe, unsupported, obsolete, duplicative, or not permitted
6. For a `public_candidate`, choose an implementation method: `original`, `clean-room`, `adapted`, `vendored`, or `reference-only`. Missing or proprietary permission permits only clean-room capability analysis, a private overlay, or rejection; it does not permit copying.
7. Record provenance before materializing the import using the exact schema field names, including `pinned_revision`, `reviewed_on`, and `reviewed_material`.
8. Apply the smallest authorized change. Preserve upstream notices and avoid unrelated updates.
9. Validate the result in every supported host and record rereview triggers, update policy, and revocation path.

## Stop conditions

Stop on unclear ownership, incompatible or absent licensing, unverifiable artifact origin, unexplained binary content, unsafe activation, or a review scope that cannot cover the proposed package. Do not treat a public GitHub repository as permission by itself.
