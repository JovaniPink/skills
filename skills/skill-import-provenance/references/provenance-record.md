# Provenance record

Record one entry for every imported, adapted, or externally inspired skill.

```json
{
  "skill": "skill-name",
  "disposition": "public_candidate",
  "implementation_method": "original | clean-room | adapted | vendored | reference-only",
  "source_url": "https://example.com/canonical-source",
  "pinned_revision": "immutable revision or explained retrieval receipt",
  "upstream_license": "SPDX identifier or exact status",
  "reviewed_on": "YYYY-MM-DD",
  "reviewed_material": ["paths or artifact identifiers"],
  "local_changes": "material differences",
  "security_review": "report path, URL, or not-applicable with reason",
  "rereview_triggers": ["paths, dependency changes, or release conditions"],
  "revocation": "how to disable, remove, or replace the skill"
}
```

Use the same five disposition values as the capability inventory: `covered`, `partial`, `public_candidate`, `private_overlay`, and `rejected`. Use `not-applicable` only where the schema permits it and with a reason. Use an immutable commit or digest when an upstream artifact may change. Keep licensing evidence and required notices with the imported material.
