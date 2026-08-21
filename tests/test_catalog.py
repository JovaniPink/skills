from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_distributions import build, marketplace_documents  # noqa: E402
from cataloglib import EXPLICIT_SKILLS, SKILLS, read_skill_metadata, skills_by_plugin  # noqa: E402
from check_generated import check as check_generated  # noqa: E402
from check_public_boundary import _publishable_paths, scan as scan_public_boundary  # noqa: E402
from evaluate_gate_fixtures import evaluate as evaluate_gate_fixtures  # noqa: E402
from package_claude_ai import package  # noqa: E402
from schema_validation import validate_instance  # noqa: E402
from validate_catalog import (  # noqa: E402
    immutable_action_reference_errors,
    validate_all,
    validate_packages,
)


class CatalogTests(unittest.TestCase):
    def test_catalog_and_generated_distributions_validate(self) -> None:
        self.assertEqual([], validate_all(require_packages=True))
        self.assertEqual([], check_generated())
        self.assertEqual([], scan_public_boundary())

    def test_native_invocation_controls_match_canonical_metadata(self) -> None:
        for skill in SKILLS:
            canonical = read_skill_metadata(ROOT / "skills" / skill)
            plugin = canonical["plugin"]
            claude = read_skill_metadata(ROOT / "plugins" / "claude" / plugin / "skills" / skill)
            self.assertEqual("explicit" if skill in EXPLICIT_SKILLS else "implicit", canonical["invocation"])
            self.assertEqual("true" if skill in EXPLICIT_SKILLS else "false", claude["claude_explicit"])

    def test_clean_generation_and_packaging_in_temporary_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-catalog-test-") as temporary:
            temporary_root = Path(temporary)
            _, claude_plugins = build(temporary_root / "plugins", write_marketplaces=False)
            generated = {
                path.name
                for plugin in claude_plugins.values()
                for path in (plugin / "skills").iterdir()
            }
            self.assertEqual(set(SKILLS), generated)
            archives = package(temporary_root / "archives")
            self.assertEqual(len(SKILLS), len(archives))

    def test_generation_check_is_non_mutating_and_includes_marketplaces(self) -> None:
        before = subprocess.run(
            ["git", "status", "--short"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout
        self.assertEqual([], check_generated())
        after = subprocess.run(
            ["git", "status", "--short"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout
        self.assertEqual(before, after)
        codex, _ = marketplace_documents()
        self.assertEqual(set(skills_by_plugin()), {entry["name"] for entry in codex["plugins"]})
        for entry in codex["plugins"]:
            self.assertEqual(
                {"source": "local", "path": f"./plugins/codex/{entry['name']}"},
                entry["source"],
            )
            self.assertEqual({"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, entry["policy"])

    def test_schema_validation_enforces_types_enums_dates_and_unknown_fields(self) -> None:
        schema = json.loads((ROOT / "provenance" / "schema.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "provenance" / "catalog.json").read_text(encoding="utf-8"))
        broken = json.loads(json.dumps(catalog))
        broken["reviewed_on"] = "not-a-date"
        broken["entries"][0]["disposition"] = "adapt"
        broken["entries"][0]["reviewed_material"] = "SKILL.md"
        broken["entries"][0]["unexpected"] = True
        errors = validate_instance(broken, schema)
        self.assertTrue(any("valid date" in error for error in errors))
        self.assertTrue(any("must be one of" in error for error in errors))
        self.assertTrue(any("expected array" in error for error in errors))
        self.assertTrue(any("additional property" in error for error in errors))

    def test_client_observation_matrix_is_reconciled_and_terminal(self) -> None:
        paths = sorted(
            path for path in (ROOT / "docs").glob("client-observations*.json")
            if path.name != "client-observations-schema.json"
        )
        self.assertGreaterEqual(len(paths), 2)
        for path in paths:
            matrix = json.loads(path.read_text(encoding="utf-8"))
            records = matrix["records"]
            self.assertEqual(matrix["summary"]["total"], len(records))
            self.assertEqual(len(records), len({record["case_id"] for record in records}))
            self.assertNotIn("not_run", {record["result"] for record in records})
            self.assertEqual(
                {"Codex CLI", "Codex Desktop", "Claude Code CLI", "Claude Code Desktop", "Claude.ai"},
                {record["surface"] for record in records},
            )

    def test_boundary_scan_covers_publishable_root_and_local_denylist(self) -> None:
        publishable = {path.relative_to(ROOT).as_posix() for path in _publishable_paths(ROOT)}
        for expected in ("README.md", ".github/workflows/validate.yml", "scripts/check_public_boundary.py"):
            self.assertIn(expected, publishable)
        with tempfile.TemporaryDirectory(prefix="boundary-regression-") as temporary:
            temporary_root = Path(temporary)
            candidate = temporary_root / "candidate.md"
            denylist = temporary_root / "denylist.txt"
            candidate.write_text("synthetic confidential canary\n", encoding="utf-8")
            denylist.write_text("confidential canary\n", encoding="utf-8")
            errors = scan_public_boundary([candidate], denylist_path=denylist, include_packages=False)
            self.assertEqual(1, len(errors))
            self.assertIn("local denylist", errors[0])

    def test_boundary_scan_rejects_non_ascii_and_non_us_english(self) -> None:
        with tempfile.TemporaryDirectory(prefix="language-boundary-") as temporary:
            candidate = Path(temporary) / "candidate.md"
            non_us_spelling = "behav" + "iour"
            candidate.write_text(f"plain{chr(0x2014)}text with {non_us_spelling}\n", encoding="utf-8")
            errors = scan_public_boundary([candidate], include_packages=False)
            self.assertTrue(any("non-ASCII character" in error for error in errors))
            self.assertTrue(any("non-US English spelling" in error for error in errors))

    def test_claude_archives_are_reproducible(self) -> None:
        with tempfile.TemporaryDirectory(prefix="package-determinism-") as temporary:
            temporary_root = Path(temporary)
            first = package(temporary_root / "first")
            second = package(temporary_root / "second")
            first_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in first]
            second_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in second]
            self.assertEqual(first_hashes, second_hashes)

    def test_stack_reference_covers_declared_languages(self) -> None:
        text = (ROOT / "skills" / "cross-stack-quality-gates" / "references" / "gate-discovery.md").read_text(encoding="utf-8")
        for stack in ("Go", "Python", "Swift", "TypeScript", "JavaScript", "SQL", "Terraform"):
            self.assertIn(stack, text)

    def test_cross_stack_fixtures_do_not_assume_a_universal_gate(self) -> None:
        self.assertEqual([], evaluate_gate_fixtures())

    def test_archives_have_valid_layout(self) -> None:
        errors: list[str] = []
        validate_packages(errors)
        self.assertEqual([], errors)

    def test_workflow_actions_require_immutable_revisions(self) -> None:
        mutable = "steps:\n  - uses: actions/checkout@v7\n"
        local = "steps:\n  - uses: ./local-action\n"
        self.assertEqual(
            ["fixture.yml: action reference must use a 40-character commit SHA: actions/checkout@v7"],
            immutable_action_reference_errors(mutable, "fixture.yml"),
        )
        self.assertEqual([], immutable_action_reference_errors(local, "fixture.yml"))


if __name__ == "__main__":
    unittest.main()
