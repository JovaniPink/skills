#!/usr/bin/env python3
"""Synchronize canonical private repo-local skills into Codex and Claude projections."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path

from cataloglib import add_claude_explicit_control, directory_hashes, read_skill_metadata


def _safe_target(repo: Path, relative: str) -> Path:
    target = (repo / relative).resolve()
    expected_parent = (repo / Path(relative).parent).resolve()
    if target.parent != expected_parent or target.name != "skills":
        raise ValueError(f"unsafe overlay target: {target}")
    return target


def _render(repo: Path, output: Path) -> tuple[Path, Path]:
    source = repo / ".agent-skills" / "skills"
    if not source.is_dir():
        raise FileNotFoundError(f"missing canonical overlay source: {source}")
    codex = output / ".agents" / "skills"
    claude = output / ".claude" / "skills"
    for skill_dir in sorted(path for path in source.iterdir() if path.is_dir()):
        metadata = read_skill_metadata(skill_dir)
        name = metadata["name"]
        if name != skill_dir.name:
            raise ValueError(f"overlay skill directory and name differ: {skill_dir}")
        shutil.copytree(skill_dir, codex / name)
        (claude / name).mkdir(parents=True)
        for item in sorted(skill_dir.iterdir()):
            if item.name == "agents":
                continue
            destination = claude / name / item.name
            if item.is_dir():
                shutil.copytree(item, destination)
            elif item.name == "SKILL.md" and metadata["invocation"] == "explicit":
                destination.write_text(add_claude_explicit_control(item.read_text(encoding="utf-8")), encoding="utf-8")
            else:
                shutil.copy2(item, destination)
    return codex, claude


def sync(repo: Path, check_only: bool) -> list[str]:
    repo = repo.resolve()
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="private-overlay-") as temporary:
        expected_codex, expected_claude = _render(repo, Path(temporary))
        pairs = (
            (expected_codex, _safe_target(repo, ".agents/skills")),
            (expected_claude, _safe_target(repo, ".claude/skills")),
        )
        for expected, actual in pairs:
            if check_only:
                if directory_hashes(expected) != directory_hashes(actual):
                    errors.append(f"private overlay projection drifted: {actual.relative_to(repo)}")
                continue
            if actual.exists():
                shutil.rmtree(actual)
            actual.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(expected, actual)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = sync(args.repo, args.check)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Private overlay projections match canonical sources." if args.check else "Private overlay projections synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
