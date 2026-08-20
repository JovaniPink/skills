# Architecture

## Source and adapters

`skills/` is the canonical, client-neutral source. A canonical skill has:

- standards-compatible YAML frontmatter in `SKILL.md`
- focused workflow instructions
- optional references loaded only when needed
- `agents/openai.yaml` for Codex presentation and invocation policy
- a matching provenance record and trigger matrix

`scripts/build_distributions.py` creates two tracked adapters:

```text
skills/ ──> plugins/codex/jovanipink-skills/skills/
        └─> plugins/claude/jovanipink-skills/skills/
```

The Codex copy retains `agents/openai.yaml` and rewrites its direct-invocation prompt to the installed plugin namespace. The Claude copy omits that client-specific directory and adds `disable-model-invocation: true` to explicit-only skill frontmatter. No client adapter changes the workflow body.

## Invocation classes

Implicit skills are read-only or diagnostic by default. They may activate when their descriptions clearly match the user's task. Explicit-only skills coordinate side effects or trust decisions and require the user to name the skill. Native adapters encode the distinction, while the workflow text still states its authorization boundary.

Invocation metadata is portable repository metadata, not a replacement for host enforcement:

- canonical: `metadata.jovanipink.invocation`
- Codex: `policy.allow_implicit_invocation`
- Claude: `disable-model-invocation`

Direct invocation is also client-native and namespaced after plugin installation:

- Codex plugin: `$jovanipink-skills:skill-name`
- Claude plugin: `/jovanipink-skills:skill-name`

Canonical unnamespaced forms remain useful when a client installs an individual skill rather than the plugin.

## Enforcement boundary

Skills provide judgment, sequencing, and reporting structure. Deterministic requirements belong in repository scripts, tests, CI, or client permissions. Prose cannot guarantee that an agent will obey a permission boundary, detect every secret, or run a gate correctly.

## Lifecycle

1. Author in `skills/`.
2. Review provenance, security, and invocation class.
3. Add trigger cases.
4. Generate client distributions and Claude.ai archives.
5. Run deterministic validation.
6. Record each client surface's observed behavior.
7. Release only when automated and required manual evidence is complete.

Unready work remains in `incubator/`. Retired skills move to `deprecated/` with a migration notice and are removed from generated catalogs.
