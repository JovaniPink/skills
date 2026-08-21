# Focused checks

Primary documentation: [official Swift and SwiftUI Engineering Profile reference](https://www.swift.org/documentation/). Verify version-sensitive behavior against the repository's pinned toolchain.

## Discovery

Inspect `Package.swift`, Xcode projects or workspaces, schemes, package resolution, deployment targets, and repository scripts. Resolve nested modules, workspaces, generated sources, and CI commands before selecting gates.

## Judgment focus

Review actor isolation, `Sendable` gaps, retain cycles, value versus reference semantics, optionals, task cancellation, view identity, state ownership, and main-thread work.

## Gate families

Consider repository scripts, formatting or linting, Swift package tests and builds, selected Xcode scheme tests, static analysis, and simulator or device checks when available. Run only commands supported by repository evidence and the current authorization boundary.

## Compatibility

Check Swift language mode, package versions, OS deployment targets, availability annotations, data migrations, and SwiftUI behavior across supported devices. Record unavailable tools and environments explicitly; never manufacture a passing result.

