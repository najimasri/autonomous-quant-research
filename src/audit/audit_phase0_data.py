#!/usr/bin/env python3
"""Verify Phase 0 source checksums and canonical metadata hashes."""

import argparse
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


def verify_present_files(paths: list[Path], manifest: dict[str, str]) -> int:
    """Verify every locally present data artifact against its recorded hash."""
    count = 0
    for path in paths:
        relative = str(path.relative_to(ROOT))
        expected = manifest.get(relative)
        if expected is None:
            raise SystemExit(f"Phase 0 data audit FAIL: unrecorded data ({relative})")
        if sha256(path) != expected:
            raise SystemExit(f"Phase 0 data audit FAIL: manifest hash ({relative})")
        count += 1
    return count


def audit_source_checkout() -> int:
    """Audit policy-optional data without requiring ignored BTC artifacts."""
    manifest = json.loads((ROOT / "manifests/DATA_SHA256.json").read_text(encoding="utf-8"))
    btc_paths = sorted((ROOT / "data/raw/btc").glob("*.zip"))
    btc_paths += sorted((ROOT / "data/canonical").glob("btc*.parquet"))
    xau_paths = sorted((ROOT / "data/raw/xau").rglob("*.bi5"))
    xau_paths += sorted((ROOT / "data/canonical").glob("xau*.parquet"))
    btc = verify_present_files(btc_paths, manifest)
    xau = verify_present_files(xau_paths, manifest)
    print(f"Phase 0 source-checkout data audit: PASS ({btc} BTC; {xau} XAU files present)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-checkout",
        action="store_true",
        help="allow policy-absent data, while hashing every recorded data file that is present",
    )
    args = parser.parse_args()
    if args.source_checkout:
        return audit_source_checkout()

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
        metadata_path = ROOT / f"data/canonical/tape_metadata_{instrument}.json"
        if not metadata_path.exists():
            raise SystemExit(f"Phase 0 data audit FAIL: {instrument} canonical artifacts absent")
        metadata = json.loads(metadata_path.read_text())
        hashes = metadata.get("canonical_shards_sha256")
        if hashes is None:
            hashes = {f"data/canonical/{instrument}_1m.parquet": metadata["canonical_sha256"]}
        for relative, expected in hashes.items():
            tape = ROOT / relative
            if not tape.exists() or sha256(tape) != expected:
                raise SystemExit(f"Phase 0 data audit FAIL: {instrument} canonical hash ({relative})")
        if metadata["rows"] <= 0:
            raise SystemExit(f"Phase 0 data audit FAIL: {instrument} empty tape")
    print(f"Phase 0 data audit: PASS ({len(archives)} BTC checksums; both canonical tapes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
