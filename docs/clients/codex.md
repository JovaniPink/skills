# Codex setup

Use the generated Codex plugin for terminal or desktop code work. Check ChatGPT Work and web separately. They may have different loading and file access.

## Check what is there

```sh
codex --version
codex plugin list --json
```

Save both the list and any warnings. If the remote list fails, the local list may still be useful, but it is incomplete.

Look for old copies in personal or project skill folders as well as the plugin cache. Compare the installed files with `plugins/codex/` from the reviewed checkout. Do not assume that a matching version means matching files.

## Install one reviewed pack

Replace the example path with your local checkout. These commands change your install:

```sh
codex plugin marketplace add /absolute/path/to/skills
codex plugin add jovanipink-skills@jovanipink-skills
codex plugin list --json
```

Open a fresh task after the install. Select a skill by its full plugin name:

```text
$jovanipink-skills:claim-verification Check which completion claims have evidence. Make no changes.
```

For skills that require direct selection, the generated `agents/openai.yaml` sets `allow_implicit_invocation: false`. Test that behavior before relying on it.

## Check the apps

In Codex desktop, inspect the plugin page and open a fresh test task. Verify the selected skill, a linked reference, a result file, and interruption recovery. If an active task still uses older files, record that task separately.

In ChatGPT Work or web, inspect that surface's own library. Do not treat the CLI list as its install record.

Review personal preferences in Codex user instructions separately from the package. Keep repository rules in `AGENTS.md`.

Follow the [shared client checks](../client-support.md) for updates, removal, and evidence. Check native `--help` before an update or uninstall; command forms can change.

Sources: [OpenAI skill guide](https://learn.chatgpt.com/docs/build-skills), [OpenAI plugin guide](https://developers.openai.com/plugins/build/plugins).
