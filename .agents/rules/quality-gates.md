# Quality Gates

- Before describing the catalog as valid or ready for commit, run the repository validation gates:
  - `python3 scripts/validate.py`
  - `python3 scripts/check_workflows.py`
  - `python3 scripts/build_distributions.py --check`
  - `python3 -m unittest discover -s tests -v`
- Never infer client behavioral parity across Codex, Claude, and Antigravity. Record manual client behavior as observed evidence in `catalog/google-surfaces.json` and client observation records.
- Preserve deterministic validation: no network calls, no cloud credentials, and no external package dependencies beyond Python standard library and pinned tools.
