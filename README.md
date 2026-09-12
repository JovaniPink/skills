# JovaniPink Skills

This repository holds 79 Agent Skills for AI coding assistants.

A skill is a short set of written instructions for one kind of task. Reviewing a code change is one kind of task. Checking whether a claim has evidence is another. Your assistant reads the matching skill and follows its steps.

A skill is only text. It installs no programs and grants no new permissions. It changes how your assistant works through a task, not what it is allowed to do.

[Getting started article](https://jovanipink.com/posts/getting-started-with-jovanipink-skills): try one skill with a small evidence exercise.

## Install one pack

A pack is a group of related skills you install together. There are seven. Start with one.

For Claude Code:

```sh
claude plugin marketplace add JovaniPink/skills --scope user
claude plugin install jovanipink-skills@jovanipink-skills --scope user
claude plugin list --json
```

For Codex:

```sh
codex plugin marketplace add JovaniPink/skills
codex plugin add jovanipink-skills@jovanipink-skills
codex plugin list --json
```

The install name has the form `plugin@marketplace`. A marketplace is a place your client looks for packs. This repository is the marketplace, and it is named `jovanipink-skills`. One pack carries that same name. So `jovanipink-skills@jovanipink-skills` is correct, not a repeated word. Every other pack reads like `jovanipink-engineering@jovanipink-skills`.

Antigravity uses an offline preview instead. See [Antigravity setup](docs/clients/antigravity.md).

Now start a fresh task and name a skill:

```text
/jovanipink-skills:claim-verification Check which completion claims have evidence. Make no changes.
```

Codex uses `$` in place of `/`.

For work where the risk is high, clone the repository first. Read the source, check out a reviewed revision, then add your local folder as the marketplace. The [five-minute quickstart](docs/quickstart.md) walks through that path.

## What these skills do for you

Each skill slows the assistant down where answers usually go wrong. It has to name its evidence. It has to keep failed checks and unknowns visible. It has to stop at any action you did not approve.

A few examples:

- `claim-verification` tests whether done, fixed, merged, or deployed is backed by evidence.
- `systematic-diagnosis` finds a cause instead of quietly changing your code.
- `code-change-review` reviews one exact diff and grades each finding.
- `source-grounded-research` keeps sources, dates, and uncertainty attached to the answer.

These are authored instructions, not measured benefits. We wrote the skills to produce those habits. We have not run a study that shows they improve your results.

## The seven packs

Install the smallest pack that covers your work.

| Pack | Use it for |
| --- | --- |
| `jovanipink-skills` | Verify claims, research, diagnose problems, review what is safe to publish |
| `jovanipink-engineering` | Frame, plan, test, and review code changes |
| `jovanipink-reasoning` | Explain code, improve writing, hand off work |
| `jovanipink-operations` | Requirements, decisions, measurement, adoption, incidents |
| `jovanipink-stack-profiles` | Language and platform guidance, such as Python, Go, and Terraform |
| `jovanipink-ai-systems` | Evaluate AI behavior, context reliability, and source-to-output checks |
| `jovanipink-agent-platforms` | Review agent architecture, tools, protocols, and retrieval |

The [skill cheatsheet](docs/skill-cheatsheet.md) lists all 79 skills with one line each. [Choose Your Skills](docs/choose-your-skills.md) helps you pick. The [skill catalog reader guide](docs/skill-catalog-reader-guide.md) explains every skill in full.

## How a skill gets picked

Every skill is marked implicit or explicit-only.

Implicit means your client may pick the skill on its own when your request matches it. You can still name it directly. 65 skills are implicit.

Explicit-only means the skill stays off until you name it. Naming it does not authorize a push, merge, deletion, release, or deployment. You still approve those yourself. 14 skills are explicit-only.

The cheatsheet shows the marking for each skill. The [glossary](docs/glossary.md) defines the other terms used here.

## What each client can do today

Codex, Claude Code, and Antigravity get equal attention here. Equal attention does not mean every feature works everywhere yet.

| Client | What we ship | Setup guide |
| --- | --- | --- |
| Codex CLI and ChatGPT desktop | Native packs with all 79 skills | [Codex setup](docs/clients/codex.md) |
| Claude Code | Native packs with all 79 skills, plus separate ZIP files for account uploads | [Claude setup](docs/clients/claude.md) |
| Antigravity | An offline preview of the implicit skills; explicit-only skills are left out | [Antigravity setup](docs/clients/antigravity.md) |

Claude Code packs and Claude account uploads are two separate installs. Updating your Code packs does not update the skill library that Chat uses. Check both.

For Claude.ai, build one-skill ZIP files from a local clone with `python3 scripts/package_claude_ai.py`. Upload them one at a time from `dist/claude-ai/`.

The 14 explicit-only skills are on hold for Claude.ai uploads. A hold means the files are ready, but we decided not to ship them yet, because a check we named has not passed. The missing check here is a control that stops Claude.ai from picking the skill on its own. A metadata field does not prove that control. Neither does a working slash command.

Client behavior changes on its own schedule. The [client support checklist](docs/client-support.md) lists what to test in each app and CLI. A result in one app does not carry to another.

## Evidence and status

This project keeps two words apart.

Authored means we wrote it. It says what the instructions intend.

Observed means we ran it and wrote down what happened, with the exact client, version, and date.

The current catalog is version 0.16.0. It has 79 skills in seven packs. The [current candidate record](docs/client-candidate-v0.16.0.md) holds the install and behavior results for it.

The `jovanipink-engineering` pack was held after one of its skills failed a live safety test. Both command lines ran the ten original test cases on 2026-09-10 and cleared it. The pack is enabled there. Other app modes are still unchecked. Read the candidate record before you enable it somewhere else.

One limit is worth knowing before you test. Every result we have recorded was taken at the first turn of a fresh session. We have not measured whether a skill still shapes replies later in a long working session, and published research suggests instructions lose force as a conversation grows. The [study design](docs/turn-depth-study.md) says how we plan to find out.

We do not claim that these skills improve your results. That claim would need a separate study with complete runs and human review. That study has not been run.

## Safety

The catalog ships instructions and reference notes. It ships no skill-level programs, hooks, MCP servers, bundled agents, or broad tool grants. Nothing installs or runs on its own.

This matters because a skill you install can shape every later task. Keeping it to text means you can read the whole thing before you trust it. It also means your client's own permission rules stay in charge.

A skill can recommend an action. Your permissions, your tests, and your approval decide whether it happens.

Read the [security policy](SECURITY.md) and the [security model](docs/security-model.md) before you use the catalog for sensitive work.

## License and origin

This is an independent work under the [MIT license](LICENSE). It does not copy or redistribute anyone else's skill text. The skills are written from the author's own practice and from primary sources, such as standards and official platform documentation.

Private product facts stay out of this catalog. [Private overlays](docs/private-overlays.md) explains how they are kept apart.

The source format is the open [Agent Skills format](https://agentskills.io/specification).

## Contribute or build it yourself

Skills are authored in `skills/`. The `plugins/` folders are generated, so do not edit them by hand.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before you open a pull request. [Repository architecture](docs/architecture.md) describes the folder layout. [Testing](docs/testing.md) lists the exact build and check commands, plus the tool versions they need. The [editorial style guide](docs/editorial-style.md) covers the writing rules.

## Where to go next

- [Five-minute quickstart](docs/quickstart.md): install and test one skill
- [Glossary](docs/glossary.md): what the terms mean
- [Skill cheatsheet](docs/skill-cheatsheet.md): all 79 skills at a glance
- [Client support checklist](docs/client-support.md): what to test in each app and CLI
- [How to use JovaniPink Skills](docs/README.md): the full guide
