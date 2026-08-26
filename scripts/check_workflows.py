#!/usr/bin/env python3
"""Validate GitHub Actions workflow YAML with the locked local parser."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Final

from cataloglib import ROOT


PYYAML_VERSION: Final = "6.0.3"


def workflow_paths(root: Path = ROOT) -> tuple[Path, ...]:
    """Return the repository workflow files in deterministic order."""

    workflows_root = root / ".github" / "workflows"
    if not workflows_root.is_dir():
        return ()
    return tuple(
        path
        for path in sorted(workflows_root.iterdir())
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml"}
    )


def workflow_syntax_errors(text: str, label: str) -> list[str]:
    """Return parser errors for one GitHub Actions workflow."""

    import yaml
    from yaml.nodes import MappingNode, Node

    try:
        node: Node | None = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.MarkedYAMLError as error:
        mark = error.problem_mark
        location = f":{mark.line + 1}:{mark.column + 1}" if mark is not None else ""
        problem = error.problem or type(error).__name__
        return [f"{label}{location}: invalid workflow YAML: {problem}"]
    except yaml.YAMLError as error:
        return [f"{label}: invalid workflow YAML: {error}"]
    if node is None:
        return [f"{label}: workflow must not be empty"]
    if not isinstance(node, MappingNode):
        return [f"{label}: workflow root must be a mapping"]
    return []


def check(root: Path = ROOT) -> list[str]:
    """Validate the locked parser version and every repository workflow."""

    errors: list[str] = []
    try:
        installed_version = version("PyYAML")
    except PackageNotFoundError:
        errors.append(f"PyYAML {PYYAML_VERSION} is required; install requirements-ci-linux.txt on Linux")
        return errors
    if installed_version != PYYAML_VERSION:
        errors.append(f"PyYAML {PYYAML_VERSION} is required; found {installed_version}")
        return errors

    paths = workflow_paths(root)
    if not paths:
        return [".github/workflows: no GitHub Actions workflow files found"]
    for path in paths:
        label = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"{label}: unable to read workflow: {error}")
            continue
        errors.extend(workflow_syntax_errors(text, label))
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"GitHub Actions workflow syntax passed for {len(workflow_paths())} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
