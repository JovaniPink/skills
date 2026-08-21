#!/usr/bin/env python3
"""Reject source-specific terms from canonical and generated skill content."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

from cataloglib import ROOT


PROHIBITED = {
    "source-specific person router": re.compile(r"\bask-matt\b", re.IGNORECASE),
    "source-specific repository name": re.compile(r"\bpstack\b", re.IGNORECASE),
    "source-specific mode name": re.compile(r"\bpoteto(?:-mode)?\b", re.IGNORECASE),
    "source-specific style name": re.compile(r"\bunslop\b", re.IGNORECASE),
    "source-specific agent name": re.compile(r"\bcomment sicko\b", re.IGNORECASE),
    "source-specific automation name": re.compile(r"\bbenny\b", re.IGNORECASE),
    "source-specific transcript path": re.compile(r"\.cursor/projects|agent-transcripts", re.IGNORECASE),
    "source-specific model slug": re.compile(r"(?:claude-fable|gpt-5\.6-sol-max|inherit-parent)", re.IGNORECASE),
    "source-specific config path": re.compile(r"pstack-models\.mdc", re.IGNORECASE),
}


def _scan_text(label: str, text: str) -> list[str]:
    errors: list[str] = []
    for finding, pattern in PROHIBITED.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{label}:{line}: {finding}")
    return errors


def _content_paths() -> list[Path]:
    roots = (ROOT / "skills", ROOT / "plugins" / "codex", ROOT / "plugins" / "claude")
    return sorted(path for root in roots if root.is_dir() for path in root.rglob("*") if path.is_file())


def check(include_packages: bool = True) -> list[str]:
    errors: list[str] = []
    for path in _content_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        errors.extend(_scan_text(path.relative_to(ROOT).as_posix(), text))
    if include_packages:
        for archive_path in sorted((ROOT / "dist" / "claude-ai").glob("*.zip")):
            with zipfile.ZipFile(archive_path) as archive:
                for member in archive.namelist():
                    try:
                        text = archive.read(member).decode("utf-8")
                    except UnicodeDecodeError:
                        continue
                    errors.extend(_scan_text(f"{archive_path.relative_to(ROOT)}!{member}", text))
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Canonical, generated, and packaged skill content passed the clean-room originality scan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
