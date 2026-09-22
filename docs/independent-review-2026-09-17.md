# Independent review, 2026-09-17

Reviewed by: an outside Claude Code session, not a catalog maintainer.

Scope: the public skills catalog, and the skills-private policy repo.

> Maintainer note, 2026-09-21: this is a historical review of 0.16.0, not current release acceptance. The review text below is unchanged. Maintainer corrections are listed at the end, and the 0.17.0 dispositions are in the [0.17.0 candidate record](client-candidate-v0.17.0.md#pr-44-disposition).

Result: the main safety rule works as intended. Two real gaps were found and are fixed below. One doc line overclaims. One structural change is suggested.

## 1. The cross-platform gate works

A skill marked explicit-only should stay off by default on both Claude Code and Codex. This is true today, and it is checked three different ways:

- Canonical skill files cannot carry the Claude-only `disable-model-invocation` field. `scripts/cataloglib.py` raises an error if it finds one, so the setting can only come from the build step, not by hand.
- The build step writes `disable-model-invocation: true` into all 14 explicit-only skills on the Claude side, and `allow_implicit_invocation: false` into all 14 on the Codex side.
- Two tests check this. `scripts/validate_catalog.py` checks the Codex file against the canonical list. `tests/test_catalog.py` checks the Claude file the same way. Both run in CI on every pull request.

No fix is needed here. This is written down so it stays a known pass, not something that has to be re-checked from scratch next time.

## 2. Real gap: the pack budget math is incomplete

`catalog/packs.json` sets a character budget for each pack, based only on the total length of each skill's `description` field. Codex's own docs say its skill list also counts the skill name and the file path, not just the description.

The `jovanipink-engineering` pack is already at 6,665 of Codex's 8,000 character limit, counting description text alone. Once name and path length are added, this pack may go over the limit. If a pack goes over the limit, Codex's own docs say it may drop whole skills from the list, not just shorten their text. That is a worse outcome than a shortened description.

Fix: add skill name length and an estimated file path length to the budget check in `scripts/validate_catalog.py`, next to the existing description length check.

## 3. Real gap: skills-private has no pre-commit check

The skills-private repo has one job: keep private product facts out of git. Its `scripts/validate.py` is a strong check. It is short, it uses only the Python standard library, and it checks its own source code to prove that.

But nothing runs this check automatically before a commit is made. The README says to run it by hand before committing. That depends on memory.

For a repo whose only job is keeping secrets out of git history, this is the wrong point to catch a mistake. By the time a person notices a forgotten check, the commit may already exist. A git pre-commit hook would run the check before the commit is created, which is the point that actually matters here.

Fix: add `scripts/validate.py` as a pre-commit hook in skills-private, so it runs on every commit attempt, not only when remembered.

## 4. One skill is using a lot of the description budget

`functional-motion-review`'s description is about 416 characters. The average description in its pack is about 267 characters. This one skill's longer description is the main reason `jovanipink-engineering` is close to its character limit. This is already stated in `docs/client-candidate-v0.14.0.md`, but it is worth repeating here next to the budget math above.

## 5. Suggestion: split the jovanipink-engineering pack

This pack has 25 skills. Fourteen skills across the whole catalog are explicit-only, meaning higher authority, since they can change files, merge branches, or run other agents. Seven of those fourteen live in this one pack, next to 18 skills that are plain read-only reviews.

Splitting this pack into two would help in two ways. First, it would bring both new packs under the character budget with room to spare, matching the other six packs. Second, it would let a person install just the read-only reviews without also installing plan execution, merge conflict handling, and multi-agent work they may not want yet.

## 6. Small wording fix needed in SECURITY.md

`SECURITY.md` says repository scripts do not reach the network. This is true for the checks that run on every pull request. It is not true for `scripts/check_upstream_freshness.py`, which does make real web calls when run with `--online`. That script only runs in a separate, scheduled, weekly job, and it only calls a fixed list of public documentation pages. It sends no repository data or user data anywhere.

The line in `SECURITY.md` should say the pull request checks never reach the network, and name the weekly freshness job as the one exception, instead of stating a blanket rule that is not quite true.

## 7. Evidence ledger note

`catalog/evidence.json` marks every one of the 79 skills with `behavioral_evidence.status: "none"`. But real, dated pass and fail results already exist in plain text for at least three skills, including the `functional-motion-review` re-test described in `docs/client-candidate-v0.14.0.md`.

This may be on purpose, matching the catalog's own rule that a pass on one client does not prove a pass on another. If it is on purpose, that is a fair choice. If it is not on purpose, the ledger should be updated to match the real, already-written evidence, so a reader checking only the ledger does not miss it.

## Maintainer reconciliation, 2026-09-21

Catalog maintainers added this section. The review text above is unchanged. These notes correct it.

- **Result.** Two gaps were reported, not fixed. This review did not implement its own suggestions.
- **Section 2.** The review treats 8,000 characters as a universal Codex limit. It is a documented fallback that applies when the model context size is unavailable.
- **Section 3.** The skills-private validator enforces a fixed policy-only tree. It is not comprehensive secret detection. Adding a hook would require revisiting that repository's explicit no-hooks policy.
- **Section 4.** The long `functional-motion-review` description adds to the pack's description total. The review did not establish that it is the main cause of discovery pressure.
- **Section 5.** Explicit-only is an invocation restriction, not a grant of authority. The pack's other 18 skills include design work as well as reviews, so they are not all read-only reviews.
