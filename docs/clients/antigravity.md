# Antigravity setup

Antigravity setup and testing have equal priority with Codex and Claude. It has an offline preview builder now. The preview still needs a loading test in the exact app or CLI you use.

## Check what is there

```sh
agy --version
agy plugin list
```

The command is `agy`. An empty imported-plugin list does not mean the client has no skills. Built-in, global, and project skills may also load.

In the desktop app, open **Settings > Customizations** and inspect the skill list. Check the IDE separately. Keep installed, enabled, listed, and used as separate facts.

## Prepare a preview

Run this from the reviewed catalog checkout. Use a new output folder:

```sh
python3 scripts/build_antigravity.py --skill claim-verification --output dist/antigravity-check
```

The result contains `plugin/` and `bundle.json`. The latter lists selected skills, exclusions, and file hashes. Omit `--skill` to prepare all eligible skills. The builder does not install anything and refuses to overwrite an existing folder.

The preview keeps `skills/<name>/SKILL.md` and linked notes. It omits Codex's `agents/` folder. The installed CLI guide uses this folder layout, but the web CLI guide also describes flat `.md` files. A loading test must settle which layout works in the chosen version. Do not flatten files by hand or lose their links.

All explicit-only skills are excluded. We have no verified Antigravity control that prevents their automatic selection. A slash command is not enough to prove that control exists.

## Install after review

Once the selected preview and test setup are ready, the native local install command is:

```sh
agy plugin install /absolute/path/to/antigravity-check/plugin
agy plugin list
```

Record the names the client actually shows. Then follow the [shared client checks](../client-support.md) in a fresh task. Verify linked notes and removal before widening the install. Keep personal and product skills separate from this public preview.

The general skill guide lists workspace `.agents/skills/` folders and global `~/.gemini/config/skills/` folders. The CLI guide also names its own global directory. Check the receiving client before placing files in either location.

Use the app or IDE's own rules page for a reviewed personal preference. Confirm that it loaded. Do not infer CLI rule loading from an IDE result.

Sources: [Antigravity skills](https://antigravity.google/docs/skills/), [CLI plugins](https://antigravity.google/docs/cli/plugins/), [IDE rules](https://antigravity.google/docs/ide/rules/).
