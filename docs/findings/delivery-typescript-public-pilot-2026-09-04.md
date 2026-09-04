# Delivery TypeScript public pilot finding

## Scope

One public, synthetic TypeScript boundary-defect case compared normal Codex with no Jovani treatment against the exact seven-skill `delivery-typescript-experimental` profile. Each variant ran three times from the same pinned fixture revision in fresh detached worktrees and isolated Codex homes.

Observed envelope: Codex CLI 0.153.0, `gpt-5.6-sol`, high reasoning, workspace-write sandbox, on-request approvals, disabled model-issued network and web search, disabled local memory, and identical root-to-working-directory repository instructions. The treatment used exact v0.9.0 skill bytes.

## Observed result

- All three baseline and all three focused runs fixed the defect with the same one-line implementation change and passed the four fixture tests.
- Deterministic task success and evidence quality tied. No serious boundary violation was observed.
- Median latency was 59.254 seconds for baseline and 70.376 seconds for focused.
- Median total tokens exposed by the client were 150,663 for baseline and 152,552 for focused.
- Both variants sometimes expanded into repository-level validation unrelated to the small fixture. The focused profile did not produce a case-level quality improvement that justified its observed overhead.

The deterministic case disposition is `neutral`. Repetitions measure stability and still represent one independent case. Blinded human review and the other preregistered cases remain incomplete, so this is partial evidence rather than a pilot-wide conclusion.

## Decision

Keep `delivery-typescript-experimental` experimental and non-default. Do not change its membership or infer that any individual skill lacks value from this one combined-profile case. A narrower treatment may be evaluated later, but it is not promoted by this result.

## Public boundary

This finding contains only a deliberately public synthetic case and generalized aggregate observations. It includes no private product case ID, prompt, repository name, raw trace, catalog detail, or product-specific failure pattern.
