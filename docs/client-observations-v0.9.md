# v0.9 Client Observation Notes

This document summarizes sanitized observations for the v0.9 candidate. The strict machine-readable record is in `client-observations-v0.9.json`.

## Current result

v0.9 acceptance remains blocked. Local package installation is not proof of web, desktop, API, or managed-agent behavior.

| Surface | Observed result | Important limitation |
| --- | --- | --- |
| Codex CLI 0.149.0-alpha.4.3 | All seven plugins installed. Skill discovery and focused-reference loading passed. | The full catalog caused description shortening, so smaller plugin packs remain the recommended default. |
| Codex Desktop 26.818.61809 build 7019 | Local cache installed. | A fresh post-install desktop task is still required. |
| ChatGPT Desktop 26.818.61809 build 7019 | Local cache installed. | This task cannot control its own application, so desktop discovery is not observed. |
| ChatGPT web | Existing custom skills were visible. | The new v0.9 agent security skill was absent. Local installation did not synchronize the web library. |
| Claude Code CLI 2.1.220 | All seven plugins and all 76 skills were discoverable. | Focused-reference invocation stopped because local OAuth had expired. |
| Claude Code Desktop 1.34493.1 | The application was signed in. | A pending relaunch was not performed because active work could have been interrupted. |
| Claude.ai | Existing custom skills were visible. | The new v0.9 agent security skill was absent. Claude Code plugin installation did not synchronize the cloud library. |
| Gemini CLI 0.56.0 (historical) | All 76 skills linked into a disposable workspace. | This predates Google's individual-user Antigravity transition and does not establish current enterprise Gemini CLI or Antigravity compatibility. Authenticated discovery was not completed. |
| OpenAI Skills API | Official interface reviewed. | No credential, project, network, or cost authority was available for an observed upload or invocation. |
| Anthropic Skills API | Official interface reviewed. | No credential, workspace, network, or cost authority was available for an observed upload or invocation. |
| Anthropic Managed Agents | Official trust model reviewed. | No account capability, credential, network, or cost authority was available for an observed session. |

## Security decisions

- Only reviewed instruction-and-reference plugins were installed.
- No plugin contains hooks, MCP servers, bundled agents, executables, dependency manifests, or tool grants.
- Historical Gemini CLI testing used the official Apache-2.0 package at exact version 0.56.0 through npx.
- Gemini skills were linked only in a disposable workspace. Nothing was installed globally.
- No new API key, OAuth grant, cloud credential, or persistent external access was created.
- Claude Desktop was not restarted while active work was running.
- Raw browser content, account details, credentials, user paths, and private project names are not included in public evidence.

## Required next observations

1. Start a fresh ChatGPT or Codex Desktop task after the plugin refresh.
2. Upload or update the v0.9 custom skill ZIPs in ChatGPT web and Claude.ai, then verify reference loading and invocation.
3. Restore Claude Code authentication and rerun the read-only focused-reference test.
4. After the Codex pilot identifies a useful treatment, create a clean Antigravity CLI experiment. Test Gemini CLI only when an applicable enterprise license is intentionally in scope.
5. Run the API surfaces only after credential, project or workspace, network, and cost authority are explicit.

## Primary documentation

- [OpenAI skill building](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI plugin packaging and local marketplaces](https://developers.openai.com/plugins/build/plugins)
- [Anthropic plugin discovery and installation](https://code.claude.com/docs/en/discover-plugins)
- [Anthropic Managed Agents skills](https://platform.claude.com/docs/en/managed-agents/skills)
- [Google's Gemini CLI to Antigravity CLI transition](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)
- [Antigravity Agent Skills](https://antigravity.google/docs/skills/)
