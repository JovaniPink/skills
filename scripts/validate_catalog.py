#!/usr/bin/env python3
"""Validate canonical skills, adapters, catalogs, references, and packages."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath

from cataloglib import (
    CATALOG_NAME,
    PLUGIN_SPECS,
    ROOT,
    SKILLS,
    VERSION,
    read_skill_metadata,
    skills_by_plugin,
    split_frontmatter,
)
from schema_validation import validate_instance


REFERENCE_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ALLOWED_CANONICAL_TOP_KEYS = {"name", "description", "license", "metadata"}
ALLOWED_RISK_CLASSES = {"read-only", "bounded-execution", "network-read", "external-write", "trust-decision"}
ACTION_USE = re.compile(r"(?m)^\s*-\s*uses:\s*([^#\s]+)")
IMMUTABLE_REVISION = re.compile(r"[0-9a-fA-F]{40}")


def _load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {error}")
        return None


def _validate_json_schema(document_path: Path, schema_path: Path, errors: list[str]) -> object | None:
    document = _load_json(document_path, errors)
    schema = _load_json(schema_path, errors)
    if document is None or schema is None:
        return document
    for error in validate_instance(document, schema):
        errors.append(f"{document_path.relative_to(ROOT)}: {error}")
    return document


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


def immutable_action_reference_errors(text: str, label: str) -> list[str]:
    """Reject mutable third-party GitHub Action references without parsing YAML."""

    errors: list[str] = []
    for reference in ACTION_USE.findall(text):
        if reference.startswith(("./", "docker://")):
            continue
        if "@" not in reference:
            errors.append(f"{label}: action reference has no revision: {reference}")
            continue
        _, revision = reference.rsplit("@", 1)
        if IMMUTABLE_REVISION.fullmatch(revision) is None:
            errors.append(f"{label}: action reference must use a 40-character commit SHA: {reference}")
    return errors


def validate_workflows(errors: list[str]) -> None:
    workflows_root = ROOT / ".github" / "workflows"
    if not workflows_root.is_dir():
        return
    for path in sorted(workflows_root.iterdir()):
        if path.suffix.lower() not in {".yaml", ".yml"} or not path.is_file():
            continue
        errors.extend(
            immutable_action_reference_errors(
                path.read_text(encoding="utf-8"),
                path.relative_to(ROOT).as_posix(),
            )
        )


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
        expected_invocation = metadata["invocation"]
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
        if metadata["plugin"] not in PLUGIN_SPECS:
            errors.append(f"skills/{skill}/SKILL.md: unsupported plugin {metadata['plugin']!r}")
        if metadata["invocation"] not in {"implicit", "explicit"}:
            errors.append(f"skills/{skill}/SKILL.md: invocation must be implicit or explicit")
        if not 1 <= len(metadata["description"]) <= 1024:
            errors.append(f"skills/{skill}/SKILL.md: description must be 1 to 1024 characters")
        if metadata["claude_explicit"] != "false":
            errors.append(f"skills/{skill}/SKILL.md: Claude controls belong only in generated output")
        if metadata["risk_class"] not in ALLOWED_RISK_CLASSES:
            errors.append(
                f"skills/{skill}/SKILL.md: risk_class must be one of {sorted(ALLOWED_RISK_CLASSES)}, "
                f"found {metadata['risk_class']!r}"
            )
        if "TODO" in text or "TBD" in text:
            errors.append(f"skills/{skill}/SKILL.md: unresolved placeholder")
        if not body.lstrip().startswith("# "):
            errors.append(f"skills/{skill}/SKILL.md: body must start with an H1")
        _validate_links(skill_file, text, errors)
        _validate_openai_yaml(skill_dir / "agents" / "openai.yaml", expected_invocation == "explicit", skill, errors)

        for item in skill_dir.rglob("*"):
            if item.is_dir() or item == skill_file or item == skill_dir / "agents" / "openai.yaml":
                continue
            if "references" not in item.parts or item.suffix.lower() not in {".md", ".json", ".txt"}:
                errors.append(f"{item.relative_to(ROOT)}: catalog permits only focused reference resources")
            elif item.is_file():
                _validate_links(item, item.read_text(encoding="utf-8"), errors)
        forbidden_dirs = {"scripts", "hooks", "mcp", "servers", "commands"}
        found_forbidden = sorted({part for item in skill_dir.rglob("*") for part in item.parts if part in forbidden_dirs})
        if found_forbidden:
            errors.append(f"skills/{skill}: forbidden skill directories: {found_forbidden}")


def validate_evals(errors: list[str]) -> None:
    document = _validate_json_schema(
        ROOT / "evals" / "cases.json",
        ROOT / "evals" / "schema.json",
        errors,
    )
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
        expected_invocation = read_skill_metadata(ROOT / "skills" / skill)["invocation"]
        if record.get("invocation") != expected_invocation:
            errors.append(f"evals/cases.json: {skill} invocation must be {expected_invocation}")
        if read_skill_metadata(ROOT / "skills" / skill)["plugin"] != "jovanipink-skills":
            rubric = record.get("output_rubric")
            baseline = record.get("baseline_comparison")
            if not isinstance(rubric, list) or len(rubric) < 3:
                errors.append(f"evals/cases.json: {skill} requires an output-quality rubric")
            if not isinstance(baseline, dict) or baseline.get("status") == "not_run":
                errors.append(f"evals/cases.json: {skill} requires a terminal baseline comparison")
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
        if expected_invocation == "explicit":
            for case in record.get("positive", []):
                prompt = case.get("prompt", "").lower()
                if f"${skill}" not in prompt and f"invoke {skill}" not in prompt and f"with ${skill}" not in prompt:
                    errors.append(f"evals/cases.json: {case.get('id')} must explicitly invoke {skill}")


def validate_provenance(errors: list[str]) -> None:
    document = _validate_json_schema(
        ROOT / "provenance" / "catalog.json",
        ROOT / "provenance" / "schema.json",
        errors,
    )
    if not isinstance(document, dict) or not isinstance(document.get("entries"), list):
        return
    entries = document["entries"]
    names = [entry.get("skill") for entry in entries if isinstance(entry, dict)]
    if sorted(names) != list(SKILLS):
        errors.append(f"provenance/catalog.json: expected one entry for every skill, found {sorted(names)}")
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("provenance/catalog.json: malformed entry")
            continue
        if entry.get("implementation_method") in {"adapted", "vendored"}:
            revision = str(entry.get("pinned_revision", ""))
            if not re.fullmatch(r"[0-9a-f]{40}", revision):
                errors.append(f"provenance/catalog.json: {entry.get('skill')} requires a 40-character pinned revision")
        skill = entry.get("skill")
        if skill in SKILLS:
            metadata = read_skill_metadata(ROOT / "skills" / skill)
            if entry.get("disposition") != "covered":
                errors.append(f"provenance/catalog.json: shipped skill {skill} disposition must be 'covered'")
            if metadata["provenance"] != entry.get("implementation_method"):
                errors.append(
                    f"provenance/catalog.json: {skill} implementation method {entry.get('implementation_method')!r} "
                    f"does not match SKILL.md metadata {metadata['provenance']!r}"
                )


def validate_auxiliary_records(errors: list[str]) -> None:
    inventory = _validate_json_schema(
        ROOT / "provenance" / "inventory-summary.json",
        ROOT / "provenance" / "inventory-summary-schema.json",
        errors,
    )
    if isinstance(inventory, dict):
        total = inventory.get("total_records")
        dispositions = inventory.get("dispositions")
        domains = inventory.get("domains")
        if isinstance(dispositions, list):
            disposition_total = sum(
                item.get("count", 0) for item in dispositions if isinstance(item, dict) and isinstance(item.get("count"), int)
            )
            if disposition_total != total:
                errors.append("provenance/inventory-summary.json: disposition counts do not reconcile")
        if isinstance(domains, list):
            domain_total = sum(
                item.get("count", 0) for item in domains if isinstance(item, dict) and isinstance(item.get("count"), int)
            )
            if domain_total != total:
                errors.append("provenance/inventory-summary.json: domain counts do not reconcile")

    roadmap = _validate_json_schema(
        ROOT / "incubator" / "roadmap.json",
        ROOT / "incubator" / "roadmap-schema.json",
        errors,
    )
    if isinstance(roadmap, dict) and isinstance(roadmap.get("tracks"), list):
        seen: set[str] = set()
        for track in roadmap["tracks"]:
            if not isinstance(track, dict) or not isinstance(track.get("skills"), list):
                continue
            for skill in track["skills"]:
                if skill in seen:
                    errors.append(f"incubator/roadmap.json: duplicate skill {skill}")
                seen.add(skill)

    observation_paths = sorted(
        path for path in (ROOT / "docs").glob("client-observations*.json")
        if path.name != "client-observations-schema.json"
    )
    for observation_path in observation_paths:
      observations = _validate_json_schema(
        observation_path,
        ROOT / "docs" / "client-observations-schema.json",
        errors,
      )
      if isinstance(observations, dict) and isinstance(observations.get("records"), list):
        records = observations["records"]
        ids = [record.get("case_id") for record in records if isinstance(record, dict)]
        if len(ids) != len(set(ids)):
            errors.append(f"{observation_path.relative_to(ROOT)}: case IDs must be unique")
        surfaces = {record.get("surface") for record in records if isinstance(record, dict)}
        expected_surfaces = {"Codex CLI", "Codex Desktop", "Claude Code CLI", "Claude Code Desktop", "Claude.ai"}
        if surfaces != expected_surfaces:
            errors.append(f"{observation_path.relative_to(ROOT)}: expected surfaces {sorted(expected_surfaces)}, found {sorted(surfaces)}")
        source_commit = observations.get("tested_source_commit")
        if any(record.get("source_commit") != source_commit for record in records if isinstance(record, dict)):
            errors.append(f"{observation_path.relative_to(ROOT)}: every row must reference the tested source commit")
        if any(record.get("result") == "not_run" for record in records if isinstance(record, dict)):
            errors.append(f"{observation_path.relative_to(ROOT)}: every manual row must have an observed terminal state")
        actual_summary = {status: 0 for status in ("pass", "fail", "blocked", "not_supported", "not_run")}
        for record in records:
            if isinstance(record, dict) and record.get("result") in actual_summary:
                actual_summary[record["result"]] += 1
        actual_summary["total"] = len(records)
        if observations.get("summary") != actual_summary:
            errors.append(f"{observation_path.relative_to(ROOT)}: summary counts do not reconcile with records")


def validate_generated_adapters(errors: list[str]) -> None:
    for skill in SKILLS:
        metadata = read_skill_metadata(ROOT / "skills" / skill)
        plugin = metadata["plugin"]
        explicit = metadata["invocation"] == "explicit"
        codex_dir = ROOT / "plugins" / "codex" / plugin / "skills" / skill
        claude_dir = ROOT / "plugins" / "claude" / plugin / "skills" / skill
        for client, path in (("Codex", codex_dir), ("Claude", claude_dir)):
            if not (path / "SKILL.md").is_file():
                errors.append(f"{client} distribution missing {skill}")
        if not (codex_dir / "agents" / "openai.yaml").is_file():
            errors.append(f"Codex distribution missing interface for {skill}")
        else:
            codex_interface = (codex_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
            if f"${plugin}:{skill}" not in codex_interface:
                errors.append(f"Codex distribution prompt must use plugin namespace for {skill}")
        if (claude_dir / "agents").exists():
            errors.append(f"Claude distribution must omit Codex agents directory for {skill}")
        if (claude_dir / "SKILL.md").is_file():
            metadata = read_skill_metadata(claude_dir)
            expected = "true" if explicit else "false"
            if metadata["claude_explicit"] != expected:
                errors.append(f"Claude distribution explicit control for {skill} must be {expected}")

    for plugin in skills_by_plugin():
        manifests = (
            ROOT / "plugins" / "codex" / plugin / ".codex-plugin" / "plugin.json",
            ROOT / "plugins" / "claude" / plugin / ".claude-plugin" / "plugin.json",
        )
        for manifest in manifests:
            value = _load_json(manifest, errors)
            if isinstance(value, dict):
                for key, expected in (("name", plugin), ("version", VERSION), ("license", "MIT")):
                    if value.get(key) != expected:
                        errors.append(f"{manifest.relative_to(ROOT)}: {key} must be {expected!r}")
        codex_manifest = _load_json(manifests[0], errors)
        if isinstance(codex_manifest, dict):
            interface = codex_manifest.get("interface")
            prompts = interface.get("defaultPrompt") if isinstance(interface, dict) else None
            if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or not all(isinstance(item, str) for item in prompts):
                errors.append(f"{manifests[0].relative_to(ROOT)}: interface.defaultPrompt must contain one to three strings")


def validate_marketplaces(errors: list[str]) -> None:
    codex_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    codex = _load_json(codex_path, errors)
    if isinstance(codex, dict):
        plugins = codex.get("plugins")
        interface = codex.get("interface")
        if codex.get("name") != CATALOG_NAME or not isinstance(interface, dict) or not interface.get("displayName"):
            errors.append(f"{codex_path.relative_to(ROOT)}: missing marketplace identity or interface")
        if not isinstance(plugins, list) or len(plugins) != len(skills_by_plugin()):
            errors.append(f"{codex_path.relative_to(ROOT)}: malformed plugin marketplace")
        else:
            for entry in plugins:
                if not isinstance(entry, dict):
                    errors.append(f"{codex_path.relative_to(ROOT)}: malformed Codex plugin entry")
                    continue
                plugin = entry.get("name")
                expected_source = {"source": "local", "path": f"./plugins/codex/{plugin}"}
                expected_policy = {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
                if set(entry) != {"name", "source", "policy", "category"}:
                    errors.append(f"{codex_path.relative_to(ROOT)}: Codex plugin entry has unsupported or missing fields")
                if plugin not in skills_by_plugin() or entry.get("source") != expected_source:
                    errors.append(f"{codex_path.relative_to(ROOT)}: Codex plugin name or object source is incorrect")
                if entry.get("policy") != expected_policy or not isinstance(entry.get("category"), str):
                    errors.append(f"{codex_path.relative_to(ROOT)}: Codex plugin policy or category is incorrect")

    claude_path = ROOT / ".claude-plugin" / "marketplace.json"
    claude = _load_json(claude_path, errors)
    if isinstance(claude, dict):
        plugins = claude.get("plugins")
        if claude.get("name") != CATALOG_NAME or not isinstance(plugins, list) or len(plugins) != len(skills_by_plugin()):
            errors.append(f"{claude_path.relative_to(ROOT)}: malformed plugin marketplace")
        else:
            for entry in plugins:
                if not isinstance(entry, dict):
                    errors.append(f"{claude_path.relative_to(ROOT)}: malformed Claude plugin entry")
                    continue
                plugin = entry.get("name")
                if plugin not in skills_by_plugin() or entry.get("version") != VERSION or entry.get("source") != f"./plugins/claude/{plugin}":
                    errors.append(f"{claude_path.relative_to(ROOT)}: Claude plugin name, version, or source is incorrect")


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
    validate_workflows(errors)
    validate_canonical(errors)
    validate_evals(errors)
    validate_provenance(errors)
    validate_auxiliary_records(errors)
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
