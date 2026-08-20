#!/usr/bin/env python3
"""Validate canonical skills, adapters, catalogs, references, and packages."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

from cataloglib import EXPLICIT_SKILLS, PLUGIN_NAME, ROOT, SKILLS, VERSION, read_skill_metadata, split_frontmatter


REFERENCE_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ALLOWED_CANONICAL_TOP_KEYS = {"name", "description", "license", "metadata"}


def _load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {error}")
        return None


def _validate_openai_yaml(path: Path, explicit: bool, skill: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"{path.relative_to(ROOT)}: missing Codex interface")
        return
    text = path.read_text(encoding="utf-8")
    prompt = re.search(r"(?m)^\s{2}default_prompt:\s*[\"']?(.+?)[\"']?\s*$", text)
    if not prompt or f"${skill}" not in prompt.group(1):
        errors.append(f"{path.relative_to(ROOT)}: default_prompt must mention ${skill}")
    policy = re.search(r"(?m)^\s{2}allow_implicit_invocation:\s*(true|false)\s*$", text)
    expected = "false" if explicit else "true"
    if not policy or policy.group(1) != expected:
        errors.append(f"{path.relative_to(ROOT)}: implicit policy must be {expected}")
    short = re.search(r"(?m)^\s{2}short_description:\s*[\"']?(.+?)[\"']?\s*$", text)
    if not short or len(short.group(1).strip("\"'")) > 80:
        errors.append(f"{path.relative_to(ROOT)}: short_description is missing or over 80 characters")


def _validate_links(path: Path, text: str, errors: list[str]) -> None:
    for raw_target in REFERENCE_LINK.findall(text):
        target = raw_target.strip().strip("<>").split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        if target.startswith("/"):
            errors.append(f"{path.relative_to(ROOT)}: absolute link is not portable: {target}")
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken local link: {target}")


def validate_canonical(errors: list[str]) -> None:
    skills_root = ROOT / "skills"
    actual = sorted(path.name for path in skills_root.iterdir() if path.is_dir()) if skills_root.is_dir() else []
    if actual != list(SKILLS):
        errors.append(f"skills/: expected {list(SKILLS)}, found {actual}")
    for skill in SKILLS:
        skill_dir = skills_root / skill
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"skills/{skill}/SKILL.md: missing")
            continue
        text = skill_file.read_text(encoding="utf-8")
        try:
            frontmatter, body = split_frontmatter(text)
            metadata = read_skill_metadata(skill_dir)
        except ValueError as error:
            errors.append(f"skills/{skill}/SKILL.md: {error}")
            continue
        top_keys = {match.group(1) for match in re.finditer(r"(?m)^([A-Za-z][A-Za-z0-9_.-]*):", frontmatter)}
        unexpected = sorted(top_keys - ALLOWED_CANONICAL_TOP_KEYS)
        if unexpected:
            errors.append(f"skills/{skill}/SKILL.md: nonportable canonical keys: {unexpected}")
        expected_invocation = "explicit" if skill in EXPLICIT_SKILLS else "implicit"
        expected = {
            "name": skill,
            "license": "MIT",
            "author": "Jovani Pink",
            "version": VERSION,
            "invocation": expected_invocation,
        }
        for key, value in expected.items():
            if metadata[key] != value:
                errors.append(f"skills/{skill}/SKILL.md: {key} must be {value!r}, found {metadata[key]!r}")
        if not 1 <= len(metadata["description"]) <= 1024:
            errors.append(f"skills/{skill}/SKILL.md: description must be 1 to 1024 characters")
        if metadata["claude_explicit"] != "false":
            errors.append(f"skills/{skill}/SKILL.md: Claude controls belong only in generated output")
        if "TODO" in text or "TBD" in text:
            errors.append(f"skills/{skill}/SKILL.md: unresolved placeholder")
        if not body.lstrip().startswith("# "):
            errors.append(f"skills/{skill}/SKILL.md: body must start with an H1")
        _validate_links(skill_file, text, errors)
        _validate_openai_yaml(skill_dir / "agents" / "openai.yaml", skill in EXPLICIT_SKILLS, skill, errors)

        for item in skill_dir.rglob("*"):
            if item.is_dir() or item == skill_file or item == skill_dir / "agents" / "openai.yaml":
                continue
            if "references" not in item.parts or item.suffix.lower() not in {".md", ".json", ".txt"}:
                errors.append(f"{item.relative_to(ROOT)}: v0.1 permits only focused reference resources")
            elif item.is_file():
                _validate_links(item, item.read_text(encoding="utf-8"), errors)
        forbidden_dirs = {"scripts", "hooks", "mcp", "servers", "commands"}
        found_forbidden = sorted({part for item in skill_dir.rglob("*") for part in item.parts if part in forbidden_dirs})
        if found_forbidden:
            errors.append(f"skills/{skill}: forbidden v0.1 directories: {found_forbidden}")


def validate_evals(errors: list[str]) -> None:
    document = _load_json(ROOT / "evals" / "cases.json", errors)
    if not isinstance(document, dict) or not isinstance(document.get("skills"), list):
        return
    records = document["skills"]
    names = [record.get("skill") for record in records if isinstance(record, dict)]
    if sorted(names) != list(SKILLS):
        errors.append(f"evals/cases.json: expected one record for every skill, found {sorted(names)}")
    ids: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("skill"), str):
            errors.append("evals/cases.json: malformed skill record")
            continue
        skill = record["skill"]
        expected_invocation = "explicit" if skill in EXPLICIT_SKILLS else "implicit"
        if record.get("invocation") != expected_invocation:
            errors.append(f"evals/cases.json: {skill} invocation must be {expected_invocation}")
        for category, minimum in (("positive", 3), ("near_miss", 3), ("safety", 1)):
            cases = record.get(category)
            if not isinstance(cases, list) or len(cases) < minimum:
                errors.append(f"evals/cases.json: {skill} requires at least {minimum} {category} cases")
                continue
            for case in cases:
                if not isinstance(case, dict) or not case.get("id") or not case.get("prompt"):
                    errors.append(f"evals/cases.json: {skill} has malformed {category} case")
                    continue
                case_id = case["id"]
                if case_id in ids:
                    errors.append(f"evals/cases.json: duplicate case id {case_id}")
                ids.add(case_id)
                if category == "safety" and not case.get("expected"):
                    errors.append(f"evals/cases.json: {case_id} requires an expected safety boundary")
        if skill in EXPLICIT_SKILLS:
            for case in record.get("positive", []):
                prompt = case.get("prompt", "").lower()
                if f"${skill}" not in prompt and f"invoke {skill}" not in prompt and f"with ${skill}" not in prompt:
                    errors.append(f"evals/cases.json: {case.get('id')} must explicitly invoke {skill}")


def validate_provenance(errors: list[str]) -> None:
    document = _load_json(ROOT / "provenance" / "catalog.json", errors)
    if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
        return
    entries = document["entries"]
    names = [entry.get("skill") for entry in entries if isinstance(entry, dict)]
    if sorted(names) != list(SKILLS):
        errors.append(f"provenance/catalog.json: expected one entry for every skill, found {sorted(names)}")
    required = {
        "skill", "disposition", "source_url", "upstream_license", "pinned_revision",
        "reviewed_material", "local_changes", "security_review", "rereview_triggers", "revocation",
    }
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("provenance/catalog.json: malformed entry")
            continue
        missing = sorted(required - set(entry))
        if missing:
            errors.append(f"provenance/catalog.json: {entry.get('skill', '<unknown>')} missing {missing}")
        if entry.get("disposition") in {"adapted", "vendored"}:
            revision = str(entry.get("pinned_revision", ""))
            if not re.fullmatch(r"[0-9a-f]{40}", revision):
                errors.append(f"provenance/catalog.json: {entry.get('skill')} requires a 40-character pinned revision")
        skill = entry.get("skill")
        if skill in SKILLS:
            metadata = read_skill_metadata(ROOT / "skills" / skill)
            if metadata["provenance"] != entry.get("disposition"):
                errors.append(
                    f"provenance/catalog.json: {skill} disposition {entry.get('disposition')!r} "
                    f"does not match SKILL.md metadata {metadata['provenance']!r}"
                )


def validate_generated_adapters(errors: list[str]) -> None:
    for skill in SKILLS:
        codex_dir = ROOT / "plugins" / "codex" / PLUGIN_NAME / "skills" / skill
        claude_dir = ROOT / "plugins" / "claude" / PLUGIN_NAME / "skills" / skill
        for client, path in (("Codex", codex_dir), ("Claude", claude_dir)):
            if not (path / "SKILL.md").is_file():
                errors.append(f"{client} distribution missing {skill}")
        if not (codex_dir / "agents" / "openai.yaml").is_file():
            errors.append(f"Codex distribution missing interface for {skill}")
        else:
            codex_interface = (codex_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            if f"${PLUGIN_NAME}:{skill}" not in codex_interface:
                errors.append(f"Codex distribution prompt must use plugin namespace for {skill}")
        if (claude_dir / "agents").exists():
            errors.append(f"Claude distribution must omit Codex agents directory for {skill}")
        if (claude_dir / "SKILL.md").is_file():
            metadata = read_skill_metadata(claude_dir)
            expected = "true" if skill in EXPLICIT_SKILLS else "false"
            if metadata["claude_explicit"] != expected:
                errors.append(f"Claude distribution explicit control for {skill} must be {expected}")

    manifests = (
        ROOT / "plugins" / "codex" / PLUGIN_NAME / ".codex-plugin" / "plugin.json",
        ROOT / "plugins" / "claude" / PLUGIN_NAME / ".claude-plugin" / "plugin.json",
    )
    for manifest in manifests:
        value = _load_json(manifest, errors)
        if isinstance(value, dict):
            for key, expected in (("name", PLUGIN_NAME), ("version", VERSION), ("license", "MIT")):
                if value.get(key) != expected:
                    errors.append(f"{manifest.relative_to(ROOT)}: {key} must be {expected!r}")


def validate_marketplaces(errors: list[str]) -> None:
    expected = (
        (ROOT / ".agents" / "plugins" / "marketplace.json", "./plugins/codex/jovanipink-skills"),
        (ROOT / ".claude-plugin" / "marketplace.json", "./plugins/claude/jovanipink-skills"),
    )
    for path, source in expected:
        value = _load_json(path, errors)
        if not isinstance(value, dict):
            continue
        plugins = value.get("plugins")
        if value.get("name") != PLUGIN_NAME or not isinstance(plugins, list) or len(plugins) != 1:
            errors.append(f"{path.relative_to(ROOT)}: malformed single-plugin marketplace")
            continue
        plugin = plugins[0]
        if plugin.get("name") != PLUGIN_NAME or plugin.get("version") != VERSION or plugin.get("source") != source:
            errors.append(f"{path.relative_to(ROOT)}: plugin name, version, or source is incorrect")


def validate_packages(errors: list[str]) -> None:
    package_root = ROOT / "dist" / "claude-ai"
    expected_names = {f"{skill}-{VERSION}.zip" for skill in SKILLS}
    actual_names = {path.name for path in package_root.glob("*.zip")} if package_root.is_dir() else set()
    if actual_names != expected_names:
        errors.append(f"dist/claude-ai: expected archives {sorted(expected_names)}, found {sorted(actual_names)}")
    checksum_path = package_root / "SHA256SUMS"
    checksums: dict[str, str] = {}
    if checksum_path.is_file():
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                checksums[parts[1].strip()] = parts[0]
    else:
        errors.append("dist/claude-ai/SHA256SUMS: missing")
    for skill in SKILLS:
        archive_path = package_root / f"{skill}-{VERSION}.zip"
        if not archive_path.is_file():
            continue
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        if checksums.get(archive_path.name) != digest:
            errors.append(f"dist/claude-ai/SHA256SUMS: digest mismatch for {archive_path.name}")
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            if f"{skill}/SKILL.md" not in names:
                errors.append(f"{archive_path.name}: missing nested {skill}/SKILL.md")
            for name in names:
                parts = PurePosixPath(name).parts
                if not parts or parts[0] != skill or ".." in parts or name.startswith("/"):
                    errors.append(f"{archive_path.name}: unsafe or incorrectly nested entry {name}")
                if "/agents/" in f"/{name}":
                    errors.append(f"{archive_path.name}: Claude.ai package contains Codex interface {name}")


def validate_all(require_packages: bool = True) -> list[str]:
    errors: list[str] = []
    validate_canonical(errors)
    validate_evals(errors)
    validate_provenance(errors)
    validate_generated_adapters(errors)
    validate_marketplaces(errors)
    if require_packages:
        validate_packages(errors)
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"Catalog validation passed for {len(SKILLS)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
