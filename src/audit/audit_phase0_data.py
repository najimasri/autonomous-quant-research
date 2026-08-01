#!/usr/bin/env python3
"""Verify Phase 0 source checksums and canonical metadata hashes."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    archives = sorted((ROOT / "data/raw/btc").glob("*.zip"))
    if not archives:
        raise SystemExit("Phase 0 data audit FAIL: no BTC archives")
    for archive in archives:
        checksum = archive.with_suffix(".zip.CHECKSUM")
        expected = checksum.read_text(encoding="utf-8").split()[0].lower()
        if sha256(archive) != expected:
            raise SystemExit(f"Phase 0 data audit FAIL: {archive.name}")
    if not any(path.stat().st_size for path in (ROOT / "data/raw/xau").rglob("*.bi5")):
        raise SystemExit("Phase 0 data audit FAIL: no XAU ticks")
    for instrument in ("btc", "xau"):
        tape = ROOT / f"data/canonical/{instrument}_1m.parquet"
        metadata_path = ROOT / f"data/canonical/tape_metadata_{instrument}.json"
        if not tape.exists() or not metadata_path.exists():
            raise SystemExit(f"Phase 0 data audit FAIL: {instrument} canonical artifacts absent")
        metadata = json.loads(metadata_path.read_text())
        if sha256(tape) != metadata["canonical_sha256"]:
            raise SystemExit(f"Phase 0 data audit FAIL: {instrument} canonical hash")
        if metadata["rows"] <= 0:
            raise SystemExit(f"Phase 0 data audit FAIL: {instrument} empty tape")
    print(f"Phase 0 data audit: PASS ({len(archives)} BTC checksums; both canonical tapes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
