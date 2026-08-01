#!/usr/bin/env python3
"""Resumably download and checksum Binance Vision BTCUSDT monthly archives."""

import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1m"


def months(start: date, end: date):
    year, month = start.year, start.month
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


def fetch_month(month: str, target: Path) -> tuple[str, str]:
    name = f"BTCUSDT-1m-{month}.zip"
    archive, checksum = target / name, target / f"{name}.CHECKSUM"
    with requests.Session() as session:
        download(session, f"{BASE}/{name}", archive)
        download(session, f"{BASE}/{name}.CHECKSUM", checksum)
    expected = checksum.read_text(encoding="utf-8").split()[0].lower()
    actual = hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"checksum mismatch: {name}")
    return name, actual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=date.fromisoformat, default=date(2017, 8, 1))
    parser.add_argument("--through", type=date.fromisoformat, default=date.today())
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    target = ROOT / "data" / "raw" / "btc"
    target.mkdir(parents=True, exist_ok=True)
    # Monthly archives exist only after a month closes.
    end = args.through.replace(day=1) - __import__("datetime").timedelta(days=1)
    start = args.start.replace(day=1)
    if start < date(2017, 8, 1) or start > end:
        raise SystemExit("range must contain closed months starting on/after 2017-08")
    expected = list(months(start, end))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for name, digest in pool.map(lambda month: fetch_month(month, target), expected):
            print(f"verified {name} {digest}")
    (target / "ingest_metadata.json").write_text(json.dumps({
        "source": BASE, "first_month": expected[0], "last_complete_month": expected[-1],
        "archives_verified": len(expected), "checksum_files": len(expected),
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
