#!/usr/bin/env python3
"""Build the deterministic UTC BTC one-minute tape from verified archives."""

import argparse
import csv
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = pa.schema([
    ("timestamp", pa.timestamp("ms", tz="UTC")), ("open", pa.float64()),
    ("high", pa.float64()), ("low", pa.float64()), ("close", pa.float64()),
    ("volume", pa.float64()), ("quote_volume", pa.float64()),
    ("trade_count", pa.int64()),
])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_timestamp(value: str) -> int:
    stamp = int(value)
    return stamp // 1000 if stamp > 10**14 else stamp


def build(output: Path, metadata: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".parquet.part")
    writer = pq.ParquetWriter(temporary, SCHEMA, compression="zstd", version="2.6")
    count = 0
    first = last = previous = None
    missing = 0
    normalized_off_grid = 0
    gaps: list[dict] = []
    try:
        for archive in sorted((ROOT / "data/raw/btc").glob("*.zip")):
            with zipfile.ZipFile(archive) as zipped:
                member = zipped.namelist()[0]
                rows = []
                with zipped.open(member) as raw:
                    text = (line.decode("utf-8") for line in raw)
                    for row in csv.reader(text):
                        stamp = normalize_timestamp(row[0])
                        if stamp % 60_000:
                            normalized_off_grid += 1
                            stamp = stamp // 60_000 * 60_000
                        if previous is not None and stamp != previous + 60_000:
                            absent = max(0, (stamp - previous) // 60_000 - 1)
                            missing += absent
                            if absent:
                                gaps.append({"after_utc": datetime.fromtimestamp(previous / 1000, timezone.utc).isoformat(),
                                             "before_utc": datetime.fromtimestamp(stamp / 1000, timezone.utc).isoformat(),
                                             "missing_minutes": absent})
                        first = stamp if first is None else first
                        last = previous = stamp
                        rows.append((datetime.fromtimestamp(stamp / 1000, timezone.utc),
                                     float(row[1]), float(row[2]), float(row[3]), float(row[4]),
                                     float(row[5]), float(row[7]), int(row[8])))
                writer.write_table(pa.Table.from_pylist([dict(zip(SCHEMA.names, row)) for row in rows], schema=SCHEMA),
                                   row_group_size=100_000)
                count += len(rows)
    finally:
        writer.close()
    temporary.replace(output)
    payload = {
        "instrument": "BTCUSDT spot", "timeframe": "1m", "timezone": "UTC",
        "rows": count, "first_utc": datetime.fromtimestamp(first / 1000, timezone.utc).isoformat(),
        "last_utc": datetime.fromtimestamp(last / 1000, timezone.utc).isoformat(),
        "missing_minutes": missing, "exchange_maintenance_gaps": gaps,
        "off_grid_source_timestamps_normalized_to_minute": normalized_off_grid,
        "canonical_sha256": sha256(output),
    }
    metadata.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "data/canonical/btc_1m.parquet")
    parser.add_argument("--metadata", type=Path, default=ROOT / "data/canonical/tape_metadata_btc.json")
    args = parser.parse_args()
    build(args.output, args.metadata)
    print(sha256(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
