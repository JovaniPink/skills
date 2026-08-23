#!/usr/bin/env python3
"""Reject external repository coupling from maintained and generated artifacts."""

from __future__ import annotations

import json
import re
import subprocess
import zipfile
from pathlib import Path
from urllib.parse import urlparse

from cataloglib import ROOT


REPOSITORY_HOSTS = "(?:" + "|".join(
    (
        "github" + r"\.com",
        "gitlab" + r"\.com",
        "bitbucket" + r"\.org",
        "codeberg" + r"\.org",
    )
) + ")"
REPOSITORY_URL = re.compile(
    rf"https?://(?:www\.)?(?P<host>{REPOSITORY_HOSTS})/(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)",
    re.IGNORECASE,
)
MARKETPLACE_COMMAND = re.compile(
    r"\b(?:marketplace|plugin|skills?)\s+(?:add|install)\s+(?P<owner>[A-Za-z0-9][A-Za-z0-9_.-]*)/(?P<repo>[A-Za-z0-9_.-]+)",
    re.IGNORECASE,
)
PACKAGE_MARKETPLACE_ID = re.compile(
    r"\bplugin\s+(?:add|install)\s+(?P<plugin>[A-Za-z0-9][A-Za-z0-9_.-]*)@(?P<marketplace>[A-Za-z0-9][A-Za-z0-9_.-]*)",
    re.IGNORECASE,
)
SOURCE_ATTRIBUTION = re.compile(
    r"\b(?:adapted|copied|derived) from\b.{0,80}\b(?:repository|skill catalog)\b",
    re.IGNORECASE,
)
CAPABILITY_MAPPING_KEY = "public_" + "mapping"
PRIMARY_AUTHORITY_HOSTS = frozenset(
    {
        "agentskills.io",
        "developer.hashicorp.com",
        "developer.salesforce.com",
        "docs.oracle.com",
        "docs.github.com",
        "docs.python.org",
        "docs.spring.io",
        "drupal.org",
        "experienceleague.adobe.com",
        "git-scm.com",
        "go.dev",
        "learn.chatgpt.com",
        "learn.microsoft.com",
        "opentelemetry.io",
        "owasp.org",
        "postgresql.org",
        "rfc-editor.org",
        "resources.docs.salesforce.com",
        "slsa.dev",
        "sre.google",
        "swift.org",
        "trailhead.salesforce.com",
        "typescriptlang.org",
        "w3.org",
        "php.net",
    }
)


def _owned(owner: str) -> bool:
    return owner.casefold() == "jovanipink"


def _ci_action_exception(label: str, host: str, owner: str) -> bool:
    return (
        label == "provenance/ci-actions.json"
        and host.casefold() == "github.com"
        and owner.casefold() == "actions"
    )


def scan_text(label: str, text: str) -> list[str]:
    """Scan one text surface while preserving narrow path-based exceptions."""

    errors: list[str] = []
    for match in REPOSITORY_URL.finditer(text):
        host = match.group("host").casefold()
        owner = match.group("owner")
        if _owned(owner) or _ci_action_exception(label, host, owner):
            continue
        line = text.count("\n", 0, match.start()) + 1
        errors.append(f"{label}:{line}: external repository URL is not permitted")

    for match in MARKETPLACE_COMMAND.finditer(text):
        if _owned(match.group("owner")):
            continue
        line = text.count("\n", 0, match.start()) + 1
        errors.append(f"{label}:{line}: external marketplace or install identifier is not permitted")

    for match in PACKAGE_MARKETPLACE_ID.finditer(text):
        plugin = match.group("plugin").casefold()
        marketplace = match.group("marketplace").casefold()
        if plugin.startswith("jovanipink-") and marketplace == "jovanipink-skills":
            continue
        line = text.count("\n", 0, match.start()) + 1
        errors.append(f"{label}:{line}: external package marketplace identifier is not permitted")

    for match in SOURCE_ATTRIBUTION.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        errors.append(f"{label}:{line}: source-specific implementation attribution is not permitted")

    for match in re.finditer(re.escape(CAPABILITY_MAPPING_KEY), text, re.IGNORECASE):
        line = text.count("\n", 0, match.start()) + 1
        errors.append(f"{label}:{line}: repository-to-repository capability mapping is not permitted")
    return errors


def provenance_source_errors() -> list[str]:
    """Require catalog behavior provenance to use an approved primary authority."""

    path = ROOT / "provenance" / "catalog.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for entry in document.get("entries", []):
        if not isinstance(entry, dict):
            continue
        skill = str(entry.get("skill", "unknown"))
        source_url = str(entry.get("source_url", ""))
        parsed = urlparse(source_url)
        host = (parsed.hostname or "").casefold()
        if host.startswith("www."):
            host = host[4:]
        if host not in PRIMARY_AUTHORITY_HOSTS:
            errors.append(f"provenance/catalog.json: {skill} source is not an approved primary authority: {source_url}")
        if "/blog/" in parsed.path.casefold():
            errors.append(f"provenance/catalog.json: {skill} uses a blog path instead of a primary authority")
    return errors


def ci_action_provenance_errors() -> list[str]:
    """Keep repository-link exceptions limited to pinned CI Action evidence."""

    path = ROOT / "provenance" / "ci-actions.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for action in document.get("actions", []):
        if not isinstance(action, dict):
            continue
        name = str(action.get("name", ""))
        source_url = str(action.get("source_url", ""))
        revision = str(action.get("pinned_revision", ""))
        expected_url = "https://" + "github.com/" + name
        if not name.startswith("actions/") or source_url != expected_url:
            errors.append(f"provenance/ci-actions.json: unsupported repository-link exception for {name or 'unknown'}")
        if re.fullmatch(r"[0-9a-f]{40}", revision) is None:
            errors.append(f"provenance/ci-actions.json: {name or 'unknown'} is not pinned to an immutable revision")
    return errors


def _content_paths() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return sorted(path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    return sorted(ROOT / item.decode("utf-8") for item in result.stdout.split(b"\0") if item)


def check(include_packages: bool = True) -> list[str]:
    errors: list[str] = []
    for path in _content_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        errors.extend(scan_text(path.relative_to(ROOT).as_posix(), text))

    if include_packages:
        for archive_path in sorted((ROOT / "dist" / "claude-ai").glob("*.zip")):
            try:
                with zipfile.ZipFile(archive_path) as archive:
                    for member in sorted(archive.namelist()):
                        try:
                            text = archive.read(member).decode("utf-8")
                        except (KeyError, UnicodeDecodeError):
                            continue
                        errors.extend(scan_text(f"{archive_path.relative_to(ROOT)}!{member}", text))
            except (OSError, zipfile.BadZipFile) as error:
                errors.append(f"{archive_path.relative_to(ROOT)}: invalid ZIP: {error}")
    errors.extend(provenance_source_errors())
    errors.extend(ci_action_provenance_errors())
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Repository-independence validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
