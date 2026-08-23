---
name: source-grounded-research
description: Research a question using current primary sources, preserving publisher URLs, dates, units, provenance, and uncertainty. Use for web investigations, fact checks, comparisons, or recommendations where current evidence and precise attribution matter.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.7.0"
  plugin: "jovanipink-skills"
  invocation: "implicit"
  provenance: "original"
  risk_class: "network-read"
---

# Source-Grounded Research

Build conclusions from evidence that can support the exact claim being made.

## Workflow

1. Restate the research question and the decision it informs.
2. Search current sources when facts may have changed, the user asks for research, or direct attribution would help.
3. Prefer primary authorities: official documentation, original datasets, statutes, filings, research papers, provider status, or first-party announcements.
4. Use discovery pages, aggregators, and community discussion to find leads or understand reactions, not as substitutes for factual authority.
5. Capture the source URL, publisher, publication or observation date, relevant units or population, and any material limitation.
6. Compare sources on the same definition and time basis. Flag incompatible scopes instead of forcing a ranking.
7. Distinguish observed facts, source claims, inference, proposal, and unresolved questions.
8. Recheck volatile facts immediately before reporting them.

## Evidence rules

- Link the page that directly supports each material claim.
- Keep quotations short; prefer faithful paraphrase.
- Preserve original publisher URLs rather than search-result or repost links.
- State when access limitations required an alternative readback method.
- Do not manufacture precision from incomplete, stale, or differently defined data.

## Output

Lead with the conclusion, then give a concise evidence table containing `Finding`, `Status`, `Source`, `Date`, and `Limit`. End with unresolved questions or recommended verification where needed.
