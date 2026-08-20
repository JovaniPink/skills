from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_distributions import build  # noqa: E402
from cataloglib import EXPLICIT_SKILLS, PLUGIN_NAME, SKILLS, read_skill_metadata  # noqa: E402
from check_generated import check as check_generated  # noqa: E402
from check_public_boundary import scan as scan_public_boundary  # noqa: E402
from evaluate_gate_fixtures import evaluate as evaluate_gate_fixtures  # noqa: E402
from package_claude_ai import package  # noqa: E402
from validate_catalog import validate_all, validate_packages  # noqa: E402


class CatalogTests(unittest.TestCase):
    def test_catalog_and_generated_distributions_validate(self) -> None:
        self.assertEqual([], validate_all(require_packages=True))
        self.assertEqual([], check_generated())
        self.assertEqual([], scan_public_boundary())

    def test_native_invocation_controls_match_canonical_metadata(self) -> None:
        for skill in SKILLS:
            canonical = read_skill_metadata(ROOT / "skills" / skill)
            claude = read_skill_metadata(ROOT / "plugins" / "claude" / PLUGIN_NAME / "skills" / skill)
            self.assertEqual("explicit" if skill in EXPLICIT_SKILLS else "implicit", canonical["invocation"])
            self.assertEqual("true" if skill in EXPLICIT_SKILLS else "false", claude["claude_explicit"])

    def test_clean_generation_and_packaging_in_temporary_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skill-catalog-test-") as temporary:
            temporary_root = Path(temporary)
            _, claude_plugin = build(temporary_root / "plugins", write_marketplaces=False)
            self.assertEqual(set(SKILLS), {path.name for path in (claude_plugin / "skills").iterdir()})
            archives = package(temporary_root / "archives")
            self.assertEqual(len(SKILLS), len(archives))

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


if __name__ == "__main__":
    unittest.main()
