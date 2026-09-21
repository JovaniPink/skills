#!/usr/bin/env python3
"""Export implicit skills to a new staging directory without installing anything."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from build_distributions import _copy_claude_skill
from cataloglib import EXPLICIT_SKILLS, ROOT, SKILLS, VERSION, directory_hashes


def export(output: Path, client: str, selected: list[str]) -> None:
    if client not in {"codex", "claude"}:
        raise ValueError("client must be codex or claude")
    if not selected or len(selected) != len(set(selected)):
        raise ValueError("select at least one skill without duplicates")
    if set(selected) - set(SKILLS):
        raise ValueError("unknown or revoked skill")
    if set(selected) & EXPLICIT_SKILLS:
        raise ValueError("explicit-only skills require separately verified plugin activation")
    if output.exists() or output.is_symlink():
        raise ValueError("output must be a new staging directory")
    for skill in selected:
        source = ROOT / "skills" / skill
        if not (source / "SKILL.md").is_file():
            raise ValueError("missing canonical skill")
        for item in source.rglob("*"):
            if item.is_symlink():
                raise ValueError("symlinks are not permitted in selected exports")
            if item.suffix == ".md":
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", item.read_text()):
                    target = target.split("#", 1)[0].strip("<>")
                    if not target or "://" in target or target.startswith("mailto:"):
                        continue
                    resolved = (item.parent / target).resolve()
                    if not resolved.is_relative_to(source.resolve()) or not resolved.exists():
                        raise ValueError("missing or non-portable selected-skill reference")
    # Resolve the parent, but never follow an output symlink or replace old output.
    output = output.parent.resolve() / output.name
    output.mkdir(parents=True, exist_ok=False)
    for skill in sorted(selected):
        source = ROOT / "skills" / skill
        target = output / skill
        if client == "codex":
            shutil.copytree(source, target)
        else:
            _copy_claude_skill(source, target, explicit=False)
    manifest = {
        "catalog_version": VERSION,
        "client": client,
        "skills": sorted(selected),
        "files": directory_hashes(output),
        "installation": "not_installed",
        "behavior": "not_observed",
    }
    (output / "export-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--client", choices=("codex", "claude"), required=True)
    parser.add_argument("--skill", action="append", required=True)
    args = parser.parse_args()
    try:
        export(args.output, args.client, args.skill)
    except ValueError as error:
        parser.error(str(error))
    print("Selected skills exported; no client configuration or installation changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
