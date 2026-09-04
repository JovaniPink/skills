# Script guidance

- Keep repository generation and validation deterministic and standard-library-only unless the reviewed CI contract explicitly says otherwise.
- Add a failing regression test before changing validator behavior.
- Do not add network access, credentials, external writes, or hidden installation behavior.
- Generated output must be reproducible from canonical source and fail on drift.
