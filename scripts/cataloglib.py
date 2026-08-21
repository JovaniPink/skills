"""Shared, standard-library-only helpers for the portable skill catalog."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.4.0"
CATALOG_NAME = "jovanipink-skills"
PLUGIN_CATEGORY = "Developer Tools"
PLUGIN_SPECS = {
    "jovanipink-skills": {
        "display_name": "JovaniPink Skills",
        "description": "Portable evidence, diagnosis, quality, publication, and skill-security workflows.",
        "short_description": "Evidence-oriented workflows for Codex",
        "keywords": ["skills", "research", "diagnosis", "quality", "security"],
    },
    "jovanipink-engineering": {
        "display_name": "JovaniPink Engineering",
        "description": "Portable planning, testing, review, worktree, branch, and orchestration workflows.",
        "short_description": "Engineering lifecycle workflows for Codex",
        "keywords": ["skills", "engineering", "testing", "review", "git"],
    },
    "jovanipink-stack-profiles": {
        "display_name": "JovaniPink Stack Profiles",
        "description": "Optional language and infrastructure engineering profiles.",
        "short_description": "Stack-specific engineering guidance for Codex",
        "keywords": ["skills", "engineering", "languages", "infrastructure"],
    },
    "jovanipink-operations": {
        "display_name": "JovaniPink Operations",
        "description": "Portable requirements, decision, measurement, adoption, and incident workflows.",
        "short_description": "Operating and decision workflows for Codex",
        "keywords": ["skills", "operations", "decisions", "measurement"],
    },
}


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


def skill_names() -> tuple[str, ...]:
    root = ROOT / "skills"
    if not root.is_dir():
        return ()
    return tuple(sorted(path.name for path in root.iterdir() if path.is_dir()))


def revoked_skill_names(path: Path | None = None) -> frozenset[str]:
    registry = path or ROOT / "catalog" / "revocations.json"
    if not registry.is_file():
        return frozenset()
    value = json.loads(registry.read_text(encoding="utf-8"))
    entries = value.get("entries", []) if isinstance(value, dict) else []
    return frozenset(
        entry["skill"] for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("skill"), str)
    )


def filter_revoked(skills: tuple[str, ...], revoked: frozenset[str]) -> tuple[str, ...]:
    return tuple(skill for skill in skills if skill not in revoked)


def skills_by_plugin() -> dict[str, tuple[str, ...]]:
    grouped: dict[str, list[str]] = {}
    for skill in SKILLS:
        plugin = read_skill_metadata(ROOT / "skills" / skill)["plugin"]
        grouped.setdefault(plugin, []).append(skill)
    return {plugin: tuple(skills) for plugin, skills in sorted(grouped.items())}


ALL_SKILLS = skill_names()
SKILLS = filter_revoked(ALL_SKILLS, revoked_skill_names())
EXPLICIT_SKILLS = frozenset(
    skill for skill in SKILLS if read_skill_metadata(ROOT / "skills" / skill)["invocation"] == "explicit"
)
PLUGIN_NAME = CATALOG_NAME


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
