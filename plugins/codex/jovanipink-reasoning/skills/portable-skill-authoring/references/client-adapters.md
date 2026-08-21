# Client adapters

Consult current official client documentation before changing these mappings.

## Canonical boundary

The canonical `SKILL.md` follows the open Agent Skills format and keeps client-native invocation controls out of its frontmatter. Portable metadata stays string-valued.

## Codex projection

- Keep `agents/openai.yaml` with interface metadata.
- Explicit-only skills set `policy.allow_implicit_invocation: false`.
- Generated default prompts use the plugin namespace when distributed through a plugin.

## Claude projection

- Omit the Codex `agents/` directory.
- Explicit-only skills add `disable-model-invocation: true` only in generated Claude frontmatter.
- A Claude.ai ZIP contains one top-level skill directory with its `SKILL.md` and focused references.

Compatible file layout is not behavioral parity. Record discovery, activation, reference loading, and lifecycle observations separately for every tested surface and exact client version.
