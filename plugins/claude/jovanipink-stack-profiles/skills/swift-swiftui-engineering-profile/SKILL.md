---
name: swift-swiftui-engineering-profile
description: Apply focused Swift and SwiftUI engineering judgment after repository gate discovery. Use for packages, applications, concurrency, UI state, tests, compatibility, and builds; require observed macOS evidence for Apple toolchain claims.
license: MIT
metadata:
  author: "Jovani Pink"
  version: "0.12.0"
  plugin: "jovanipink-stack-profiles"
  invocation: "implicit"
  provenance: "clean-room"
  risk_class: "read-only"
---

# Swift and SwiftUI Engineering Profile

Use this profile only after repository discovery identifies the stack. Read [focused checks](references/checks.md) when stack-specific gates or hazards determine the result.

## Workflow

1. Discover `Package.swift`, Xcode projects or workspaces, schemes, package resolution, deployment targets, and repository scripts.
2. Follow repository-defined commands and pinned tool versions before suggesting defaults.
3. Review idiomatic design and material hazards, especially actor isolation, `Sendable` gaps, retain cycles, value versus reference semantics, optionals, task cancellation, view identity, state ownership, and main-thread work.
4. Select proportionate gates from repository scripts, formatting or linting, Swift package tests and builds, selected Xcode scheme tests, static analysis, and simulator or device checks when available.
5. Review compatibility across Swift language mode, package versions, OS deployment targets, availability annotations, data migrations, and SwiftUI behavior across supported devices.
6. Report every missing tool, skipped command, unsupported platform, or unavailable environment as incomplete rather than passing.

## Boundaries

- Do not invent one universal command or replace repository policy with generic preferences.
- Do not install, upgrade, publish, deploy, apply, or mutate shared state merely to run a gate.
- Separate static review, executed checks, build evidence, provider state, and live behavior.

## Output

Return Discovery, Hazards, Commands selected, Results, Compatibility, Missing evidence, and Next safe gate.

