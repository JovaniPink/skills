#!/usr/bin/env python3
"""Build a deterministic release manifest for an exact tested source commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path

from cataloglib import ROOT, SKILLS, VERSION, directory_hashes, read_skill_metadata, skills_by_plugin


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_hash(path: Path) -> str:
    value = json.dumps(directory_hashes(path), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build(source_commit: str, output: Path | None = None) -> Path:
    if re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise ValueError("source commit must be a full 40-character lowercase Git SHA")
    artifacts: list[dict[str, str]] = []
    for client in ("codex", "claude"):
        for plugin in skills_by_plugin():
            path = ROOT / "plugins" / client / plugin
            artifacts.append({"kind": "tree", "path": path.relative_to(ROOT).as_posix(), "sha256": _tree_hash(path)})
    for path in (
        ROOT / ".agents" / "plugins" / "marketplace.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / "catalog" / "compatibility.json",
        ROOT / "catalog" / "deprecations.json",
        ROOT / "catalog" / "revocations.json",
        ROOT / "catalog" / "upstream-pins.json",
    ):
        artifacts.append({"kind": "file", "path": path.relative_to(ROOT).as_posix(), "sha256": _file_hash(path)})
    for skill in SKILLS:
        archive = ROOT / "dist" / "claude-ai" / f"{skill}-{VERSION}.zip"
        if not archive.is_file():
            raise FileNotFoundError(f"missing packaged skill: {archive}")
        artifacts.append({"kind": "zip", "path": archive.relative_to(ROOT).as_posix(), "sha256": _file_hash(archive)})
    value = {
        "$schema": "../manifest-schema.json",
        "catalog_version": VERSION,
        "source_commit": source_commit,
        "created_on": date.today().isoformat(),
        "artifacts": sorted(artifacts, key=lambda item: item["path"]),
    }
    target = (output or ROOT / "releases" / VERSION / "manifest.json").resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    target = build(args.source_commit, args.output)
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
