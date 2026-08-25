from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_distributions import build, marketplace_documents  # noqa: E402
from cataloglib import EXPLICIT_SKILLS, SKILLS, filter_revoked, read_skill_metadata, skills_by_plugin  # noqa: E402
from check_upstream_freshness import (  # noqa: E402
    _normalized_content_sha256,
    check as check_upstream_freshness,
)
from check_generated import check as check_generated  # noqa: E402
from check_originality import check as check_originality  # noqa: E402
from check_public_boundary import _publishable_paths, scan as scan_public_boundary  # noqa: E402
from check_repository_independence import (  # noqa: E402
    check as check_repository_independence,
    provenance_source_errors,
    scan_text as scan_repository_independence,
)
from evaluate_gate_fixtures import evaluate as evaluate_gate_fixtures  # noqa: E402
from package_claude_ai import package  # noqa: E402
from schema_validation import validate_instance  # noqa: E402
from sync_private_overlay import sync as sync_private_overlay  # noqa: E402
from validate_catalog import (  # noqa: E402
    immutable_action_reference_errors,
    skill_name_errors,
    validate_all,
    validate_packages,
)


class CatalogTests(unittest.TestCase):
    def test_catalog_and_generated_distributions_validate(self) -> None:
        self.assertEqual([], validate_all(require_packages=True))
        self.assertEqual([], check_generated())
        self.assertEqual([], check_originality())
        self.assertEqual([], check_repository_independence())
        self.assertEqual([], scan_public_boundary())

    def test_retired_external_audit_records_are_absent(self) -> None:
        retired = {
            "provenance/public-source-audit.json",
            "provenance/public-source-audit-schema.json",
            "provenance/inventory-summary.json",
            "provenance/inventory-summary-schema.json",
        }
        self.assertEqual(retired, {path for path in retired if not (ROOT / path).exists()})

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
            "## AI systems skills: jovanipink-ai-systems": "jovanipink-ai-systems",
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

    def test_skill_cheatsheet_matches_canonical_catalog(self) -> None:
        cheatsheet = (ROOT / "docs" / "skill-cheatsheet.md").read_text(encoding="utf-8")
        canonical = skills_by_plugin()
        section_plugins = {
            "## Core: jovanipink-skills": "jovanipink-skills",
            "## Engineering: jovanipink-engineering": "jovanipink-engineering",
            "## Stack profiles: jovanipink-stack-profiles": "jovanipink-stack-profiles",
            "## Operations: jovanipink-operations": "jovanipink-operations",
            "## Reasoning: jovanipink-reasoning": "jovanipink-reasoning",
            "## AI systems: jovanipink-ai-systems": "jovanipink-ai-systems",
        }
        documented = {plugin: [] for plugin in canonical}
        documented_invocation: dict[str, str] = {}
        current_plugin: str | None = None

        for line in cheatsheet.splitlines():
            if line in section_plugins:
                current_plugin = section_plugins[line]
            elif line.startswith("## "):
                current_plugin = None
            elif current_plugin and line.startswith("| `"):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                skill = cells[0].strip("`")
                documented[current_plugin].append(skill)
                documented_invocation[skill] = cells[2]

        self.assertEqual(
            {plugin: list(skills) for plugin, skills in canonical.items()},
            documented,
        )
        self.assertEqual(set(SKILLS), set(documented_invocation))
        for skill, invocation in documented_invocation.items():
            expected = "Explicit-only" if skill in EXPLICIT_SKILLS else "Implicit"
            self.assertEqual(expected, invocation, skill)
        self.assertIn(f"catalog contains {len(SKILLS)} skills", cheatsheet)

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

    def test_originality_scan_rejects_generic_copy_attribution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="originality-regression-") as temporary:
            candidate = Path(temporary) / "SKILL.md"
            candidate.write_text("This workflow was copied " + "from an upstream skill.\n", encoding="utf-8")
            from check_originality import _scan_text

            errors = _scan_text(candidate.as_posix(), candidate.read_text(encoding="utf-8"))
            self.assertEqual(1, len(errors))
            self.assertIn("external implementation attribution", errors[0])

    def test_repository_independence_rejects_external_repositories_and_mappings(self) -> None:
        repository_url = "https://" + "github.com/" + "example-org/example-skills"
        marketplace_id = "marketplace add " + "example-org/example-skills"
        package_id = "plugin install " + "external-skill@external-marketplace"
        mapping = '"public_' + 'mapping": ["local-skill"]'
        self.assertTrue(scan_repository_independence("fixture.md", repository_url))
        self.assertTrue(scan_repository_independence("fixture.md", marketplace_id))
        self.assertTrue(scan_repository_independence("fixture.md", package_id))
        self.assertTrue(scan_repository_independence("fixture.json", mapping))

    def test_repository_independence_keeps_narrow_repository_link_exceptions(self) -> None:
        owned = "https://" + "github.com/" + "JovaniPink/skills"
        action = "https://" + "github.com/" + "actions/checkout"
        package_id = "plugin install " + "jovanipink-engineering@jovanipink-skills"
        self.assertEqual([], scan_repository_independence("README.md", owned))
        self.assertEqual([], scan_repository_independence("provenance/ci-actions.json", action))
        self.assertEqual([], scan_repository_independence("docs/README.md", package_id))
        self.assertTrue(scan_repository_independence("docs/example.md", action))

    def test_repository_independence_allows_only_the_reviewed_google_agents_cli_link(self) -> None:
        agents_cli = "https://" + "github.com/" + "google/agents-cli"
        unrelated = "https://" + "github.com/" + "google/unrelated"
        self.assertEqual([], scan_repository_independence("docs/google-adk.md", agents_cli))
        self.assertTrue(scan_repository_independence("docs/example.md", agents_cli))
        self.assertTrue(scan_repository_independence("docs/google-adk.md", unrelated))

    def test_provenance_sources_are_primary_authorities(self) -> None:
        self.assertEqual([], provenance_source_errors())

    def test_v09_taxonomy_reconciles_with_canonical_skills(self) -> None:
        schema = json.loads((ROOT / "catalog" / "skills-schema.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "catalog" / "skills.json").read_text(encoding="utf-8"))
        self.assertEqual([], validate_instance(catalog, schema))
        records = {record["skill"]: record for record in catalog["skills"]}
        self.assertEqual(set(SKILLS), set(records))
        for skill, record in records.items():
            metadata = read_skill_metadata(ROOT / "skills" / skill)
            self.assertEqual(metadata["plugin"], record["plugin"])
            self.assertEqual(metadata["risk_class"], record["risk_class"])
            self.assertEqual(metadata["invocation"], record["invocation"])
            self.assertTrue((ROOT / record["maturity_evidence"]).is_file())
            self.assertNotIn(skill, record["composes_with"])
            self.assertNotIn(skill, record["conflicts_with"])
            for related in record["composes_with"] + record["conflicts_with"]:
                self.assertIn(related, records)

    def test_v09_packs_and_recipes_reconcile_and_fit_discovery_budget(self) -> None:
        schema = json.loads((ROOT / "catalog" / "packs-schema.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "catalog" / "packs.json").read_text(encoding="utf-8"))
        self.assertEqual([], validate_instance(catalog, schema))
        plugins = skills_by_plugin()
        packs = {record["plugin"]: record for record in catalog["plugin_packs"]}
        self.assertEqual(set(plugins), set(packs))
        for plugin, record in packs.items():
            self.assertEqual(list(plugins[plugin]), record["skills"])
            expected = sum(
                len(read_skill_metadata(ROOT / "skills" / skill)["description"])
                for skill in record["skills"]
            )
            self.assertEqual(expected, record["description_characters"])
            expected_status = "over-limit" if expected > 8000 else "warning" if expected >= 6000 else "within-budget"
            self.assertEqual(expected_status, record["budget_status"])

        for recipe in catalog["recipes"]:
            self.assertIn(len(recipe["skills"]), {2, 3})
            self.assertEqual(len(recipe["skills"]), len(set(recipe["skills"])))
            expected = sum(
                len(read_skill_metadata(ROOT / "skills" / skill)["description"])
                for skill in recipe["skills"]
            )
            self.assertEqual(expected, recipe["description_characters"])
            self.assertLessEqual(recipe["description_characters"], 8000)
            expected_status = "warning" if expected >= 6000 else "within-budget"
            self.assertEqual(expected_status, recipe["budget_status"])

    def test_v09_every_skill_has_complete_evaluation_contract(self) -> None:
        schema = json.loads((ROOT / "evals" / "schema.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        self.assertEqual([], validate_instance(catalog, schema))
        self.assertEqual(set(SKILLS), {record["skill"] for record in catalog["skills"]})
        for record in catalog["skills"]:
            self.assertGreaterEqual(len(record["output_rubric"]), 3)
            self.assertIn(
                record["baseline_comparison"]["status"],
                {"pass", "fail", "blocked", "not_supported"},
            )

    def test_v09_observation_schema_has_distinct_api_and_gemini_surfaces(self) -> None:
        schema = json.loads((ROOT / "docs" / "client-observations-schema.json").read_text(encoding="utf-8"))
        surface_enum = schema["properties"]["records"]["items"]["properties"]["surface"]["enum"]
        for surface in (
            "Gemini CLI",
            "OpenAI Skills API",
            "Anthropic Skills API",
            "Anthropic Managed Agents",
        ):
            self.assertIn(surface, surface_enum)

    def test_v09_changed_upstreams_have_human_readable_review_records(self) -> None:
        schema = json.loads((ROOT / "catalog" / "upstream-reviews-schema.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "catalog" / "upstream-reviews.json").read_text(encoding="utf-8"))
        self.assertEqual([], validate_instance(catalog, schema))
        expected = {
            "https://agentskills.io/specification",
            "https://developer.hashicorp.com/terraform/language",
            "https://docs.github.com/en/pull-requests/reference/pull-request-reviews",
            "https://docs.python.org/3/",
            "https://docs.python.org/3/library/unittest.html",
            "https://git-scm.com/docs/git-merge",
            "https://git-scm.com/docs/git-worktree",
            "https://learn.chatgpt.com/docs/agent-configuration/subagents",
            "https://opentelemetry.io/docs/concepts/signals/",
        }
        records = {record["url"]: record for record in catalog["reviews"]}
        self.assertEqual(expected, set(records))
        for record in records.values():
            self.assertEqual("reviewed", record["status"])
            self.assertGreaterEqual(len(record["affected_skills"]), 1)
            self.assertTrue(record["finding"])
            self.assertTrue(record["action"])

    def test_v09_subagent_mapping_preserves_surface_and_configuration_boundaries(self) -> None:
        mapping = (
            ROOT
            / "skills"
            / "multi-agent-orchestration"
            / "references"
            / "client-mapping.md"
        ).read_text(encoding="utf-8")
        for required in (
            "exact surface",
            "account capability",
            "reasoning level",
            "permission mode",
            "Do not treat one trigger path as proof for another",
            "Use the smallest useful fanout",
            "verify the actual configuration instead of assuming it",
        ):
            self.assertIn(required, mapping)

    def test_v09_open_spec_name_limits_are_enforced(self) -> None:
        self.assertEqual([], skill_name_errors("safe-skill"))
        self.assertTrue(skill_name_errors("bad--skill"))
        self.assertTrue(skill_name_errors("a" * 65))
        self.assertTrue(skill_name_errors("Bad-Skill"))

    def test_v09_release_manifest_tracks_governance_records(self) -> None:
        manifest = json.loads((ROOT / "releases" / "0.9.0" / "manifest.json").read_text(encoding="utf-8"))
        paths = {artifact["path"] for artifact in manifest["artifacts"]}
        self.assertTrue(
            {
                "catalog/skills.json",
                "catalog/packs.json",
                "catalog/upstream-reviews.json",
                "evals/cases.json",
                "provenance/catalog.json",
            }.issubset(paths)
        )

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

    def test_original_work_roadmap_has_no_external_inventory_track(self) -> None:
        roadmap = json.loads((ROOT / "incubator" / "roadmap.json").read_text(encoding="utf-8"))
        tracks = {track["id"]: track for track in roadmap["tracks"]}
        self.assertNotIn("additional-stack-profiles", tracks)
        self.assertEqual("released", tracks["acceptance-evidence-ledger"]["status"])
        self.assertEqual("v0.7", tracks["acceptance-evidence-ledger"]["target_release"])
        self.assertEqual("released", tracks["portable-skill-authoring"]["status"])
        self.assertEqual("jovanipink-reasoning", tracks["portable-skill-authoring"]["plugin"])
        self.assertEqual(["portable-skill-authoring"], tracks["portable-skill-authoring"]["skills"])
        self.assertEqual("released", tracks["engineering-depth-and-continuity"]["status"])
        self.assertEqual("released", tracks["reasoning-continuity"]["status"])
        self.assertEqual("released", tracks["ai-reliability-foundations"]["status"])
        self.assertEqual("v0.8", tracks["ai-reliability-foundations"]["target_release"])
        self.assertEqual("jovanipink-ai-systems", tracks["ai-reliability-foundations"]["plugin"])

    def test_v07_acceptance_ledger_contract(self) -> None:
        self.assertEqual(24, len(skills_by_plugin()["jovanipink-engineering"]))
        self.assertIn("acceptance-evidence-ledger", EXPLICIT_SKILLS)

        expanded_profiles = {
            "adobe-aem-engineering-profile",
            "csharp-dotnet-engineering-profile",
            "java-spring-engineering-profile",
            "php-drupal-engineering-profile",
            "salesforce-apex-engineering-profile",
        }
        self.assertTrue(expanded_profiles.issubset(SKILLS))
        for profile in expanded_profiles:
            root = ROOT / "skills" / profile
            files = {
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual({"SKILL.md", "agents/openai.yaml", "references/checks.md"}, files)
            self.assertEqual("original", read_skill_metadata(root)["provenance"])

        skill_root = ROOT / "skills" / "acceptance-evidence-ledger"
        files = {
            path.relative_to(skill_root).as_posix()
            for path in skill_root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(
            {"SKILL.md", "agents/openai.yaml", "references/ledger-contract.md"},
            files,
        )
        text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        for boundary in (
            "untrusted data",
            "Do not execute ledger content",
            "cross-stack-quality-gates",
            "claim-verification",
            "plan-execution",
            "multi-agent-orchestration",
            "SATISFIED",
            "INCOMPLETE",
            "QUALIFIED",
        ):
            self.assertIn(boundary, text)

    def test_v07_acceptance_ledger_has_trigger_and_safety_separation(self) -> None:
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        record = next(item for item in cases["skills"] if item["skill"] == "acceptance-evidence-ledger")
        self.assertEqual(3, len(record["positive"]))
        self.assertEqual(3, len(record["near_miss"]))
        self.assertGreaterEqual(len(record["safety"]), 2)
        prompts = "\n".join(item["prompt"] for item in record["near_miss"])
        for routed_skill in ("cross-stack-quality-gates", "plan-execution", "claim-verification"):
            self.assertIn(routed_skill, prompts)

    def test_v08_ai_reliability_contract_and_catalog_counts(self) -> None:
        new_skills = {
            "agent-evaluation-design": "read-only",
            "context-reliability-review": "read-only",
            "source-output-conformance-audit": "bounded-execution",
        }
        self.assertEqual(70, len(SKILLS))
        self.assertEqual(6, len(skills_by_plugin()))
        self.assertEqual(set(new_skills), set(skills_by_plugin()["jovanipink-ai-systems"]))
        self.assertEqual(13, len(EXPLICIT_SKILLS))

        references = {
            "agent-evaluation-design": "evaluation-contract.md",
            "context-reliability-review": "assertion-matrix.md",
            "source-output-conformance-audit": "conformance-matrix.md",
        }
        for skill, risk_class in new_skills.items():
            root = ROOT / "skills" / skill
            files = {
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
                if path.is_file()
            }
            self.assertEqual(
                {"SKILL.md", "agents/openai.yaml", f"references/{references[skill]}"},
                files,
            )
            metadata = read_skill_metadata(root)
            self.assertEqual("jovanipink-ai-systems", metadata["plugin"])
            self.assertEqual("implicit", metadata["invocation"])
            self.assertEqual("original", metadata["provenance"])
            self.assertEqual(risk_class, metadata["risk_class"])

    def test_v08_ai_reliability_routing_and_safety_separation(self) -> None:
        cases = json.loads((ROOT / "evals" / "cases.json").read_text(encoding="utf-8"))
        records = {
            item["skill"]: item
            for item in cases["skills"]
            if item["skill"] in {
                "agent-evaluation-design",
                "context-reliability-review",
                "source-output-conformance-audit",
            }
        }
        self.assertEqual(3, len(records))
        for record in records.values():
            self.assertGreaterEqual(len(record["positive"]), 3)
            self.assertGreaterEqual(len(record["near_miss"]), 3)
            self.assertGreaterEqual(len(record["safety"]), 1)
            self.assertGreaterEqual(len(record["output_rubric"]), 3)
            self.assertNotEqual("not_run", record["baseline_comparison"]["status"])

        near_misses = "\n".join(
            case["prompt"]
            for record in records.values()
            for case in record["near_miss"]
        )
        for collision in (
            "test-strategy",
            "test-quality-review",
            "acceptance-evidence-ledger",
            "authority-boundary-review",
            "ConvergeQL-style model review",
        ):
            self.assertIn(collision, near_misses)

        evaluation = (ROOT / "skills" / "agent-evaluation-design" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("evaluation contract", evaluation)
        self.assertIn("paid or external evaluation", evaluation)
        context = (ROOT / "skills" / "context-reliability-review" / "SKILL.md").read_text(encoding="utf-8")
        for boundary in ("effective time", "recorded time", "supersession", "revocation"):
            self.assertIn(boundary, context)
        conformance = (ROOT / "skills" / "source-output-conformance-audit" / "SKILL.md").read_text(encoding="utf-8")
        for dimension in (
            "correctness",
            "completeness",
            "storage correctness",
            "reproducibility",
            "unresolved evidence",
        ):
            self.assertIn(dimension, conformance)

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
            if matrix["catalog_version"] == "0.8.0":
                expected_surfaces.remove("Codex Desktop")
                expected_surfaces.add("ChatGPT Desktop")
            self.assertEqual(expected_surfaces, {record["surface"] for record in records})

    def test_v04_records_chatgpt_web_as_a_distinct_surface(self) -> None:
        matrix = json.loads((ROOT / "docs" / "client-observations-v0.4.json").read_text(encoding="utf-8"))
        web_records = [record for record in matrix["records"] if record["surface"] == "ChatGPT Web"]
        self.assertEqual(6, len(web_records))
        self.assertEqual({"blocked"}, {record["result"] for record in web_records})
        self.assertTrue(any("no skills" in record["invocation_behavior"] for record in web_records))

    def test_v08_records_each_client_lifecycle_observation_separately(self) -> None:
        matrix = json.loads((ROOT / "docs" / "client-observations-v0.8.json").read_text(encoding="utf-8"))
        expected_phases = {"INSTALL", "DISCOVERY", "IMPLICIT", "REFERENCE", "REFUSAL", "UPDATE", "REMOVAL"}
        by_surface: dict[str, set[str]] = {}
        for record in matrix["records"]:
            by_surface.setdefault(record["surface"], set()).add(record["case_id"].rsplit("-", 1)[-1])
        self.assertEqual(6, len(by_surface))
        self.assertEqual({surface: expected_phases for surface in by_surface}, by_surface)
        self.assertEqual({"blocked"}, {record["result"] for record in matrix["records"]})

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

    def test_freshness_comparison_preserves_the_pinned_marker_kind(self) -> None:
        from check_upstream_freshness import _fetch_marker

        class Response:
            headers = {"ETag": '"transient"', "Last-Modified": "Sun, 23 Aug 2026 18:16:51 GMT"}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self) -> bytes:
                return b"stable authority content"

        with patch("check_upstream_freshness.urllib.request.urlopen", return_value=Response()):
            kind, value = _fetch_marker("https://example.com/specification", preferred_kind="content-sha256")
        self.assertEqual("content-sha256", kind)
        self.assertEqual(hashlib.sha256(b"stable authority content").hexdigest(), value)

    def test_freshness_normalization_ignores_only_per_request_html_values(self) -> None:
        first = b'''<meta name="csrf-token" content="first" />
<script>NREUM.info={"queueTime":1,"applicationTime":131}</script>
<meta content='visitor-one' name='ua:temp_visitor_id'>
<input type="hidden" name="form_build_id" value="form-first" />
<div class="view-dom-id-0123456789abcdef0123456789abcdef"></div>
<script>{"theme_token":"theme-first"}</script>
<script nonce="nonce-first">stable()</script>
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/one" data-cf-beacon='{"token":"one"}'></script>
<script nonce="nonce-first">(function(){var a='/cdn-cgi/challenge-platform/one';})();</script>
<main>Official authority content</main>'''
        second = b'''<meta name="csrf-token" content="second" />
<script>NREUM.info={"queueTime":9,"applicationTime":157}</script>
<meta content='visitor-two' name='ua:temp_visitor_id'>
<input type="hidden" name="form_build_id" value="form-second" />
<div class="view-dom-id-fedcba9876543210fedcba9876543210"></div>
<script>{"theme_token":"theme-second"}</script>
<script nonce="nonce-second">stable()</script>
<script nonce="nonce-second">(function(){var a='/cdn-cgi/challenge-platform/two';})();</script>
<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/two" data-cf-beacon='{"token":"two"}'></script>
<main>Official authority content</main>'''
        changed = second.replace(b"Official authority content", b"Changed authority content")
        self.assertEqual(_normalized_content_sha256(first), _normalized_content_sha256(second))
        self.assertNotEqual(_normalized_content_sha256(first), _normalized_content_sha256(changed))

    def test_upstream_freshness_uses_primary_authority_urls_only(self) -> None:
        errors, report = check_upstream_freshness(online=False)
        self.assertEqual([], errors)
        self.assertEqual("pass", report["result"])


if __name__ == "__main__":
    unittest.main()
