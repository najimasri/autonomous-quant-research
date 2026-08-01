#!/usr/bin/env python3
"""Verify Phase 0 source checksums and canonical metadata hashes."""

import argparse
import hashlib
import json
from pathlib import Path

import pyarrow.parquet as pq

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


def verify_canonical_shards(data_manifest: dict[str, str]) -> tuple[int, int]:
    """Verify every recorded yearly shard by hash and physical row count."""
    shard_count = 0
    row_count = 0
    for instrument in ("btc", "xau"):
        batch_path = ROOT / f"manifests/{instrument}_batch_manifest.json"
        batch = json.loads(batch_path.read_text(encoding="utf-8"))
        for relative, recorded in sorted(batch["shards"].items()):
            path = ROOT / relative
            if not path.exists():
                raise SystemExit(f"Phase 0 data audit FAIL: absent shard ({relative})")
            digest = sha256(path)
            if digest != recorded["sha256"] or digest != data_manifest.get(relative):
                raise SystemExit(f"Phase 0 data audit FAIL: shard hash ({relative})")
            rows = pq.ParquetFile(path).metadata.num_rows
            if rows != recorded["rows"]:
                raise SystemExit(f"Phase 0 data audit FAIL: shard rows ({relative})")
            shard_count += 1
            row_count += rows
    return shard_count, row_count


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

    data_manifest = json.loads((ROOT / "manifests/DATA_SHA256.json").read_text(encoding="utf-8"))
    recorded_archives = sorted(relative for relative in data_manifest
                               if relative.startswith("data/raw/btc/") and relative.endswith(".zip"))
    archives = [ROOT / relative for relative in recorded_archives]
    if not archives:
        raise SystemExit("Phase 0 data audit FAIL: no BTC archives")
    for archive in archives:
        if not archive.exists():
            raise SystemExit(f"Phase 0 data audit FAIL: absent BTC archive ({archive.name})")
        checksum = archive.with_suffix(".zip.CHECKSUM")
        expected = checksum.read_text(encoding="utf-8").split()[0].lower()
        digest = sha256(archive)
        if digest != expected or digest != data_manifest[str(archive.relative_to(ROOT))]:
            raise SystemExit(f"Phase 0 data audit FAIL: {archive.name}")
    shards, rows = verify_canonical_shards(data_manifest)
    costs = json.loads((ROOT / "manifests/xau_cost_observations.json").read_text(encoding="utf-8"))
    if (costs.get("candle", {}).get("label") != "CANDLE_DERIVED_APPROXIMATION"
            or costs.get("tick", {}).get("label") != "TICK_OBSERVED"
            or costs["candle"].get("rows", 0) <= 0 or costs["tick"].get("rows", 0) <= 0):
        raise SystemExit("Phase 0 data audit FAIL: XAU cost observations")
    print(f"Phase 0 data audit: PASS ({len(archives)} BTC checksums; "
          f"{shards} canonical shards; {rows} canonical rows; XAU cost observations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
