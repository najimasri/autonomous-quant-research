#!/usr/bin/env python3
"""Resumably download public Dukascopy XAUUSD hourly tick files."""

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from threading import local

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://datafeed.dukascopy.com/datafeed/XAUUSD"
THREAD_STATE = local()


def http_session() -> requests.Session:
    if not hasattr(THREAD_STATE, "session"):
        session = requests.Session()
        session.mount("https://", HTTPAdapter(pool_connections=1, pool_maxsize=1,
                      max_retries=Retry(total=50, backoff_factor=2,
                      status_forcelist=(429, 500, 502, 503, 504),
                      respect_retry_after_header=True)))
        THREAD_STATE.session = session
    return THREAD_STATE.session


def hours(start: datetime, end: datetime):
    current = start
    while current < end:
        # The contracted OTC feed is closed from Friday 22:00 through Sunday
        # 21:00 UTC; avoiding guaranteed-empty requests makes full rebuilds
        # substantially faster without excluding a quoting hour.
        if current.weekday() < 4 or (current.weekday() == 4 and current.hour < 22) or (current.weekday() == 6 and current.hour >= 21):
            yield current
        current += timedelta(hours=1)


def fetch(stamp: datetime, target: Path) -> tuple[str, int]:
    relative = f"{stamp.year:04d}/{stamp.month - 1:02d}/{stamp.day:02d}/{stamp.hour:02d}h_ticks.bi5"
    destination = target / relative
    if destination.exists():
        return relative, destination.stat().st_size
    response = http_session().get(f"{BASE}/{relative}", timeout=60)
    if response.status_code == 404:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.touch()
        return relative, 0
    response.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(".part")
    partial.write_bytes(response.content)
    partial.replace(destination)
    return relative, len(response.content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=date.fromisoformat, default=date(2010, 1, 1))
    parser.add_argument("--through", type=date.fromisoformat, default=date.today())
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    target = ROOT / "data" / "raw" / "xau"
    target.mkdir(parents=True, exist_ok=True)
    start = datetime.combine(args.start, datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(args.through + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)
    expected = list(hours(start, end))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for relative, size in pool.map(lambda stamp: fetch(stamp, target), expected):
            if size >= 0:
                print(f"{relative} {size}")
    files = list(target.rglob("*.bi5"))
    (target / "ingest_metadata.json").write_text(json.dumps({
        "source": BASE, "start_utc": start.isoformat(), "end_exclusive_utc": end.isoformat(),
        "expected_market_hours": len(expected), "files_present": len(files),
        "nonempty_files": sum(path.stat().st_size > 0 for path in files),
        "empty_or_not_found_hours": sum(path.stat().st_size == 0 for path in files),
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
