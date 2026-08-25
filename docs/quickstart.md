# Five-Minute Quickstart

This quickstart installs one focused plugin from a reviewed local clone. It does not publish a marketplace, change a workspace account, or prove behavior on another client.

## Minute 1: Review and clone

```sh
git clone https://github.com/JovaniPink/skills.git
cd skills
git status --short --branch
```

For sensitive work, check out a reviewed tag or full commit rather than a mutable branch.

## Minute 2: Validate the clone

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

These commands verify the repository structure and generated artifacts. They do not prove installation or activation in a client.

## Minute 3: Choose one plugin

Read [Choose Your Skills](choose-your-skills.md). A useful starting point is:

- `jovanipink-skills` for research, verification, diagnosis, and public-boundary review;
- `jovanipink-engineering` for a broad engineering lifecycle;
- `jovanipink-operations` for requirements, decisions, measurement, and incidents.
- `jovanipink-agent-platforms` for human-facing Google ADK, agent architecture, tool, security, protocol, and retrieval reviews.

Avoid installing all plugins by default.

## Minute 4: Install in one client

Codex CLI or the local ChatGPT desktop development path:

```sh
codex plugin marketplace add /absolute/path/to/skills
codex plugin add jovanipink-skills@jovanipink-skills
codex plugin list --json
```

Claude Code or Claude Desktop local Code sessions:

```sh
claude plugin marketplace add /absolute/path/to/skills --scope user
claude plugin install jovanipink-skills@jovanipink-skills --scope user
claude plugin list --json
```

Gemini CLI uses its own Agent Skills scopes and `/skills` commands. Follow the current [Gemini CLI Agent Skills documentation](https://geminicli.com/docs/cli/skills/) and record that surface separately.

Start a fresh session after installation.

## Minute 5: Run a read-only check

Try a prompt that does not change external state:

```text
Verify whether this branch is committed, pushed, reviewed, merged, deployed, and live. Report only the states supported by current evidence. Do not change anything.
```

Confirm whether the client discovered and activated `claim-verification`. Record the exact client version, plugin version, source commit, prompt, result, timestamp, and evidence reference. Do not treat a result on one surface as proof for another.

## Explicit-only reminder

Explicit-only skills require direct selection. Direct selection chooses a workflow; it does not authorize every action inside that workflow.

Codex example:

```text
$jovanipink-skills:publish-change-safely Prepare the publication checks, but do not push or open a pull request.
```

Claude Code example:

```text
/jovanipink-skills:publish-change-safely Prepare the publication checks, but do not push or open a pull request.
```

## Next reading

- [How to Use JovaniPink Skills](README.md)
- [Skill Cheatsheet](skill-cheatsheet.md)
- [Taxonomy](taxonomy.md)
- [Security Model](security-model.md)
- [Manual Smoke Tests](manual-smoke-tests.md)
