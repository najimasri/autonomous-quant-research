#!/usr/bin/env python3
"""Build a deterministic BID-price XAUUSD minute tape from Dukascopy ticks."""

import argparse
import hashlib
import json
import lzma
import struct
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
RECORD = struct.Struct(">3I2f")
SCHEMA = pa.schema([
    ("timestamp", pa.timestamp("ms", tz="UTC")), ("open", pa.float64()),
    ("high", pa.float64()), ("low", pa.float64()), ("close", pa.float64()),
    ("tick_volume", pa.int64()), ("spread_median", pa.float64()),
])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decode(path: Path) -> pd.DataFrame:
    if path.stat().st_size == 0:
        return pd.DataFrame()
    relative = path.relative_to(ROOT / "data/raw/xau")
    year, month0, day = map(int, relative.parts[:3])
    hour = int(relative.name[:2])
    base = datetime(year, month0 + 1, day, hour, tzinfo=timezone.utc)
    try:
        content = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_AUTO)
    except lzma.LZMAError:
        content = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_RAW,
                                  filters=[{"id": lzma.FILTER_LZMA1, "dict_size": 1 << 23,
                                            "lc": 3, "lp": 0, "pb": 2}])
    values = list(RECORD.iter_unpack(content))
    if not values:
        return pd.DataFrame()
    frame = pd.DataFrame(values, columns=["offset", "ask", "bid", "ask_volume", "bid_volume"])
    frame["timestamp"] = pd.to_datetime(base) + pd.to_timedelta(frame.offset, unit="ms")
    frame["bid"] = frame.bid / 1000.0
    frame["spread"] = (frame.ask - frame.bid * 1000.0) / 1000.0
    return frame


def aggregate(paths: list[Path]) -> pd.DataFrame:
    ticks = [frame for path in paths if not (frame := decode(path)).empty]
    if not ticks:
        return pd.DataFrame()
    tick = pd.concat(ticks, ignore_index=True).set_index("timestamp")
    ohlc = tick.bid.resample("1min").ohlc()
    ohlc["tick_volume"] = tick.bid.resample("1min").count()
    ohlc["spread_median"] = tick.spread.resample("1min").median()
    return ohlc.dropna().reset_index()


def build(output: Path, metadata: Path, costs: Path) -> None:
    all_paths = sorted((ROOT / "data/raw/xau").rglob("*.bi5"))
    years = sorted({int(path.relative_to(ROOT / "data/raw/xau").parts[0]) for path in all_paths})
    count = 0
    first = last = None
    missing = 0
    observations = []
    shard_hashes = {}
    for year in years:
        frame = aggregate([path for path in all_paths if path.relative_to(ROOT / "data/raw/xau").parts[0] == str(year)])
        if frame.empty:
            continue
        shard = output.with_name(f"{output.stem}_{year}{output.suffix}")
        temporary = shard.with_suffix(".parquet.part")
        table = pa.Table.from_pandas(frame, schema=SCHEMA, preserve_index=False)
        pq.write_table(table, temporary, compression="zstd", version="2.6", row_group_size=100_000)
        temporary.replace(shard)
        shard_hashes[str(shard.relative_to(ROOT))] = sha256(shard)
        stamps = frame.timestamp.astype("int64") // 1_000_000
        diffs = stamps.diff().dropna()
        missing += int(np.maximum(0, diffs // 60_000 - 1).sum())
        first = frame.timestamp.iloc[0].isoformat() if first is None else first
        last = frame.timestamp.iloc[-1].isoformat()
        session = pd.cut(frame.timestamp.dt.hour, [-1, 6, 12, 20, 23], labels=["asia", "europe", "us", "late"])
        for label, values in frame.groupby(session, observed=True).spread_median:
            observations.append({"year": year, "session_utc": str(label), "observations": int(values.count()),
                                 "median_spread": float(values.median()), "p95_spread": float(values.quantile(.95))})
        count += len(frame)
    metadata.write_text(json.dumps({"instrument": "XAUUSD Dukascopy", "price_side": "BID", "volume_type": "tick volume",
                                    "timeframe": "1m", "timezone": "UTC", "rows": count, "first_utc": first,
                                    "last_utc": last, "missing_minutes_between_observed_minutes": missing,
                                    "known_limits": ["single liquidity provider feed", "bid-side prices", "tick volume only", "occasional gaps"],
                                    "canonical_shards_sha256": shard_hashes}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    costs.write_text(json.dumps({"instrument": "XAUUSD", "spread_unit": "USD per ounce", "sessions": observations},
                                indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "data/canonical/xau_1m.parquet")
    parser.add_argument("--metadata", type=Path, default=ROOT / "data/canonical/tape_metadata_xau.json")
    parser.add_argument("--costs", type=Path, default=ROOT / "data/canonical/cost_observations_xau.json")
    args = parser.parse_args()
    build(args.output, args.metadata, args.costs)
    print(args.metadata.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
