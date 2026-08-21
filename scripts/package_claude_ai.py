#!/usr/bin/env python3
"""Create reproducible, individually nested Claude.ai skill archives."""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

from cataloglib import PLUGIN_NAME, ROOT, SKILLS, VERSION


ARCHIVE_TIME = (2026, 1, 1, 0, 0, 0)


def _write_file(archive: zipfile.ZipFile, source: Path, name: str) -> None:
    info = zipfile.ZipInfo(name, ARCHIVE_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, source.read_bytes())


def package(output_dir: Path | None = None) -> list[Path]:
    source_root = ROOT / "plugins" / "claude" / PLUGIN_NAME / "skills"
    output_dir = (output_dir or ROOT / "dist" / "claude-ai").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    for existing in output_dir.glob("*.zip"):
        existing.unlink()
    checksum_file = output_dir / "SHA256SUMS"
    if checksum_file.exists():
        checksum_file.unlink()

    archives: list[Path] = []
    for skill in SKILLS:
        source = source_root / skill
        if not (source / "SKILL.md").is_file():
            raise FileNotFoundError(f"generate the Claude distribution first: {source}")
        archive_path = output_dir / f"{skill}-{VERSION}.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            for item in sorted(source.rglob("*")):
                if item.is_file():
                    _write_file(archive, item, f"{skill}/{item.relative_to(source).as_posix()}")
        archives.append(archive_path)

    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in archives]
    checksum_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return archives


def main() -> int:
    archives = package()
    print(f"Packaged {len(archives)} Claude.ai skill archives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
