# Turn-Depth Study Design

Every observation this repository holds was taken at the first turn of a fresh session. Nothing has been recorded about whether a skill still shapes a reply twenty turns later.

This page is the written method for finding out. It has not been run. When it is, the results belong in a client observation matrix, not here.

## Why this matters

Published work finds that instruction adherence falls as a conversation grows.

- Li and others, "Measuring and Controlling Instruction (In)Stability in Language Model Dialogs," COLM 2024, [arXiv:2402.10962](https://arxiv.org/abs/2402.10962). The abstract reports "a significant instruction drift within eight rounds of conversations."
- Epstein and others, "MMMT-IF," [arXiv:2409.18216](https://arxiv.org/abs/2409.18216). Instruction following, checked by running code rather than by asking a model to grade, falls from 0.81 at turn 1 to 0.64 at turn 20 across three frontier models. Moving all instructions to the end of the input raised the score by 22.3 points, so the problem is finding scattered instructions, not understanding them.

Neither studies Agent Skills in Claude Code, Codex, or Antigravity. Applying them to this catalog is an extrapolation, and that is exactly why it needs its own measurement.

## What to measure

Check whether the reply still carries the skill's own named output sections.

Do not ask the client whether it remembers the skill. Kruthof, "Models Recall What They Violate," [arXiv:2604.28031](https://arxiv.org/abs/2604.28031), finds models accurately restate constraints they are breaking at the same moment. Self-report is not evidence. Section presence is.

## How to run it

1. Pick one skill with a strict output contract. `functional-motion-review` is the natural first choice, because its ten cases already have recorded turn-one results.
2. Run all ten cases the way they were run before: one fresh session each, one turn. This is the baseline.
3. Open one session and work through unrelated tasks until you reach a chosen turn index. Record the index. Then run case one.
4. Repeat for each case at the same index, in a fresh long session each time, so one case cannot prime the next.
5. Repeat at a second, deeper index.

Keep the client, client version, pack version, model, and permission mode identical across all three conditions. Only session depth changes.

## How to score it

For each case, record whether every named section the skill requires appears in the reply. Report the share of cases that kept their full contract at each turn index.

A drop is a finding. No drop is also a finding, and a more useful one, because it would show the concern does not transfer from the published benchmarks to this catalog.

## How to record it

Each result becomes one record in the matrix for its catalog version, with `session_depth` set to `continued_session` and `turn_index` set to the recorded turn. Baseline runs keep `fresh_single_turn`.

The schema accepts these fields, and the validator requires a turn index whenever the depth is a continued session, so a result cannot be filed without saying how deep it was.

## What this design cannot show

- One operator scoring their own runs. Section presence is close to mechanical, but it is not blind.
- One client. A result here would carry no claim about any other client, as always.
- Filler turns are not controlled. Task difficulty, context length, and topic all change together, so a drop shows that depth is associated with contract loss, not which part of depth caused it.
- Ten cases on one skill. That is a signal about this catalog, not a measured property of skills in general.

State these limits in any record produced from this method.
