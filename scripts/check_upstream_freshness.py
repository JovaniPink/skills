#!/usr/bin/env python3
"""Check provenance review age and optionally compare pinned upstream bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from datetime import date
from pathlib import Path

from cataloglib import ROOT, VERSION


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object: {path}")
    return value


def _fetch_marker(url: str) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "JovaniPink-skills-freshness/0.4"})
    with urllib.request.urlopen(request, timeout=30) as response:
        etag = response.headers.get("ETag")
        if etag and not etag.startswith("W/"):
            return "etag", etag
        last_modified = response.headers.get("Last-Modified")
        if last_modified:
            return "last-modified", last_modified
        return "content-sha256", hashlib.sha256(response.read()).hexdigest()


def source_urls() -> list[str]:
    catalog = _load(ROOT / "provenance" / "catalog.json")
    entries = catalog.get("entries", [])
    return sorted({entry["source_url"] for entry in entries if isinstance(entry, dict) and isinstance(entry.get("source_url"), str)})


def refresh_pins(output: Path | None = None) -> Path:
    sources: list[dict[str, str]] = []
    for url in source_urls():
        try:
            marker_kind, marker_value = _fetch_marker(url)
        except Exception as error:
            raise RuntimeError(f"cannot pin {url}: {type(error).__name__}: {error}") from error
        sources.append({"source_url": url, "marker_kind": marker_kind, "marker_value": marker_value})
    value = {
        "$schema": "./upstream-pins-schema.json",
        "catalog_version": VERSION,
        "reviewed_on": date.today().isoformat(),
        "max_review_age_days": 90,
        "sources": sources,
    }
    target = (output or ROOT / "catalog" / "upstream-pins.json").resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return target


def check(online: bool = False, today: date | None = None) -> tuple[list[str], dict[str, object]]:
    today = today or date.today()
    pins = _load(ROOT / "catalog" / "upstream-pins.json")
    expected = {
        item["source_url"]: (item["marker_kind"], item["marker_value"])
        for item in pins.get("sources", [])
        if isinstance(item, dict) and isinstance(item.get("source_url"), str)
    }
    errors: list[str] = []
    urls = source_urls()
    missing = sorted(set(urls) - set(expected))
    extra = sorted(set(expected) - set(urls))
    if missing:
        errors.append(f"upstream pins missing provenance sources: {missing}")
    if extra:
        errors.append(f"upstream pins contain unused sources: {extra}")
    reviewed_on = date.fromisoformat(str(pins["reviewed_on"]))
    maximum = int(pins["max_review_age_days"])
    if (today - reviewed_on).days > maximum:
        errors.append(f"security re-review is overdue: pins reviewed {reviewed_on.isoformat()}, maximum age {maximum} days")
    records: list[dict[str, str]] = []
    if online:
        for url in urls:
            try:
                observed_kind, observed_value = _fetch_marker(url)
                observed = f"{observed_kind}:{observed_value}"
                expected_marker = expected.get(url)
                result = "pass" if expected_marker == (observed_kind, observed_value) else "changed"
                if result == "changed":
                    errors.append(f"upstream content changed: {url}")
            except Exception as error:
                observed = "unavailable"
                result = "blocked"
                errors.append(f"upstream check blocked for {url}: {type(error).__name__}: {error}")
            expected_text = "missing" if expected.get(url) is None else f"{expected[url][0]}:{expected[url][1]}"
            records.append({"source_url": url, "expected_marker": expected_text, "observed_marker": observed, "result": result})
    report = {
        "catalog_version": VERSION,
        "checked_on": today.isoformat(),
        "online": online,
        "result": "pass" if not errors else "fail",
        "records": records,
        "errors": errors,
    }
    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--refresh-pins", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.refresh_pins:
        target = refresh_pins(args.output)
        print(f"Wrote reviewed upstream pins to {target}")
        return 0
    errors, report = check(online=args.online)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print("Upstream provenance freshness passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
