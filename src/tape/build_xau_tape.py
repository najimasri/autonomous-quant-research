#!/usr/bin/env python3
"""Build deterministic yearly XAUUSD minute shards from daily candles."""

import argparse
import hashlib
import json
import lzma
import struct
from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
# Dukascopy XAU candle record: seconds from UTC day start, four integer prices,
# then floating-point volume. XAUUSD is published in thousandths.
RECORD = struct.Struct(">5If")
PRICE_SCALE = 1_000
SCHEMA = pa.schema([
    ("timestamp", pa.timestamp("ms", tz="UTC")), ("open", pa.float64()),
    ("high", pa.float64()), ("low", pa.float64()), ("close", pa.float64()),
    ("tick_volume", pa.float64()), ("spread_proxy", pa.float64()),
])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decompress(path: Path) -> bytes:
    try:
        return lzma.decompress(path.read_bytes(), format=lzma.FORMAT_AUTO)
    except lzma.LZMAError:
        return lzma.decompress(path.read_bytes(), format=lzma.FORMAT_RAW,
                               filters=[{"id": lzma.FILTER_LZMA1, "dict_size": 1 << 23,
                                         "lc": 3, "lp": 0, "pb": 2}])


def decode(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    relative = path.relative_to(ROOT / "data/raw/xau")
    year, month0, day = map(int, relative.parts[:3])
    content = decompress(path)
    if len(content) % RECORD.size:
        raise ValueError(f"invalid Dukascopy candle length: {path} ({len(content)} bytes)")
    values = list(RECORD.iter_unpack(content))
    frame = pd.DataFrame(values, columns=["offset", "open", "close", "low", "high", "volume"])
    frame[["open", "close", "low", "high"]] /= PRICE_SCALE
    base = datetime(year, month0 + 1, day, tzinfo=timezone.utc)
    frame["timestamp"] = pd.to_datetime(base) + pd.to_timedelta(frame.pop("offset"), unit="s")
    return frame


def build_year(year: int) -> pd.DataFrame:
    root = ROOT / "data/raw/xau" / str(year)
    bid_frames = [frame for path in sorted(root.rglob("BID_candles_min_1.bi5"))
                  if not (frame := decode(path)).empty] if root.exists() else []
    ask_frames = [frame for path in sorted(root.rglob("ASK_candles_min_1.bi5"))
                  if not (frame := decode(path)).empty] if root.exists() else []
    bids = pd.concat(bid_frames, ignore_index=True) if bid_frames else pd.DataFrame()
    asks = pd.concat(ask_frames, ignore_index=True) if ask_frames else pd.DataFrame()
    if bids.empty:
        return pd.DataFrame()
    if asks.empty:
        raise ValueError(f"year {year} has BID candles but no ASK candles")
    ask_close = asks[["timestamp", "close"]].rename(columns={"close": "ask_close"})
    frame = bids.merge(ask_close, on="timestamp", how="left", validate="one_to_one")
    if frame.ask_close.isna().any():
        raise ValueError(f"year {year} has unmatched BID/ASK candle timestamps")
    frame["spread_proxy"] = frame.pop("ask_close") - frame["close"]
    frame = frame.rename(columns={"volume": "tick_volume"})
    return frame[[field.name for field in SCHEMA]]


def build(start_year: int, through_year: int, output_dir: Path, manifest: Path) -> None:
    if start_year < 2010 or through_year < start_year or through_year - start_year + 1 > 4:
        raise ValueError("build range must contain 1-4 calendar years starting no earlier than 2010")
    output_dir = output_dir.resolve()
    manifest = manifest.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    shards = {}
    for year in range(start_year, through_year + 1):
        frame = build_year(year)
        if frame.empty:
            raise ValueError(f"no BID candle rows found for {year}")
        shard = output_dir / f"xau_1m_{year}.parquet"
        temporary = shard.with_suffix(".parquet.part")
        pq.write_table(pa.Table.from_pandas(frame, schema=SCHEMA, preserve_index=False),
                       temporary, compression="zstd", version="2.6", row_group_size=100_000)
        temporary.replace(shard)
        stamps = frame.timestamp.astype("int64") // 1_000_000
        shards[str(shard.relative_to(ROOT))] = {
            "rows": len(frame), "sha256": sha256(shard),
            "first_utc": frame.timestamp.iloc[0].isoformat(),
            "last_utc": frame.timestamp.iloc[-1].isoformat(),
            "missing_minutes_between_observed_minutes":
                int(np.maximum(0, stamps.diff().dropna() // 60_000 - 1).sum()),
        }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({
        "instrument": "XAUUSD Dukascopy",
        "source_files": ["BID_candles_min_1.bi5", "ASK_candles_min_1.bi5"],
        "price_side": "BID",
        "spread_proxy": "ask close minus bid close",
        "spread_label": "CANDLE_DERIVED_APPROXIMATION",
        "timeframe": "1m", "timezone": "UTC",
        "known_limits": ["single liquidity provider feed", "bid-side prices",
                         "tick volume only", "occasional gaps"],
        "shards": shards,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--through-year", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "data/canonical")
    parser.add_argument("--manifest", type=Path, default=ROOT / "manifests/xau_batch_manifest.json")
    args = parser.parse_args()
    build(args.start_year, args.through_year, args.output_dir, args.manifest)
    print(args.manifest.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
