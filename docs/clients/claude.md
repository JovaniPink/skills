# Claude setup

Claude Code gets the same source skills and release checks as Codex. Its install and use tests run on their own schedule.

## Check what is there

```sh
claude --version
claude plugin list --json
```

Check personal skills, project skills, and plugins for copies with the same name. Keep a list of old copies before changing anything. In the app, also check **Customize > Skills > Yours**. A personal upload and a plugin can both appear there.

## Install one reviewed pack

Replace the example path with your local checkout. These commands change your install:

```sh
claude plugin marketplace add /absolute/path/to/skills --scope user
claude plugin install jovanipink-skills@jovanipink-skills --scope user
claude plugin list --json
```

For an existing install, refresh the marketplace before updating the plugin. Use `claude plugin marketplace update --help` and `claude plugin update --help` to check the current command form. Save the old version and file hashes first.

Start a fresh task, then select the full plugin command:

```text
/jovanipink-skills:claim-verification Check which completion claims have evidence. Make no changes.
```

Generated Claude packages omit Codex's `agents/` files. Skills that require direct selection get `disable-model-invocation: true`. Check both direct selection and a related prompt that should leave the skill inactive.

## Check each app mode

Claude desktop Code mode, Claude.ai, and Cowork each need their own record. Note whether the task runs locally or remotely. Check loading, linked files, result files, and resume behavior in each mode you use.

For an account upload, build the separate one-skill ZIP with `python3 scripts/package_claude_ai.py`. Review it before uploading. Do not upload an explicit-only skill until the receiving mode has a verified control that prevents automatic selection.

Personal preferences belong in the user's `CLAUDE.md` for local Code use. Repository guidance uses the checked-in `CLAUDE.md`. Confirm which files loaded; do not assume a local file syncs to a cloud task.

Follow the [shared client checks](../client-support.md). Remove duplicate copies only after reviewing their source and saving what is needed to restore them.

Sources: [Claude skills](https://code.claude.com/docs/en/skills), [plugin management](https://code.claude.com/docs/en/discover-plugins), [Claude memory](https://code.claude.com/docs/en/memory).
