# Google ADK and Agent Skills

Google Agent Development Kit, or ADK, affects this project in two different ways. Keep them separate.

## Developer-assistant use

ChatGPT, Codex, Claude, and Gemini CLI can use a human-facing skill to help a developer design, build, test, or review an ADK application. In this repository, `google-adk-engineering-profile` is that kind of workflow.

It can help a person:

- discover the exact ADK language and version in a repository;
- review agent, runner, session, memory, artifact, tool, protocol, evaluation, and deployment boundaries;
- compose ADK-specific work with general security, evaluation, observability, performance, and operational-readiness skills;
- keep experimental framework behavior separate from observed local results.

It cannot deploy an agent, create cloud infrastructure, authenticate to a provider, release a product bundle, or grant a tool.

## Runtime-agent use

ADK can also load open-format Agent Skills as capabilities inside an ADK agent through `SkillToolset`. Google documents this feature as experimental. The toolset can expose facilities that load skill instructions, load skill resources, and run skill scripts.

That is a larger trust boundary than using a skill as developer guidance. A production agent can act on user data and registered tools. Skill content must not decide which tools exist or which credentials, identities, tenants, or production resources they can reach.

Runtime skills therefore belong in the separate `JovaniPink/jovanipink-adk` foundation and private product overlays. They do not belong in this assistant catalog's client observation matrix.

The planned first runtime foundation accepts instruction and Markdown reference files only. It rejects scripts, hooks, assets, executables, dependency manifests, `allowed-tools`, mutable remote loading, and undeclared archive content. Its public contract verifies a content-addressed bundle and release receipt before constructing an ADK skill toolset. This assistant repository does not claim that separate implementation is complete.

## Google Agents CLI

Google Agents CLI is optional developer tooling. Google publishes seven skills that help coding agents work with ADK projects. This project does not vendor those skills and does not make the CLI a runtime dependency.

Before any workspace installation:

1. Review the exact repository revision and Apache-2.0 license.
2. Inspect the files, dependencies, and installation behavior.
3. Pin an immutable revision in provenance.
4. Preview the workspace changes.
5. Keep authentication, infrastructure creation, deployment, and publication separately authorized.

Do not perform an unreviewed global installation.

## Version and evidence rules

- Discover the installed ADK version from the project lockfile and runtime, not from a remembered latest version.
- Treat `SkillToolset` and tool confirmation as experimental until exact-version tests pass.
- Record language support separately for Python, TypeScript, and Go.
- Keep local construction, evaluation, deployment, and live production behavior as separate claims.
- Do not claim ADK parity across assistant clients or runtime languages.

## Primary resources

- [ADK Agent Skills](https://adk-labs.github.io/adk-docs/skills/)
- [ADK safety and security](https://adk-labs.github.io/adk-docs/safety/)
- [ADK evaluation](https://adk-labs.github.io/adk-docs/evaluate/)
- [ADK tool confirmation](https://adk-labs.github.io/adk-docs/tools-custom/confirmation/)
- [Google Agents CLI](https://github.com/google/agents-cli)
- [Google Agents CLI skills](https://google.github.io/agents-cli/reference/skills/)
- [Gemini CLI Agent Skills](https://geminicli.com/docs/cli/skills/)
