# Gate discovery

Use only the rows matching the target repository. Repository instructions and CI remain authoritative.

| Stack signal | Common discovery surfaces | Candidate gates to confirm |
|---|---|---|
| Go | `go.mod`, `go.work`, CI | `go test`, `go vet`, project linters, build |
| Python | `pyproject.toml`, lockfiles, `tox.ini`, CI | project test, type, lint, package, and migration checks |
| Swift | `Package.swift`, `.xcodeproj`, `.xcworkspace`, CI | SwiftPM tests or explicit `xcodebuild` scheme and destination |
| TypeScript / JavaScript | `package.json`, workspace files, CI | declared lint, typecheck, test, and build scripts using the committed package manager |
| SQL | migration config, model directories, warehouse docs, CI | formatter or parser, migration checks, engine-specific tests, data-quality queries |
| Terraform | `.terraform-version`, lockfile, modules, CI | format check, init without backend when appropriate, validate, lint, and plan |

## Selection checks

- Prefer commands already used by CI or documented for contributors.
- Inspect lockfiles before choosing a package manager or tool version.
- Confirm required services, credentials, simulators, or remote backends before running a gate.
- If a command can mutate tracked files or external state, use its check-only form or request authorization.
- When no gate exists, report the missing contract and suggest a gate; do not invent a passing substitute.
