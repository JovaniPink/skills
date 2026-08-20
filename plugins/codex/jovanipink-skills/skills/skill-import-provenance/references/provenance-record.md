# Provenance record

Record one entry for every imported, adapted, or externally inspired skill.

```json
{
  "skill": "skill-name",
  "disposition": "original | vendor | adapt | clean-room | reference | reject",
  "source_url": "https://example.com/canonical-source",
  "revision": "immutable revision or not-applicable",
  "upstream_license": "SPDX identifier or exact status",
  "reviewed_on": "YYYY-MM-DD",
  "reviewed_files": ["paths or artifact identifiers"],
  "local_changes": "material differences",
  "security_review": "report path, URL, or not-applicable with reason",
  "rereview_triggers": ["paths, dependency changes, or release conditions"],
  "revocation": "how to disable, remove, or replace the skill"
}
```

Use `not-applicable` only with a reason. Use an immutable commit or digest when an upstream artifact may change. Keep licensing evidence and required notices with the imported material.
