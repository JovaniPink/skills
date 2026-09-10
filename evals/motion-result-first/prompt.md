---
name: motion-result-first
tags:
  - functional-motion-review
  - output-order
plugins:
  - jovanipink-engineering
runs: 3
max_turns: 6
timeout_seconds: 300
allowed_tools:
  - Read
  - Glob
  - Grep
---

Review whether the motion in this animated release-timeline widget helps a reader answer "which build introduced the regression".

Use only the facts below. Do not ask for more input, and do not change any code.

- The widget animates a horizontal timeline of seven builds over about 900 milliseconds on load, then replays whenever the tab regains focus.
- Build rows come from a checked-in fixture file with fixed timestamps. The fixture is labeled "sample data" in the page source but the label is not rendered.
- Keyboard check: the timeline scrubber is reachable by Tab but cannot be operated by arrow keys. The check failed.
- Reduced motion: no `prefers-reduced-motion` branch exists.
- Bundle: the animation library adds 34 KB gzipped. Baseline and candidate Lighthouse navigation scores are both 96.
- Comprehension: no participant study has been run. No task-completion or error data exists.

Report your review.
