# Authoring Guide

## Scope

One skill should express one reusable capability. Put activation context in the frontmatter description and procedural content in the body. Keep `SKILL.md` concise; move substantial lookup material into focused `references/` files.

Use lowercase hyphenated names no longer than 64 characters. The directory name and frontmatter `name` must match.

## Required frontmatter

```yaml
---
name: example-skill
description: What the skill does and the concrete situations that should activate it.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.1.0"
  plugin: "jovanipink-skills"
  invocation: "implicit"
  provenance: "original"
  risk_class: "read-only"
---
```

All metadata values are strings. Invocation is either `implicit` or `explicit`. Use explicit invocation when the workflow primarily coordinates publication, deployment, destructive mutation, credentialed writes, import of untrusted code, or a similarly consequential trust decision. `plugin` selects the generated distribution. `provenance` records implementation method, while the catalog separately records capability disposition. `risk_class` is one of `read-only`, `bounded-execution`, `network-read`, `external-write`, or `trust-decision`.

## Codex interface

Every canonical skill includes `agents/openai.yaml`:

```yaml
interface:
  display_name: "Example Skill"
  short_description: "A compact interface description"
  default_prompt: "Use $example-skill to ..."
policy:
  allow_implicit_invocation: true
```

The canonical default prompt must mention the skill with `$skill-name`. Set the policy to `false` for explicit-only skills. Generation rewrites that prompt to `$jovanipink-skills:skill-name` for the installed plugin namespace.

## Workflow rules

- Name the authority capable of proving each conclusion.
- Distinguish observation, inference, proposal, and unresolved questions.
- Preserve the boundary between diagnosis and remediation.
- Do not assume one quality command, branch name, remote, identity, provider, framework, or deployment target.
- State stop conditions and missing-evidence outcomes.
- Keep deterministic enforcement in scripts, tests, CI, or host permissions.
- Do not encode workspace-specific private facts in a public skill.

## References and scripts

References must be directly linked from `SKILL.md`, use relative paths, and be necessary to execute the workflow. The catalog does not permit skill-level scripts, hooks, MCP servers, dependencies, bundled agents, or executable payloads.

## Completion checklist

- standards-valid skill structure
- native Codex and Claude invocation mapping
- provenance record
- three positive, three near-miss, and one conflict/safety trigger case
- reference and link validation
- public/private boundary scan
- generated-tree drift check
- client-specific smoke evidence where release policy requires it
