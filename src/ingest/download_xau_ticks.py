#!/usr/bin/env python3
"""Download a bounded March/September sample of Dukascopy XAUUSD ticks."""

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

import download_xau as candles

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://datafeed.dukascopy.com/datafeed/XAUUSD"
SAMPLE_MONTHS = (3, 9)


def sample_days(year: int, days_per_month: int = 1):
    """Choose the first N weekdays of March and September deterministically."""
    for month in SAMPLE_MONTHS:
        day = date(year, month, 1)
        emitted = 0
        while emitted < days_per_month:
            if day.weekday() < 5:
                yield day
                emitted += 1
            day += timedelta(days=1)


def relative_paths(day: date):
    prefix = f"{day.year:04d}/{day.month - 1:02d}/{day.day:02d}"
    for hour in range(24):
        yield f"{prefix}/{hour:02d}h_ticks.bi5"


def fetch(relative: str, target: Path):
    return candles.fetch(relative, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-year", type=int, required=True)
    parser.add_argument("--through-year", type=int, required=True)
    parser.add_argument("--days-per-month", type=int, choices=range(1, 6), default=1)
    parser.add_argument("--workers", type=candles.worker_count, default=candles.MAX_WORKERS)
    args = parser.parse_args()
    if args.start_year < 2010 or not args.start_year <= args.through_year <= args.start_year + 3:
        raise SystemExit("refusing: range must be 1-4 years starting no earlier than 2010")

    target = ROOT / "data/raw/xau_ticks"
    paths = [path for year in range(args.start_year, args.through_year + 1)
             for day in sample_days(year, args.days_per_month) for path in relative_paths(day)]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for relative, size in pool.map(lambda path: fetch(path, target), paths):
            print(f"{relative} {size}")
    target.mkdir(parents=True, exist_ok=True)
    (target / "ingest_metadata.json").write_text(json.dumps({
        "source": BASE, "sample_months": list(SAMPLE_MONTHS),
        "days_per_month": args.days_per_month, "expected_files": len(paths),
        "pacing": {"max_concurrent_requests": candles.MAX_WORKERS,
                   "minimum_request_spacing_ms": int(candles.REQUEST_SPACING_SECONDS * 1000)},
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
