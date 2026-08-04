#!/usr/bin/env python3
"""Hash large, intentionally untracked source and canonical data artifacts."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "manifests" / "DATA_SHA256.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    files = []
    for base, patterns in ((ROOT / "data/raw", ("*.zip", "*.bi5")),
                           (ROOT / "data/canonical", ("*.parquet",)),
                           (ROOT / "data/derivatives", ("*.parquet",))):
        for pattern in patterns:
            files.extend(base.rglob(pattern))
    inventory = {str(path.relative_to(ROOT)): sha256(path) for path in sorted(files)}
    OUTPUT.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(inventory)} data hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
