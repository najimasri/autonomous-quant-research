#!/usr/bin/env python3
"""Resumably download public Dukascopy XAUUSD hourly tick files."""

import argparse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://datafeed.dukascopy.com/datafeed/XAUUSD"


def hours(start: datetime, end: datetime):
    current = start
    while current < end:
        yield current
        current += timedelta(hours=1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=date.fromisoformat, default=date(2010, 1, 1))
    parser.add_argument("--through", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    target = ROOT / "data" / "raw" / "xau"
    target.mkdir(parents=True, exist_ok=True)
    start = datetime.combine(args.start, datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(args.through + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)
    with requests.Session() as session:
        for stamp in hours(start, end):
            relative = f"{stamp.year:04d}/{stamp.month - 1:02d}/{stamp.day:02d}/{stamp.hour:02d}h_ticks.bi5"
            destination = target / relative
            if destination.exists():
                continue
            response = session.get(f"{BASE}/{relative}", timeout=60)
            if response.status_code == 404:
                continue
            response.raise_for_status()
            destination.parent.mkdir(parents=True, exist_ok=True)
            partial = destination.with_suffix(".part")
            partial.write_bytes(response.content)
            partial.replace(destination)
            print(relative)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
