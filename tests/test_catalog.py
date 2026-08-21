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
from cataloglib import EXPLICIT_SKILLS, SKILLS, filter_revoked, read_skill_metadata, skills_by_plugin  # noqa: E402
from check_upstream_freshness import check as check_upstream_freshness  # noqa: E402
from check_generated import check as check_generated  # noqa: E402
from check_originality import check as check_originality  # noqa: E402
from check_public_boundary import _publishable_paths, scan as scan_public_boundary  # noqa: E402
from evaluate_gate_fixtures import evaluate as evaluate_gate_fixtures  # noqa: E402
from package_claude_ai import package  # noqa: E402
from schema_validation import validate_instance  # noqa: E402
from sync_private_overlay import sync as sync_private_overlay  # noqa: E402
from validate_catalog import (  # noqa: E402
    immutable_action_reference_errors,
    validate_all,
    validate_packages,
)


class CatalogTests(unittest.TestCase):
    def test_catalog_and_generated_distributions_validate(self) -> None:
        self.assertEqual([], validate_all(require_packages=True))
        self.assertEqual([], check_generated())
        self.assertEqual([], check_originality())
        self.assertEqual([], scan_public_boundary())

    def test_public_source_audit_is_complete_and_clean_room(self) -> None:
        audit = json.loads((ROOT / "provenance" / "public-source-audit.json").read_text(encoding="utf-8"))
        self.assertEqual(2, len(audit["sources"]))
        self.assertEqual(80, audit["summary"]["skill_directories"])
        self.assertEqual(12, audit["summary"]["bundle_components"])
        self.assertEqual(92, audit["summary"]["total_components"])
        components = [component for source in audit["sources"] for component in source["components"]]
        self.assertEqual(92, len(components))
        self.assertEqual(80, sum(component["component_class"] == "skill" for component in components))
        for source in audit["sources"]:
            self.assertTrue(source["content_reviewed"])
            self.assertFalse(source["text_copied"])
            self.assertFalse(source["structure_copied"])
            self.assertFalse(source["implementation_reused"])
        v06 = {
            "code-change-review",
            "module-interface-design",
            "prototype-spike",
            "merge-conflict-reconciliation",
            "guided-configuration",
            "task-handoff",
            "workflow-retrospective",
        }
        mapped = [component for component in components if v06.intersection(component["public_mapping"])]
        self.assertTrue(mapped)
        self.assertEqual(set(), {component["disposition"] for component in mapped} - {"covered"})

    def test_reasoning_plugin_keeps_discovery_scope_focused(self) -> None:
        reasoning = skills_by_plugin()["jovanipink-reasoning"]
        self.assertEqual(11, len(reasoning))
        descriptions = [read_skill_metadata(ROOT / "skills" / skill)["description"] for skill in reasoning]
        self.assertLess(sum(len(description) for description in descriptions), 4000)
        self.assertEqual(len(descriptions), len(set(descriptions)))

    def test_reader_guide_matches_canonical_catalog(self) -> None:
        guide = (ROOT / "docs" / "skill-catalog-reader-guide.md").read_text(encoding="utf-8")
        canonical = skills_by_plugin()
        section_plugins = {
            "## Core skills: jovanipink-skills": "jovanipink-skills",
            "## Engineering skills: jovanipink-engineering": "jovanipink-engineering",
            "## Stack profiles: jovanipink-stack-profiles": "jovanipink-stack-profiles",
            "## Operations skills: jovanipink-operations": "jovanipink-operations",
            "## Reasoning skills: jovanipink-reasoning": "jovanipink-reasoning",
        }
        documented = {plugin: [] for plugin in canonical}
        documented_explicit: set[str] = set()
        current_plugin: str | None = None
        current_skill: str | None = None

        for line in guide.splitlines():
            if line in section_plugins:
                current_plugin = section_plugins[line]
                current_skill = None
            elif line.startswith("## "):
                current_plugin = None
                current_skill = None
            elif current_plugin and line.startswith("### "):
                current_skill = line.removeprefix("### ")
                documented[current_plugin].append(current_skill)
            elif current_skill and line == "Invocation: `explicit-only`.":
                documented_explicit.add(current_skill)

        self.assertEqual(
            {plugin: list(skills) for plugin, skills in canonical.items()},
            documented,
        )
        self.assertEqual(set(EXPLICIT_SKILLS), documented_explicit)
        self.assertIn(f"contains {len(SKILLS)} portable agent skills", guide)

        for plugin, skills in canonical.items():
            explicit = [skill for skill in skills if skill in EXPLICIT_SKILLS]
            explicit_cell = ", ".join(f"`{skill}`" for skill in explicit) or "None"
            self.assertIn(f"| `{plugin}` | {len(skills)} | {explicit_cell} |", guide)
        self.assertIn(
            f"| **Total** | **{len(SKILLS)}** | **{len(EXPLICIT_SKILLS)} skills** |",
            guide,
        )

    def test_v06_mutating_workflows_are_explicit_and_bounded(self) -> None:
        expected = {
            "prototype-spike",
            "merge-conflict-reconciliation",
            "guided-configuration",
            "task-handoff",
            "workflow-retrospective",
        }
        self.assertTrue(expected.issubset(EXPLICIT_SKILLS))
        conflict = (ROOT / "skills" / "merge-conflict-reconciliation" / "SKILL.md").read_text(encoding="utf-8")
        for boundary in ("abort", "Stage, continue, commit, push", "destructive reset"):
            self.assertIn(boundary, conflict)
        prototype = (ROOT / "skills" / "prototype-spike" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("not production readiness", prototype)
        self.assertIn("Do not commit, merge, deploy, migrate, publish, or promote", prototype)

    def test_v06_focused_references_exist(self) -> None:
        references = {
            "implementation-planning": {"specification-synthesis.md", "work-packages.md", "decision-map.md"},
            "multi-agent-orchestration": {"candidate-comparison.md", "coverage-fanout.md", "client-mapping.md"},
        }
        for skill, expected in references.items():
            actual = {path.name for path in (ROOT / "skills" / skill / "references").glob("*.md")}
            self.assertTrue(expected.issubset(actual))

    def test_originality_scan_rejects_source_specific_terms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="originality-regression-") as temporary:
            candidate = Path(temporary) / "SKILL.md"
            candidate.write_text("Use " + "pot" + "eto-mode for every task.\n", encoding="utf-8")
            from check_originality import _scan_text

            errors = _scan_text(candidate.as_posix(), candidate.read_text(encoding="utf-8"))
            self.assertEqual(1, len(errors))
            self.assertIn("source-specific mode name", errors[0])

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

    def test_private_inventory_reconciliation_is_sanitized_and_current(self) -> None:
        summary = json.loads((ROOT / "provenance" / "inventory-summary.json").read_text(encoding="utf-8"))
        counts = {entry["disposition"]: entry["count"] for entry in summary["dispositions"]}
        self.assertEqual(
            {
                "covered": 27,
                "partial": 0,
                "public_candidate": 2,
                "private_overlay": 1,
                "rejected": 22,
            },
            counts,
        )
        self.assertFalse(summary["content_opened"])
        self.assertFalse(summary["text_copied"])
        self.assertFalse(summary["implementation_reused"])

        roadmap = json.loads((ROOT / "incubator" / "roadmap.json").read_text(encoding="utf-8"))
        tracks = {track["id"]: track for track in roadmap["tracks"]}
        self.assertEqual("released", tracks["portable-skill-authoring"]["status"])
        self.assertEqual("jovanipink-reasoning", tracks["portable-skill-authoring"]["plugin"])
        self.assertEqual(["portable-skill-authoring"], tracks["portable-skill-authoring"]["skills"])
        self.assertEqual("released", tracks["engineering-depth-and-continuity"]["status"])
        self.assertEqual("released", tracks["reasoning-continuity"]["status"])

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
            expected_surfaces = {
                "Codex CLI",
                "Codex Desktop",
                "Claude Code CLI",
                "Claude Code Desktop",
                "Claude.ai",
            }
            if matrix["catalog_version"] not in {"0.1.0", "0.2.0", "0.3.0"}:
                expected_surfaces.add("ChatGPT Web")
            self.assertEqual(expected_surfaces, {record["surface"] for record in records})

    def test_v04_records_chatgpt_web_as_a_distinct_surface(self) -> None:
        matrix = json.loads((ROOT / "docs" / "client-observations-v0.4.json").read_text(encoding="utf-8"))
        web_records = [record for record in matrix["records"] if record["surface"] == "ChatGPT Web"]
        self.assertEqual(6, len(web_records))
        self.assertEqual({"blocked"}, {record["result"] for record in web_records})
        self.assertTrue(any("no skills" in record["invocation_behavior"] for record in web_records))

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
            non_us_spelling = "organi" + "sation"
            candidate.write_text(
                f"plain{chr(0x2014)}text with {non_us_spelling}{chr(7)}\n",
                encoding="utf-8",
            )
            errors = scan_public_boundary([candidate], include_packages=False)
            self.assertTrue(any("non-ASCII character" in error for error in errors))
            self.assertTrue(any("non-US English spelling" in error for error in errors))
            self.assertTrue(any("ASCII control character" in error for error in errors))

    def test_boundary_scan_preserves_exact_external_tokens(self) -> None:
        with tempfile.TemporaryDirectory(prefix="language-token-boundary-") as temporary:
            candidate = Path(temporary) / "candidate.md"
            candidate.write_text(
                "External references:\n"
                "- https://example.com/catalogue/reference\n"
                "- [Acme Colour API](https://example.com/api)\n"
                "- `assets/catalogue/reference.json`\n",
                encoding="utf-8",
            )
            self.assertEqual([], scan_public_boundary([candidate], include_packages=False))

    def test_boundary_scan_still_rejects_reader_authored_spelling(self) -> None:
        with tempfile.TemporaryDirectory(prefix="language-prose-boundary-") as temporary:
            candidate = Path(temporary) / "candidate.md"
            candidate.write_text("The cata" + "logue describes the API.\n", encoding="utf-8")
            errors = scan_public_boundary([candidate], include_packages=False)
            self.assertEqual(1, len(errors))
            self.assertIn("non-US English spelling", errors[0])

    def test_compound_skill_titles_follow_editorial_style(self) -> None:
        expected = {
            "cross-capability-dependency-mapping": "Cross-Capability Dependency Mapping",
            "cross-stack-quality-gates": "Cross-Stack Quality Gates",
            "dependency-supply-chain-review": "Dependency and Supply-Chain Review",
            "high-signal-technical-writing": "High-Signal Technical Writing",
            "multi-agent-orchestration": "Multi-Agent Orchestration",
            "public-private-boundary-review": "Public-Private Boundary Review",
            "source-grounded-research": "Source-Grounded Research",
            "test-driven-change": "Test-Driven Change",
        }
        for skill, title in expected.items():
            body = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            interface = (ROOT / "skills" / skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"# {title}\n", body)
            self.assertIn(f'display_name: "{title}"', interface)

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

    def test_revocation_filter_withdraws_catalog_advertisement(self) -> None:
        self.assertEqual(("kept-skill",), filter_revoked(("kept-skill", "revoked-skill"), frozenset({"revoked-skill"})))

    def test_private_overlay_example_is_drift_free(self) -> None:
        self.assertEqual([], sync_private_overlay(ROOT / "examples" / "private-overlay", check_only=True))

    def test_upstream_review_freshness_is_current_offline(self) -> None:
        errors, report = check_upstream_freshness(online=False)
        self.assertEqual([], errors)
        self.assertEqual("pass", report["result"])

    def test_public_source_audit_revisions_feed_freshness(self) -> None:
        from check_upstream_freshness import audited_git_sources

        sources = audited_git_sources()
        self.assertEqual(2, len(sources))
        self.assertEqual(
            {
                "5b15a47f2d7150f545fbcacbfe381787fc0230dc",
                "46125561306434d8a1d7745d540d8932ab0cd2a2",
            },
            {source["pinned_revision"] for source in sources},
        )


if __name__ == "__main__":
    unittest.main()
