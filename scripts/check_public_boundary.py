#!/usr/bin/env python3
"""Scan canonical and generated text for common public-boundary violations."""

from __future__ import annotations

import re
from pathlib import Path

from cataloglib import ROOT


SCAN_ROOTS = (
    ROOT / "skills",
    ROOT / "plugins",
    ROOT / "docs",
    ROOT / "evals",
    ROOT / "provenance",
)
TEXT_SUFFIXES = {"", ".md", ".json", ".yaml", ".yml", ".txt", ".py"}


def _patterns() -> list[tuple[str, re.Pattern[str]]]:
    # Construct sensitive literals in pieces so this scanner does not flag itself.
    return [
        ("absolute macOS user path", re.compile("/" + "Users/[^/\\s]+/")),
        ("absolute Linux user path", re.compile("/" + "home/[^/\\s]+/")),
        ("private SSH remote", re.compile("git" + r"@[A-Za-z0-9_.-]+:")),
        ("work-repository path", re.compile(r"src/" + "work/", re.IGNORECASE)),
        ("private organization identifier", re.compile("Dig" + "DeepIQ", re.IGNORECASE)),
        ("private product identifier", re.compile("Form" + "578", re.IGNORECASE)),
        ("known proprietary source name", re.compile("Boun" + "teous", re.IGNORECASE)),
        ("GitHub token", re.compile("gh" + r"[pousr]_[A-Za-z0-9]{20,}")),
        ("OpenAI-style secret", re.compile("s" + r"k-[A-Za-z0-9]{20,}")),
        ("AWS access key", re.compile("AK" + r"IA[0-9A-Z]{16}")),
        ("private key block", re.compile("BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY")),
        ("unsupported universal validation claim", re.compile(r"all (?:clients|validators|surfaces) (?:pass|passed|are supported)", re.IGNORECASE)),
    ]


def scan() -> list[str]:
    errors: list[str] = []
    local_denylist = ROOT / ".local-boundary-denylist"
    patterns = _patterns()
    if local_denylist.is_file():
        for line in local_denylist.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value and not value.startswith("#"):
                patterns.append(("local denylist", re.compile(re.escape(value), re.IGNORECASE)))

    for scan_root in SCAN_ROOTS:
        if not scan_root.exists():
            errors.append(f"missing scan root: {scan_root.relative_to(ROOT)}")
            continue
        for path in sorted(scan_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            relative = path.relative_to(ROOT)
            for label, pattern in patterns:
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    errors.append(f"{relative}:{line}: {label}")
    return errors


def main() -> int:
    errors = scan()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Public/private boundary scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
