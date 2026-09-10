# Quickstart

Choose the client you want to use: Codex, Claude Code, or Antigravity. You can prepare and check any of them without waiting for another client.

## 1. Get the skills

```sh
git clone https://github.com/JovaniPink/skills.git
cd skills
git status --short --branch
```

Choose a reviewed tag or full commit for the version you want to use.

## 2. Check the files

Use PyYAML 6.0.3 from a trusted Python environment. See [Testing](testing.md) for the full setup.

```sh
python3 scripts/check_workflows.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Passing checks mean the source and packages agree. You still need to check that your client loads them.

## 3. Choose a pack

Start with the skills your task needs. A pack is a group of skills you install together.

- `jovanipink-skills`: check claims, research, and find causes of problems.
- `jovanipink-engineering`: plan, write, test, and review code.
- `jovanipink-reasoning`: explain code, improve writing, and hand off work.

The engineering pack was held after a live motion-review failure. Both command lines ran the ten original cases on 2026-09-10 and cleared it, so the pack is enabled there. Other app modes remain unchecked; read the [current candidate checks](client-candidate-v0.14.0.md) before you rely on one.

The [selection guide](choose-your-skills.md) lists the other packs.

## 4. Follow your client's setup guide

| Client | Guide | Current package |
| --- | --- | --- |
| Codex | [Setup and checks](clients/codex.md) | Native plugins |
| Claude Code | [Setup and checks](clients/claude.md) | Native plugins; separate account ZIPs |
| Antigravity | [Setup and checks](clients/antigravity.md) | Offline preview; loading check still needed |

First list existing skills and look for old copies. Then review the package before installing it. Use a fresh task for the check.

Gemini CLI is a separate, conditional enterprise check. It is not the Antigravity CLI. See [Google clients and tools](google-agent-surfaces.md).

## 5. Try a small task

```text
Check this task summary against its evidence. State the supported result first. Keep failed checks, unknowns, and unfinished work visible. Make no changes.
```

Confirm which skill the client used. Open one of its linked notes. Ask a status question, then resume the task and check that the original goal is still clear.

Use the [client checklist](client-support.md) to record the version, files, result, and anything you could not check. Test the CLI and app separately.
