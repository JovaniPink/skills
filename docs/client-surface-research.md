# Client Surface Research

Reviewed: 2026-08-21

This note separates documented product support from observed installation and invocation behavior. It does not claim parity between clients.

## OpenAI surfaces

OpenAI documents plugin-bundled skills for Chat and Work across ChatGPT web, desktop, and mobile, as well as Codex in the ChatGPT desktop app and Codex CLI. Direct invocation uses `@` in ChatGPT and `$` in Codex. Repository and personal marketplaces are managed with the Codex CLI and installed and tested through the ChatGPT desktop app. Workspace publication is a separate administrative action from local installation, and the universal plugin directory is separate from local marketplaces.

Current observation: Codex CLI 0.145.0 installed all four local plugins at version 0.4.0 and passed the recorded v0.4 cases. ChatGPT Web in Safari 26.6 showed no installed skills. Therefore, the local marketplace installation was not treated as a web installation. No workspace publication or public-directory submission was attempted.

Primary sources:

- OpenAI, [Build skills](https://learn.chatgpt.com/docs/build-skills), reviewed 2026-08-21.
- OpenAI, [Build plugins](https://developers.openai.com/plugins/build/plugins), reviewed 2026-08-21.

## Anthropic surfaces

Anthropic documents user-scope and project-scope plugin installation for Claude Code, including local and SSH sessions in the desktop application. Claude.ai custom skills use individual ZIP uploads under account customization and are private to the individual account by default. These are different distribution paths and are tested separately.

Current observation: Claude Code CLI 2.1.220 installed all four plugins and exposed all 46 namespaced skills during initialization. Model-dependent tests were blocked because the OAuth session expired. Claude Code Desktop 1.34493.1 was not tested in a fresh message. No v0.4 Claude.ai upload was performed.

Primary sources:

- Anthropic, [Claude Code on desktop](https://code.claude.com/docs/en/desktop), reviewed 2026-08-21.
- Anthropic, [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins), reviewed 2026-08-21.
- Anthropic, [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces), reviewed 2026-08-21.
- Anthropic, [Use Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude), reviewed 2026-08-21.

## Security boundary

The exact generated v0.4 plugin trees were reviewed before local installation. They contain skills and references only: no hooks, MCP servers, bundled agents, skill-level executables, package dependencies, or broad tool permissions. The remaining risk is instruction behavior and implicit activation, so tests used fresh read-only sessions and no repository or remote mutation.

All four plugins should not be enabled by default without need. The combined discovery descriptions consumed enough context for Codex to shorten skill descriptions, and Claude reported about 3,377 tokens of always-on plugin context. Focused installation reduces trigger collision and context pressure.
