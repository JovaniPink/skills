#!/usr/bin/env python3
"""Synchronize canonical private repo-local skills into Codex and Claude projections."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import tempfile
from pathlib import Path

from cataloglib import add_claude_explicit_control, directory_hashes, read_skill_metadata


def _safe_target(repo: Path, relative: str) -> Path:
    """Return the projection folder inside repo, refusing any symlinked path.

    Resolving through a symlinked `.agents` or `.claude` parent would let sync remove
    and replace a directory outside the repository, so every component between the
    repository and the target must be a real directory (or not exist yet), and the
    resolved target must stay inside the repository.
    """
    current = repo
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"unsafe overlay target: {current} is a symlink")
    target = (repo / relative).resolve()
    expected_parent = (repo / Path(relative).parent).resolve()
    if (
        target.parent != expected_parent
        or target.name != "skills"
        or not target.is_relative_to(repo)
    ):
        raise ValueError(f"unsafe overlay target: {target}")
    return target


def _directory_flags() -> int | None:
    """No-follow directory open flags, or None where the platform lacks them (Windows).

    Looked up lazily so importing this module, and running --check, work everywhere.
    """
    directory = getattr(os, "O_DIRECTORY", None)
    no_follow = getattr(os, "O_NOFOLLOW", None)
    if directory is None or no_follow is None or not shutil.rmtree.avoids_symlink_attacks:
        return None
    return os.O_RDONLY | directory | no_follow


def _open_directory(name: str, dir_fd: int, create: bool = False) -> int:
    """Open a directory relative to dir_fd without following a symlink at name."""
    flags = _directory_flags()
    if flags is None:
        raise ValueError("overlay synchronization requires no-follow directory support")
    try:
        return os.open(name, flags, dir_fd=dir_fd)
    except FileNotFoundError:
        if not create:
            raise
        os.mkdir(name, 0o755, dir_fd=dir_fd)
        return os.open(name, flags, dir_fd=dir_fd)


def _copy_tree_into(source: Path, name: str, dir_fd: int) -> None:
    """Copy a trusted rendered tree to name under dir_fd, creating every entry exclusively."""
    os.mkdir(name, 0o755, dir_fd=dir_fd)
    target_fd = _open_directory(name, dir_fd)
    try:
        for entry in sorted(source.iterdir()):
            if entry.is_symlink():
                raise ValueError(f"rendered overlay contains a symlink: {entry}")
            if entry.is_dir():
                _copy_tree_into(entry, entry.name, target_fd)
                continue
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
            output = os.open(entry.name, flags, stat.S_IMODE(entry.stat().st_mode), dir_fd=target_fd)
            try:
                data = memoryview(entry.read_bytes())
                while data:
                    data = data[os.write(output, data):]
            finally:
                os.close(output)
    finally:
        os.close(target_fd)


def _replace_projection(repo_fd: int, relative: str, expected: Path) -> None:
    """Replace repo/relative with expected, bound to directory handles, never following links.

    The parent (.agents or .claude) is opened with O_NOFOLLOW, and every later step
    works relative to that handle, so a symlink swapped in after validation cannot
    redirect the delete or the copy outside the repository. The old projection is
    renamed aside and removed with the symlink-safe fd-based rmtree.
    """
    parent_name, leaf = Path(relative).parts
    token = f"{os.getpid()}-{os.urandom(4).hex()}"
    staging, retired = f".{leaf}.sync-{token}", f".{leaf}.old-{token}"
    parent_fd = _open_directory(parent_name, repo_fd, create=True)
    try:
        _copy_tree_into(expected, staging, parent_fd)
        try:
            existing = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        if existing is not None:
            if not stat.S_ISDIR(existing.st_mode):
                shutil.rmtree(staging, dir_fd=parent_fd)
                raise ValueError(f"unsafe overlay target: {relative} is not a directory")
            os.rename(leaf, retired, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
            shutil.rmtree(retired, dir_fd=parent_fd)
        os.rename(staging, leaf, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
    finally:
        os.close(parent_fd)


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


def _check_existing_conventions(repo: Path) -> list[str]:
    """Refuse repositories whose client skill folders are not projections of .agent-skills/."""
    if (repo / ".agent-skills").exists():
        return []
    for relative in (".claude/skills", ".agents/skills"):
        if (repo / relative).exists():
            return [
                f"{relative} exists without .agent-skills/; follow the existing repo-local "
                "skill convention instead of this synchronizer"
            ]
    return []


def sync(repo: Path, check_only: bool) -> list[str]:
    repo = repo.resolve()
    errors = _check_existing_conventions(repo)
    if errors:
        return errors
    with tempfile.TemporaryDirectory(prefix="private-overlay-") as temporary:
        expected_codex, expected_claude = _render(repo, Path(temporary))
        # Validate every target before changing any, so a bad second target cannot
        # leave the first one already replaced.
        targets = [
            (expected, relative, _safe_target(repo, relative))
            for expected, relative in ((expected_codex, ".agents/skills"), (expected_claude, ".claude/skills"))
        ]
        if check_only:
            for expected, _relative, actual in targets:
                if directory_hashes(expected) != directory_hashes(actual):
                    errors.append(f"private overlay projection drifted: {actual.relative_to(repo)}")
            return errors
        flags = _directory_flags()
        if flags is None:
            raise ValueError("overlay synchronization requires no-follow directory support; use --check on this platform")
        # Bind the repository once, without following a symlink at its path, and do every
        # replacement relative to that handle so a renamed repository cannot redirect it.
        repo_fd = os.open(repo, flags)
        try:
            for expected, relative, _actual in targets:
                _replace_projection(repo_fd, relative, expected)
        finally:
            os.close(repo_fd)
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
