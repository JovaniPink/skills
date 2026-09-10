# Finding Vocabulary

Use this vocabulary when a skill reports findings. It gives every review the same severity words and the same way to say whether a change introduced a problem.

## Why this exists

The catalog has 26 review skills. Overlap is deliberate: every skill declares `composes_with`, 19 declare `conflicts_with`, and 11 route to a named sibling in their own instructions. A motion review can hand work to accessibility, performance, and authority reviews in one pass.

Four skills currently name a severity, and they use three different words for it: `severity` without a scale, `blocking`, and `major`. Nothing defines any of them. So `code-change-review` asks for findings "ordered by severity" against a scale that does not exist, and two skills reviewing the same code produce findings a reader cannot rank against each other.

That is an evidence problem, not a formatting problem. A duplicate finding counted twice overstates how much is wrong.

## Severity

Use these four words, ordered from least to most severe. They come from the Static Analysis Results Interchange Format (SARIF), an OASIS standard for exchanging analysis results between tools.

| Level | Use it when |
| --- | --- |
| `none` | The finding carries no judgment. It records something the reader asked about. |
| `note` | The reader may want to act, and nothing breaks if they do not. |
| `warning` | Something is wrong and the reader should decide. It does not block on its own. |
| `error` | Something is wrong enough to stop the reviewed action until it is resolved. |

Two rules keep the scale honest:

- Severity describes the finding, not the reviewer's confidence. Say what the evidence supports separately.
- A skill may not invent a fifth level. If a finding does not fit, say why in the finding itself.

## Finding state

State whether the reviewed change caused the problem. These four words also come from SARIF, where they describe a result against a baseline.

| State | Meaning in a review |
| --- | --- |
| `new` | The reviewed change introduced this. |
| `unchanged` | The problem predates the change and the change did not touch it. |
| `updated` | The problem predates the change, and the change altered the affected code. |
| `absent` | The baseline had this and the change removed it. |

Every finding needs a state. Reporting an existing problem as if the change caused it is the error this prevents, and it is the same class of mistake as reporting a proposal as a ratified decision.

A changed line is not automatically the cause. An unchanged line can still be affected. Decide the state from what the evidence shows, not from whether the line appears in the diff.

## Ownership

One root cause is one finding, owned by one skill.

When two skills would report the same cause, the skill that owns the underlying rule reports it. Another skill may name the effect it observed and point to the owner. Do not report the same cause once per skill, and do not report it once per location: list the locations inside the single finding.

## Volume

Rank findings by reader impact and report the most severe first. When a review would return more findings than a reader can act on, report the top ones and state how many were left out and where. A silent cut is a false clean result.

## What this does not adopt

SARIF is a JSON exchange format for analysis tools. This catalog produces prose reviews written by agents for people to read. Only the vocabulary and the distinctions transfer.

Skills do not emit SARIF documents, do not compute fingerprints, and do not carry rule identifiers or numeric ranks. A skill that later needs machine-readable output should treat that as its own decision with its own review.

## Known gap

No skill aggregates findings across skills. `cross-stack-quality-gates` consolidates gate results, which are command outcomes, not findings. Nothing deduplicates overlapping findings, applies single ownership across a multi-skill review, or produces one ranked list from several reviews.

This vocabulary is the part that has to exist first, because findings cannot be merged or ranked until they are comparable. Whether the catalog gains an aggregating skill is a separate decision.

## Sources

Severity and finding-state vocabulary follow [SARIF Version 2.1.0 Plus Errata 01](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html), 28 August 2023, read 2026-09-10. Its `level` property defines the four severity values as ordered from least to most severe. Its `baselineState` property defines the four finding states against a baseline run.
