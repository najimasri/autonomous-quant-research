#!/usr/bin/env python3
"""Resumably download and checksum Binance Vision BTCUSDT monthly archives."""

import argparse
import hashlib
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1m"


def months(start_year: int, start_month: int, end: date):
    year, month = start_year, start_month
    while (year, month) <= (end.year, end.month):
        yield f"{year:04d}-{month:02d}"
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)


def download(session: requests.Session, url: str, destination: Path) -> None:
    if destination.exists():
        return
    partial = destination.with_suffix(destination.suffix + ".part")
    headers = {"Range": f"bytes={partial.stat().st_size}-"} if partial.exists() else {}
    with session.get(url, headers=headers, stream=True, timeout=60) as response:
        response.raise_for_status()
        mode = "ab" if response.status_code == 206 else "wb"
        with partial.open(mode) as handle:
            for chunk in response.iter_content(1024 * 1024):
                handle.write(chunk)
    partial.replace(destination)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    target = ROOT / "data" / "raw" / "btc"
    target.mkdir(parents=True, exist_ok=True)
    with requests.Session() as session:
        for month in months(2017, 8, args.through):
            name = f"BTCUSDT-1m-{month}.zip"
            archive, checksum = target / name, target / f"{name}.CHECKSUM"
            download(session, f"{BASE}/{name}", archive)
            download(session, f"{BASE}/{name}.CHECKSUM", checksum)
            expected = checksum.read_text(encoding="utf-8").split()[0].lower()
            actual = hashlib.sha256(archive.read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(f"checksum mismatch: {name}")
            print(f"verified {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
