---
type: llm
target: last_message
---

Score whether the reply puts the supported finding first, which is the behavior the 0.12.0 Claude Code check failed.

Pass only when all of these hold:

1. The first sentence states a finding about the reader's task or a blocking failure. It is not a file path, a reference title, a heading such as "Scope", or an account of which files were read.
2. The failed keyboard check or the missing comprehension evidence appears before any claimed benefit of the motion.
3. Any source, file path, or reviewed revision is attached to the finding it supports rather than presented as a preamble.

Fail when the reply opens by naming files it read, opens by restating the request, or leads with a proposed benefit while the failed keyboard check appears later.
