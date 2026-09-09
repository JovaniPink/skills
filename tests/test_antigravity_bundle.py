from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_antigravity import build  # noqa: E402
from cataloglib import EXPLICIT_SKILLS, SKILLS, directory_hashes  # noqa: E402


class AntigravityBundleTests(unittest.TestCase):
    def test_bundle_keeps_source_and_references_and_excludes_explicit_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "candidate"
            build(target)
            receipt = json.loads((target / "bundle.json").read_text())
            included = set(receipt["included_skills"])
            self.assertEqual(set(SKILLS) - set(EXPLICIT_SKILLS), included)
            self.assertEqual(set(EXPLICIT_SKILLS), set(receipt["excluded_skills"]))
            self.assertEqual("not_observed", receipt["client_loading"])
            self.assertEqual("preview", receipt["status"])
            for skill in included:
                destination = target / "plugin" / "skills" / skill
                expected = {
                    key: value for key, value in directory_hashes(ROOT / "skills" / skill).items()
                    if not key.startswith("agents/")
                }
                self.assertEqual(expected, directory_hashes(destination))
            self.assertEqual(included, {path.name for path in (target / "plugin" / "skills").iterdir()})
            self.assertEqual({"plugin.json", "skills"}, {path.name for path in (target / "plugin").iterdir()})

    def test_focused_bundle_and_deterministic_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first, second = Path(temporary) / "first", Path(temporary) / "second"
            build(first, ["claim-verification"])
            build(second, ["claim-verification"])
            self.assertEqual(directory_hashes(first), directory_hashes(second))

    def test_explicit_unknown_and_duplicate_selection_fail_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            for selected in (["publish-change-safely"], ["unknown"], ["claim-verification"] * 2):
                target = Path(temporary) / "candidate"
                with self.assertRaises(ValueError):
                    build(target, selected)
                self.assertFalse(target.exists())

    def test_existing_output_is_never_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            marker = target / "keep.txt"
            marker.write_text("previous evidence")
            with self.assertRaises(FileExistsError):
                build(target)
            self.assertEqual("previous evidence", marker.read_text())
