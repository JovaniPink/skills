#!/usr/bin/env python3
"""Generate tracked Codex and Claude plugin distributions."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from cataloglib import (
    EXPLICIT_SKILLS,
    PLUGIN_CATEGORY,
    PLUGIN_NAME,
    ROOT,
    SKILLS,
    VERSION,
    add_claude_explicit_control,
)


DESCRIPTION = "Portable evidence, diagnosis, quality, publication, and skill-security workflows."


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def marketplace_documents() -> tuple[dict[str, object], dict[str, object]]:
    """Return the client-native marketplace documents for tracked output."""

    codex = {
        "name": PLUGIN_NAME,
        "interface": {"displayName": "JovaniPink Skills"},
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "source": {
                    "source": "local",
                    "path": "./plugins/codex/jovanipink-skills",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": PLUGIN_CATEGORY,
            }
        ],
    }
    claude = {
        "name": PLUGIN_NAME,
        "description": "Portable evidence-oriented workflow skills for software, research, and operations.",
        "owner": {"name": "Jovani Pink", "url": "https://jovanipink.com"},
        "plugins": [
            {
                "name": PLUGIN_NAME,
                "source": "./plugins/claude/jovanipink-skills",
                "description": DESCRIPTION,
                "version": VERSION,
            }
        ],
    }
    return codex, claude


def _reset_directory(path: Path, allowed_parent: Path) -> None:
    path = path.resolve()
    allowed_parent = allowed_parent.resolve()
    if path.parent != allowed_parent or path.name != PLUGIN_NAME:
        raise ValueError(f"refusing to reset unexpected distribution path: {path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def _copy_codex_skill(source: Path, target: Path, skill: str) -> None:
    shutil.copytree(source, target)
    interface_path = target / "agents" / "openai.yaml"
    interface = interface_path.read_text(encoding="utf-8")
    interface_path.write_text(
        interface.replace(f"${skill}", f"${PLUGIN_NAME}:{skill}"),
        encoding="utf-8",
    )


def _copy_claude_skill(source: Path, target: Path, explicit: bool) -> None:
    target.mkdir(parents=True)
    for item in sorted(source.iterdir()):
        if item.name == "agents":
            continue
        destination = target / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        elif item.name == "SKILL.md" and explicit:
            destination.write_text(
                add_claude_explicit_control(item.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        else:
            shutil.copy2(item, destination)


def build(output_root: Path, write_marketplaces: bool = False) -> tuple[Path, Path]:
    output_root = output_root.resolve()
    codex_parent = output_root / "codex"
    claude_parent = output_root / "claude"
    codex_plugin = codex_parent / PLUGIN_NAME
    claude_plugin = claude_parent / PLUGIN_NAME
    codex_parent.mkdir(parents=True, exist_ok=True)
    claude_parent.mkdir(parents=True, exist_ok=True)
    _reset_directory(codex_plugin, codex_parent)
    _reset_directory(claude_plugin, claude_parent)

    for skill in SKILLS:
        source = ROOT / "skills" / skill
        if not source.is_dir():
            raise FileNotFoundError(f"missing canonical skill: {source}")
        _copy_codex_skill(source, codex_plugin / "skills" / skill, skill)
        _copy_claude_skill(source, claude_plugin / "skills" / skill, skill in EXPLICIT_SKILLS)

    _write_json(
        codex_plugin / ".codex-plugin" / "plugin.json",
        {
            "name": PLUGIN_NAME,
            "version": VERSION,
            "description": DESCRIPTION,
            "author": {"name": "Jovani Pink", "url": "https://jovanipink.com"},
            "homepage": "https://github.com/JovaniPink/skills",
            "repository": "https://github.com/JovaniPink/skills",
            "license": "MIT",
            "skills": "./skills/",
            "interface": {
                "displayName": "JovaniPink Skills",
                "shortDescription": "Evidence-oriented workflows for Codex",
                "longDescription": DESCRIPTION,
                "developerName": "Jovani Pink",
                "category": PLUGIN_CATEGORY,
                "capabilities": ["Skills"],
                "defaultPrompt": [
                    "Help me choose and use a JovaniPink workflow skill."
                ],
            },
        },
    )
    _write_json(
        claude_plugin / ".claude-plugin" / "plugin.json",
        {
            "name": PLUGIN_NAME,
            "version": VERSION,
            "description": DESCRIPTION,
            "author": {"name": "Jovani Pink", "url": "https://jovanipink.com"},
            "homepage": "https://github.com/JovaniPink/skills",
            "repository": "https://github.com/JovaniPink/skills",
            "license": "MIT",
            "keywords": ["skills", "research", "diagnosis", "quality", "security"],
        },
    )

    if write_marketplaces:
        codex_marketplace, claude_marketplace = marketplace_documents()
        _write_json(ROOT / ".agents" / "plugins" / "marketplace.json", codex_marketplace)
        _write_json(ROOT / ".claude-plugin" / "marketplace.json", claude_marketplace)
    return codex_plugin, claude_plugin


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "plugins",
        help="Parent containing codex/ and claude/ distribution directories.",
    )
    parser.add_argument(
        "--write-marketplaces",
        action="store_true",
        help="Also rewrite root marketplace files when the host permits it.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare tracked output with a temporary render without modifying the checkout.",
    )
    args = parser.parse_args()
    if args.check:
        if args.output_root != ROOT / "plugins" or args.write_marketplaces:
            parser.error("--check cannot be combined with output or write options")
        from check_generated import check

        errors = check()
        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors))
            return 1
        print("Generated distributions and marketplaces match canonical sources.")
        return 0
    build(args.output_root, write_marketplaces=args.write_marketplaces)
    print(f"Generated {len(SKILLS)} Codex skills and {len(SKILLS)} Claude skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
