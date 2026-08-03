#!/usr/bin/env python3
"""Build or verify the deterministic artifact SHA-256 manifest."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "manifests" / "MANIFEST_SHA256.json"
EXCLUDED_PARTS = {".git", ".pytest_cache", "__pycache__", "phase3_round4_returns"}
EXCLUDED_FILES = {OUTPUT}
EXCLUDED_SUFFIXES = {".zip", ".bi5", ".parquet", ".part"}


def inventory() -> dict[str, str]:
    result = {}
    for path in sorted(ROOT.rglob("*")):
        if (not path.is_file() or set(path.parts) & EXCLUDED_PARTS or path in EXCLUDED_FILES
                or path.suffix in EXCLUDED_SUFFIXES):
            continue
        result[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    current = inventory()
    if args.check:
        expected = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if current != expected:
            raise SystemExit("Manifest mismatch; run build_manifest.py")
        print(f"Manifest audit: PASS ({len(current)} artifacts)")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote {len(current)} artifact hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
