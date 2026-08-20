# Repository guidance

- Author skills only under `skills/`; regenerate client distributions.
- Treat `plugins/` as generated output.
- Do not add private paths, identities, infrastructure contracts, secrets, proprietary text, hooks, MCP servers, broad tool grants, or skill-level executables.
- Keep diagnosis, review, publication, merge, deployment, and provider acceptance as separately authorized actions.
- Run `python3 scripts/validate.py` and the unit tests before describing the catalog as valid.
- Record manual client behavior as observed evidence; never infer parity across clients.
