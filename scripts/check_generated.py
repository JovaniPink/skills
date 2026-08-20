#!/usr/bin/env python3
"""Fail when tracked plugin trees drift from canonical sources."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from build_distributions import build, marketplace_documents
from cataloglib import PLUGIN_NAME, ROOT, directory_hashes


def check() -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="jovanipink-skills-") as temporary:
        output_root = Path(temporary) / "plugins"
        build(output_root, write_marketplaces=False)
        for client in ("codex", "claude"):
            expected = directory_hashes(output_root / client / PLUGIN_NAME)
            actual = directory_hashes(ROOT / "plugins" / client / PLUGIN_NAME)
            missing = sorted(set(expected) - set(actual))
            extra = sorted(set(actual) - set(expected))
            changed = sorted(path for path in set(expected) & set(actual) if expected[path] != actual[path])
            for path in missing:
                errors.append(f"{client} generated file missing: {path}")
            for path in extra:
                errors.append(f"{client} generated file unexpected: {path}")
            for path in changed:
                errors.append(f"{client} generated file drifted: {path}")

        codex_marketplace, claude_marketplace = marketplace_documents()
        expected_marketplaces = (
            (ROOT / ".agents" / "plugins" / "marketplace.json", codex_marketplace),
            (ROOT / ".claude-plugin" / "marketplace.json", claude_marketplace),
        )
        for path, expected in expected_marketplaces:
            rendered = json.dumps(expected, indent=2, sort_keys=False) + "\n"
            if not path.is_file():
                errors.append(f"generated marketplace missing: {path.relative_to(ROOT)}")
            elif path.read_text(encoding="utf-8") != rendered:
                errors.append(f"generated marketplace drifted: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Generated distributions match canonical sources.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
