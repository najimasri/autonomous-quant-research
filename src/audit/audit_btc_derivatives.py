#!/usr/bin/env python3
"""Audit committed BTC derivatives shards against their provenance manifest."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "manifests/btc_derivatives_manifest.json"
REQUIRED = {"fundingRate", "perp_klines_1m", "metrics", "liquidationSnapshot"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("source_domain") != "data.binance.vision":
        raise SystemExit("BTC derivatives audit FAIL: untrusted source domain")
    sources = manifest.get("sources", {})
    if set(sources) != REQUIRED:
        raise SystemExit("BTC derivatives audit FAIL: source set mismatch")
    for name, source in sources.items():
        status = source.get("availability_status")
        if status == "NO_STATIC_ARCHIVES_FOUND":
            if source.get("first_available_archive") or source.get("first_available_date") or source.get("shards"):
                raise SystemExit(f"BTC derivatives audit FAIL: inconsistent unavailable source {name}")
            continue
        if status != "AVAILABLE" or not source.get("first_available_archive") or not source.get("first_available_date"):
            raise SystemExit(f"BTC derivatives audit FAIL: missing first availability for {name}")
        for relative, metadata in source.get("shards", {}).items():
            path = ROOT / relative
            if not path.is_file() or metadata.get("rows", 0) <= 0:
                raise SystemExit(f"BTC derivatives audit FAIL: missing/empty {relative}")
            if sha256(path) != metadata.get("sha256"):
                raise SystemExit(f"BTC derivatives audit FAIL: hash mismatch {relative}")
    print(f"BTC derivatives audit: PASS ({len(sources)} sources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
