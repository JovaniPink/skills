# Authoring Rules

- Author canonical skills only under `skills/`; never author skills directly under `plugins/`.
- Treat all files under `plugins/`, `.agents/plugins/marketplace.json`, `.claude-plugin/marketplace.json`, and `.gemini/plugins/marketplace.json` as generated output. Regenerate client distributions using `python3 scripts/build_distributions.py --write-marketplaces`.
- Do not add private paths, identities, infrastructure contracts, secrets, proprietary text, hooks, MCP servers, broad tool grants, or skill-level executables.
- Write in ASCII, US English, and approachable language following `docs/editorial-style.md`.
- Keep diagnosis, review, publication, merge, deployment, and provider acceptance as separately authorized actions.
