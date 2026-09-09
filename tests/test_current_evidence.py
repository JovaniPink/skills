"""Regression coverage carried forward from the older evidence PRs."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_catalog  # noqa: E402
from schema_validation import validate_instance  # noqa: E402

RECORD = "claude-account-repair-2026-09-08.md"


class CurrentEvidenceTests(unittest.TestCase):
    def check_docs(
        self, content: str, record: str = "Catalog version: 0.11.0\n"
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "docs"
            docs.mkdir()
            (docs / RECORD).write_text(record, encoding="utf-8")
            for name in ("manual-smoke-tests.md", "validation-evidence.md"):
                (docs / name).write_text(content, encoding="utf-8")
            errors: list[str] = []
            with patch.object(validate_catalog, "ROOT", root):
                validate_catalog.validate_current_client_evidence(errors)
            return errors

    def test_current_records_have_visible_entry_points(self) -> None:
        errors: list[str] = []
        validate_catalog.validate_current_client_evidence(errors)
        self.assertEqual([], errors)

    def test_missing_or_hidden_links_cannot_pass(self) -> None:
        link = f"[Current account evidence]({RECORD})"
        self.assertEqual([], self.check_docs("# Checks\n\n" + link))
        for hidden in (
            "",
            f"<!-- {link} -->",
            f"<!-- {link}",
            f"```markdown\n{link}\n```",
            f"~~~\n{link}\n~~~",
            f"```\n{link}",
            f"````\n```\n{link}\n```\n````",
            f"<pre>{link}</pre>",
            f"<div hidden>{link}</div>",
            f"`{link}`",
            f"``{link}``",
            f"    {link}",
            f"\t{link}",
            "\\" + link,
            "!" + link,
            "[Historical record](client-observations-v0.9.json)",
        ):
            with self.subTest(hidden=hidden):
                self.assertTrue(self.check_docs("# Checks\n\n" + hidden))

    def test_link_only_in_historical_section_cannot_pass(self) -> None:
        self.assertTrue(
            self.check_docs(f"# Checks\n\n## Historical\n\n[Record]({RECORD})")
        )

    def test_historical_records_remain_valid_in_their_own_section(self) -> None:
        self.assertEqual(
            [],
            self.check_docs(
                f"# Checks\n\n[Current]({RECORD})\n\n## History\n"
                "[Old matrix](client-observations.json)\n"
            ),
        )

    def test_missing_documents_and_wrong_record_version_fail(self) -> None:
        link = f"[Current]({RECORD})"
        self.assertTrue(self.check_docs(link, "Catalog version: 0.9.0\n"))
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(validate_catalog, "ROOT", Path(temporary)):
                errors: list[str] = []
                validate_catalog.validate_current_client_evidence(errors)
                self.assertTrue(errors)

    def test_shared_schema_accepts_all_historical_manifests(self) -> None:
        schema = json.loads((ROOT / "releases/manifest-schema.json").read_text())
        for path in (ROOT / "releases").glob("*/manifest.json"):
            with self.subTest(path=path.name):
                self.assertEqual(
                    [], validate_instance(json.loads(path.read_text()), schema)
                )

    def test_release_versions_reject_malformed_values(self) -> None:
        schema = json.loads((ROOT / "releases/manifest-schema.json").read_text())[
            "properties"
        ]["catalog_version"]
        for version in ("0.9.0", "0.11.0", "1.2.3-rc.1+build.2"):
            self.assertEqual([], validate_instance(version, schema), version)
        for version in ("v0.9.0", "01.2.3", "1.2", "1.2.3-01", "1.2.3+", "1.2.3\n"):
            self.assertTrue(validate_instance(version, schema), version)
