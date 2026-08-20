"""Shared, standard-library-only helpers for the portable skill catalog."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
PLUGIN_NAME = "jovanipink-skills"
PLUGIN_CATEGORY = "Developer Tools"
SKILLS = (
    "authority-boundary-review",
    "claim-verification",
    "cross-stack-quality-gates",
    "prelaunch-readiness",
    "public-private-boundary-review",
    "publish-change-safely",
    "skill-import-provenance",
    "skill-security-review",
    "source-grounded-research",
    "systematic-diagnosis",
)
EXPLICIT_SKILLS = frozenset({"publish-change-safely", "skill-import-provenance"})


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    marker = "\n---\n"
    end = text.find(marker, 4)
    if end < 0:
        raise ValueError("SKILL.md has no closing frontmatter delimiter")
    return text[4:end], text[end + len(marker) :]


def _scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        raise ValueError(f"missing frontmatter key: {key}")
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def _metadata_scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^\s{{2}}{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        raise ValueError(f"missing metadata key: {key}")
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def read_skill_metadata(skill_dir: Path) -> dict[str, str]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(text)
    result = {
        "name": _scalar(frontmatter, "name"),
        "description": _scalar(frontmatter, "description"),
        "license": _scalar(frontmatter, "license"),
        "author": _metadata_scalar(frontmatter, "author"),
        "version": _metadata_scalar(frontmatter, "version"),
        "plugin": _metadata_scalar(frontmatter, "plugin"),
        "invocation": _metadata_scalar(frontmatter, "invocation"),
        "provenance": _metadata_scalar(frontmatter, "provenance"),
        "risk_class": _metadata_scalar(frontmatter, "risk_class"),
    }
    result["claude_explicit"] = "true" if re.search(
        r"(?m)^disable-model-invocation:\s*true\s*$", frontmatter
    ) else "false"
    return result


def add_claude_explicit_control(text: str) -> str:
    frontmatter, body = split_frontmatter(text)
    if re.search(r"(?m)^disable-model-invocation:", frontmatter):
        raise ValueError("canonical frontmatter must not contain Claude-native controls")
    return f"---\n{frontmatter}\ndisable-model-invocation: true\n---\n{body}"


def directory_hashes(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if not path.is_dir():
        return hashes
    for item in sorted(path.rglob("*")):
        if item.is_file():
            relative = item.relative_to(path).as_posix()
            hashes[relative] = hashlib.sha256(item.read_bytes()).hexdigest()
    return hashes
