#!/usr/bin/env python3
"""Build candle-approximation and sampled-tick XAU spread distributions."""

import argparse
import json
import lzma
import struct
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]
TICK = struct.Struct(">IIIff")  # millisecond, ask, bid, ask volume, bid volume
PRICE_SCALE = 1_000
QUANTILES = (0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)


def decompress(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        return lzma.decompress(data, format=lzma.FORMAT_AUTO)
    except lzma.LZMAError:
        return lzma.decompress(data, format=lzma.FORMAT_RAW,
                               filters=[{"id": lzma.FILTER_LZMA1, "dict_size": 1 << 23,
                                         "lc": 3, "lp": 0, "pb": 2}])


def tick_spreads(path: Path) -> np.ndarray:
    content = decompress(path)
    if len(content) % TICK.size:
        raise ValueError(f"invalid Dukascopy tick length: {path} ({len(content)} bytes)")
    return np.fromiter(((ask - bid) / PRICE_SCALE
                        for _, ask, bid, _, _ in TICK.iter_unpack(content)), dtype=float)


def distribution(values, label: str) -> dict:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if not len(values):
        raise ValueError(f"no observations for {label}")
    return {"label": label, "rows": int(len(values)), "minimum": float(values.min()),
            "maximum": float(values.max()), "mean": float(values.mean()),
            "quantiles": {str(q): float(v) for q, v in zip(QUANTILES, np.quantile(values, QUANTILES))}}


def build(candle_dir: Path, tick_dir: Path, output: Path) -> None:
    candle_parts = [pq.read_table(path, columns=["spread_proxy"])["spread_proxy"].to_numpy()
                    for path in sorted(candle_dir.glob("xau_1m_*.parquet"))]
    tick_parts = [tick_spreads(path) for path in sorted(tick_dir.rglob("*h_ticks.bi5"))
                  if path.stat().st_size]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "instrument": "XAUUSD Dukascopy", "price_unit": "USD per troy ounce",
        "candle": distribution(np.concatenate(candle_parts) if candle_parts else [],
                               "CANDLE_DERIVED_APPROXIMATION"),
        "tick": distribution(np.concatenate(tick_parts) if tick_parts else [], "TICK_OBSERVED"),
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candle-dir", type=Path, default=ROOT / "data/canonical")
    parser.add_argument("--tick-dir", type=Path, default=ROOT / "data/raw/xau_ticks")
    parser.add_argument("--output", type=Path, default=ROOT / "manifests/xau_cost_observations.json")
    args = parser.parse_args()
    build(args.candle_dir, args.tick_dir, args.output)
    print(args.output.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
