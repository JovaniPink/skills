# Migrate to Measured Skills 0.17.0

Measured Skills is maintained by Measured Studios. The homepage is https://measuredstudios.com/skills. The GitHub source remains https://github.com/JovaniPink/skills until an organization transfer is approved.

## Identity mapping

| Previous identity | New identity |
| --- | --- |
| jovanipink-skills marketplace and core pack | measured-skills marketplace and core pack |
| jovanipink-engineering | measured-engineering-build, measured-engineering-review, measured-engineering-delivery |
| jovanipink-stack-profiles | measured-stack-profiles |
| jovanipink-operations | measured-operations |
| jovanipink-reasoning | measured-reasoning |
| jovanipink-ai-systems | measured-ai-systems |
| jovanipink-agent-platforms | measured-agent-platforms |

This is a breaking pre-1.0 identity change. Skill names remain stable; plugin-qualified invocations change. There are no installed compatibility aliases. Historical attribution, source URLs, observations, and retained 0.16.0 artifacts are not rewritten as current evidence.

## Upgrade and rollback

1. Record exact installed versions, enabled packs, client versions, and current configuration. Preserve a recoverable local configuration backup without publishing it.
2. Prepare 0.17.0 in an isolated client configuration or pilot workspace. Disable old catalog plugins there before enabling new ones; never discover both identities for the same skill.
3. Install only the chosen pack through the tested client's native plugin flow. Check its inventory and generated file hashes in a fresh session. Recheck explicit-only behavior before enabling delivery workflows.
4. Promote only after the pilot criteria pass. Until then the normal configuration remains unchanged.
5. To roll back, disable new identities, restore the previous configuration and the immutable 0.16.0 distribution, then verify one copy of each intended skill in a fresh session. Do not rebuild an old release from new source or relabel new bytes 0.16.0.

## Focused build selection

Enable `measured-engineering-build` and stage only `cross-stack-quality-gates` plus the primary language profile. They are available tools, not seven mandatory ceremonies.

```sh
python3 scripts/export_selected.py --client codex --output dist/build-extras-codex --skill cross-stack-quality-gates --skill typescript-javascript-engineering-profile
python3 scripts/export_selected.py --client claude --output dist/build-extras-claude --skill cross-stack-quality-gates --skill typescript-javascript-engineering-profile
```

Use a new staging directory for each export. Review its manifest before a separate, authorized installation. The tool refuses explicit-only skills; supported plugin controls remain their route. It changes no client configuration.

## Discovery size is an estimate

The catalog reports description counts and native-layout estimates including skill names and relative paths. These are not captured client prompts. Codex's documented budget is model-dependent, with an 8,000-character fallback when context size is unavailable. Absolute installed paths, other plugins, client formatting, and model context affect the actual list. Do not infer omissions or behavior from counts alone.
