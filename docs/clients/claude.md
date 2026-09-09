# Claude setup

Claude Code gets the same source skills and release checks as Codex. Its install and use tests run on their own schedule.

A **Code plugin** is a package installed for Claude Code. An **account upload** is a skill added through Customize in Claude. Check both stores. A successful Code update does not prove that Chat has the same files.

See the [September account repair check](../claude-account-repair-2026-09-08.md) for dated results and remaining app checks.

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

For an existing install, refresh the marketplace before updating the plugin. Use `claude plugin marketplace update --help` and `claude plugin update --help` to check the current command form. Save the old version and file hashes first. Check every installed file after the update. In the observed 2.1.220 update, all seven packs moved to 0.11.0 and their files matched the generated source. The desktop plugin pages also showed the new version; that did not establish behavior in an existing task.

Start a fresh task, then select the full plugin command:

```text
/jovanipink-skills:claim-verification Check which completion claims have evidence. Make no changes.
```

Generated Claude packages omit Codex's `agents/` files. Skills that require direct selection get `disable-model-invocation: true`. Check both direct selection and a related prompt that should leave the skill inactive.

## Check each app mode

Claude desktop Code mode, Claude.ai, and Cowork each need their own record. Note whether the task runs locally or remotely. Check loading, linked files, result files, and resume behavior in each mode you use.

For an account upload, build the separate one-skill ZIP with `python3 scripts/package_claude_ai.py`. Review it before uploading. The command prepares all 77 skills; it does not approve every ZIP for every app. Keep a separate upload checklist. The current staged target is 63 skills that allow automatic selection, with 14 explicit-only workflows held. Do not upload an explicit-only skill until the receiving mode has a verified control that prevents automatic selection. A metadata field or working slash command alone does not prove that control.

To update an existing account skill, open its menu and choose **Download** to save the old copy. Then choose **Replace**, select the reviewed ZIP, and save. Check the scan result, version, file count, and linked files. In the observed web check, claim-verification changed from one file to two files and showed version 0.11.0. A fresh Chat task visibly read both files. This does not prove Cowork or desktop task behavior.

Check that each download exists and opens before replacing or disabling its entry. Older uploads may download as `.skill` archives; newer entries may download as one-skill plugin ZIPs. Compare the skill files inside them. Neither the archive name nor a mount path alone proves the install source. Use Replace rather than creating another entry with the same name.

Refresh the web and desktop libraries after an account change. Check both lists before uploading another copy. Use fresh tasks to check the files actually loaded; an old task can retain old instructions. Save file hashes and tool output, then test linked files, result downloads, failed checks, unfinished work, and resumption. Record **prepared**, **installed**, **enabled**, **loaded**, and **behavior-tested** separately.

Personal preferences belong in the user's `CLAUDE.md` for local Code use. Repository guidance uses the checked-in `CLAUDE.md`. Confirm which files loaded; do not assume a local file syncs to a cloud task.

If a live check reports expired sign-in, leave it blocked until sign-in is refreshed. Read the process exit code and error text as well as its final event. In one observed authentication failure, the CLI emitted a `success` subtype with `is_error: true` while exiting with code 1. That is not a passing check.

Follow the [shared client checks](../client-support.md). Remove duplicate copies only after reviewing their source and saving what is needed to restore them.

Sources: [Claude skills](https://code.claude.com/docs/en/skills), [plugin management](https://code.claude.com/docs/en/discover-plugins), [Claude memory](https://code.claude.com/docs/en/memory).
