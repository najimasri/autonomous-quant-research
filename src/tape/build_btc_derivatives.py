#!/usr/bin/env python3
"""Normalize verified BTC derivatives archives into compact yearly Parquet shards."""

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/btc_derivatives"
OUT = ROOT / "data/derivatives"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_archive(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as bundle:
        members = [name for name in bundle.namelist() if name.endswith(".csv")]
        if len(members) != 1:
            raise ValueError(f"expected one CSV in {path}")
        with bundle.open(members[0]) as handle:
            return pd.read_csv(handle)


def timestamp_column(frame: pd.DataFrame) -> str:
    candidates = ("timestamp", "open_time", "create_time", "time", "calc_time")
    lowered = {str(column).lower(): column for column in frame.columns}
    for candidate in candidates:
        if candidate in lowered:
            return lowered[candidate]
    raise ValueError(f"no timestamp column in {list(frame.columns)}")


def normalize(frame: pd.DataFrame, source: str) -> pd.DataFrame:
    frame.columns = [str(column).strip().lower().replace(" ", "_") for column in frame.columns]
    column = timestamp_column(frame)
    numeric = pd.to_numeric(frame[column], errors="coerce")
    unit = "us" if numeric.dropna().median() > 10**14 else "ms"
    frame["timestamp"] = pd.to_datetime(numeric, unit=unit, utc=True, errors="coerce")
    frame = frame.dropna(subset=["timestamp"]).sort_values("timestamp")
    frame.insert(0, "source", source)
    return frame.drop_duplicates(subset=["timestamp"], keep="last")


def build(raw_root: Path, output_root: Path, manifest_path: Path) -> dict:
    acquisition = json.loads((raw_root / "acquisition_manifest.json").read_text())
    result = {"instrument": "BTCUSDT USDT-M perpetual", "source_domain": "data.binance.vision", "sources": {}}
    output_root.mkdir(parents=True, exist_ok=True)
    for source, metadata in acquisition.items():
        archives = [raw_root / source / name for name in metadata["archives"]]
        frames = [normalize(read_archive(path), source) for path in archives]
        source_manifest = {
            "availability_status": metadata["availability_status"],
            "first_available_archive": metadata["first_available_archive"],
            "first_available_date": metadata["first_available_date"],
            "shards": {},
        }
        if frames:
            combined = pd.concat(frames, ignore_index=True, sort=False).sort_values("timestamp")
            for year, shard in combined.groupby(combined.timestamp.dt.year):
                destination = output_root / f"btc_{source}_{year}.parquet"
                shard.to_parquet(destination, index=False, compression="zstd")
                relative = str(destination.relative_to(ROOT))
                source_manifest["shards"][relative] = {
                    "rows": len(shard), "first_utc": shard.timestamp.min().isoformat(),
                    "last_utc": shard.timestamp.max().isoformat(), "sha256": sha256(destination),
                }
        result["sources"][source] = source_manifest
    manifest_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, default=RAW)
    parser.add_argument("--output-root", type=Path, default=OUT)
    parser.add_argument("--manifest", type=Path, default=ROOT / "manifests/btc_derivatives_manifest.json")
    args = parser.parse_args()
    build(args.raw_root, args.output_root, args.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
