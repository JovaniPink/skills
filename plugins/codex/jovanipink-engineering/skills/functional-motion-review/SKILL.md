---
name: functional-motion-review
description: Review whether interface motion clarifies evidence, sequence, comparison, or reader actions. Use for animated editorial and data experiences; not for routine styling, implementing animation, or claiming engagement from visual polish.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.9.0"
  plugin: "jovanipink-engineering"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---

# Functional Motion Review

Assess a named reader task, not how animated a page looks. Review only; this skill does not authorize code changes, installs, analytics, user recruitment, publication, or deployment.

## Review

1. Identify the reader's question and the intended benefit. Distinguish the proposed benefit from observed comprehension findings.
2. Trace each displayed object to its authority, version, timestamp, and evidence kind. Domain state must commit independently of animation completion. Keep live observations, examples, simulations, predictions, and retrospectives visibly distinct.
3. Name the relationship the motion expresses. Chronology, correlation, modeled causality, reported causality, revision, and provenance are different; a connector cannot establish causation.
4. Assign a local role and intensity. Roles are orientation, feedback, continuity, sequence, comparison, causality, provenance, uncertainty, and progress. M0 is static; M1 is bounded feedback; M2 is controlled explanatory transition; M3 is sustained or orchestrated presentation. These are review vocabulary, not adoption targets. Ordinary reading can remain M0.
5. Inspect complete initial content, document order, native links and disclosures, keyboard operation, focus, non-color labels, reduced motion, and interruption behavior. Unknown motion preference starts static. Returning from a hidden page does not justify resuming playback. Replays identify cadence separately from domain time.
6. Compare exact baseline and candidate builds, dependencies, bundle sizes, layout shifts, long tasks, and repeatable lab runs under the same device settings. Do not treat a Lighthouse navigation result as interaction latency or field Core Web Vitals evidence.
7. Examine consented, counterbalanced task findings when available: errors, completion times, and confusion. Preference and dwell time do not establish comprehension. Keep absent participant evidence explicitly absent; do not propose production instrumentation to fill the gap.

## Route detailed reviews

- Use `accessibility-review` for criterion-level findings and the assistive-technology matrix.
- Use `performance-scalability-diagnosis` for measured performance regressions.
- Use `api-contract-compatibility-review` when a presentation change touches producer or consumer contracts.
- Use `authority-boundary-review` if the evidence authority itself is unresolved.

If a companion is unavailable, report that limit and use its primary authority without inventing a completed review. Do not duplicate their full procedures here.

## Stop and report

Reject fake live activity, hidden essential content, unlabelled synthetic outcomes, playback that cannot be interrupted, and analytics scope expansion. Do not repair a domain contract to accommodate choreography. Keep each project's taxonomy, runtime, and visual identity local; reuse a recipe only after multiple pilots demonstrate the same behavior. Missing evidence is not an engagement improvement or an accessibility conformance claim.

## Output

Return Reader task, Intended benefit, Evidence and domain authority, Motion role and intensity, Static and keyboard behavior, Reduced motion and interruption, Bundle and performance evidence, Comprehension findings, Risks, and Missing evidence. Label each conclusion as repository inspection, browser observation, automated test, participant finding, or recommendation, with date and exact reviewed revision.

Primary accessibility authority: [WCAG 2.2](https://www.w3.org/TR/WCAG22/). Evaluate the stated AA target and distinguish voluntarily applied AAA interaction-animation guidance.
