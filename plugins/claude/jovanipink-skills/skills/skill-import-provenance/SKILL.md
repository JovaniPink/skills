---
name: skill-import-provenance
description: Import or adapt an agent skill only after verifying license, source, revision, authorship, security review, local changes, and rereview or revocation policy. Use only when the user explicitly asks to add, vendor, mirror, or adapt a skill from another source.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.1.0"
  jovanipink.invocation: "explicit"
  jovanipink.provenance: "clean-room"
disable-model-invocation: true
---

# Skill Import Provenance

Do not copy first and investigate later. Read [provenance record](references/provenance-record.md) before proposing an import.

## Workflow

1. Resolve the canonical upstream repository, exact revision, artifact, author, and license.
2. Confirm the license permits the intended copying, modification, redistribution, and commercial or internal use. Missing or proprietary permission blocks public import.
3. Inventory the exact files proposed for import and their dependencies, scripts, assets, hooks, and network behavior.
4. Run or obtain a security review appropriate to the package's influence and execution surface.
5. Choose one disposition:
   - `vendor`: preserve source with license and notices
   - `adapt`: record upstream and material changes under a compatible license
   - `clean-room`: use only public behavior or capability requirements and independently author
   - `reference`: link without copying
   - `reject`: do not import
6. Record provenance before materializing the import.
7. Apply the smallest authorized change. Preserve upstream notices and avoid unrelated updates.
8. Validate the result in every supported host and record rereview triggers, update policy, and revocation path.

## Stop conditions

Stop on unclear ownership, incompatible or absent licensing, unverifiable artifact origin, unexplained binary content, unsafe activation, or a review scope that cannot cover the proposed package. Do not treat a public GitHub repository as permission by itself.
