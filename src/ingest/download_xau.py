#!/usr/bin/env python3
"""Download daily Dukascopy XAUUSD one-minute BID and ASK candles safely."""

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from threading import Lock, local

import requests

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://datafeed.dukascopy.com/datafeed/XAUUSD"
MAX_WORKERS = 4
REQUEST_SPACING_SECONDS = 0.2
MAX_ATTEMPTS = 8
RETRYABLE_STATUS = frozenset((429, 500, 502, 503, 504))
THREAD_STATE = local()


class RequestPacer:
    """Serialize request starts so the process-wide spacing cannot be bypassed."""

    def __init__(self, spacing: float = REQUEST_SPACING_SECONDS) -> None:
        self.spacing = spacing
        self._lock = Lock()
        self._last_start: float | None = None

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            if self._last_start is not None:
                time.sleep(max(0.0, self.spacing - (now - self._last_start)))
            self._last_start = time.monotonic()


PACER = RequestPacer()


def http_session() -> requests.Session:
    if not hasattr(THREAD_STATE, "session"):
        # Retries are deliberately implemented by fetch(): adapter-level retries
        # could evade the process-wide request pacer.
        THREAD_STATE.session = requests.Session()
    return THREAD_STATE.session


def trading_days(start: date, through: date):
    current = start
    while current <= through:
        if current.weekday() < 5:
            yield current
        current += timedelta(days=1)


def relative_paths(day: date):
    prefix = f"{day.year:04d}/{day.month - 1:02d}/{day.day:02d}"
    for side in ("BID", "ASK"):
        yield f"{prefix}/{side}_candles_min_1.bi5"


def retry_after_seconds(value: str | None, now: datetime | None = None) -> float:
    if value is None:
        return 0.0
    try:
        return max(0.0, float(value))
    except ValueError:
        retry_at = parsedate_to_datetime(value)
        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=timezone.utc)
        return max(0.0, (retry_at - (now or datetime.now(timezone.utc))).total_seconds())


def fetch(relative: str, target: Path) -> tuple[str, int]:
    destination = target / relative
    if destination.exists():
        return relative, destination.stat().st_size

    for attempt in range(MAX_ATTEMPTS):
        PACER.wait()
        try:
            response = http_session().get(f"{BASE}/{relative}", timeout=60)
        except requests.RequestException:
            if attempt + 1 == MAX_ATTEMPTS:
                raise
            time.sleep(min(60.0, 2.0**attempt))
            continue

        if response.status_code == 404:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.touch()
            return relative, 0
        if response.status_code in RETRYABLE_STATUS:
            if attempt + 1 == MAX_ATTEMPTS:
                response.raise_for_status()
            # Never retry earlier than either exponential backoff or the
            # server's Retry-After instruction.
            delay = max(min(60.0, 2.0**attempt),
                        retry_after_seconds(response.headers.get("Retry-After")))
            time.sleep(delay)
            continue

        response.raise_for_status()
        destination.parent.mkdir(parents=True, exist_ok=True)
        partial = destination.with_suffix(destination.suffix + ".part")
        partial.write_bytes(response.content)
        partial.replace(destination)
        return relative, len(response.content)

    raise AssertionError("retry loop exhausted")


def worker_count(value: str) -> int:
    workers = int(value)
    if not 1 <= workers <= MAX_WORKERS:
        raise argparse.ArgumentTypeError("workers must be between 1 and 4")
    return workers


def validate_batch(start: date, through: date) -> None:
    if start < date(2010, 1, 1):
        raise SystemExit("XAU acquisition starts no earlier than 2010-01-01")
    if through < start:
        raise SystemExit("--through must not precede --start")
    if through.year - start.year + 1 > 4:
        raise SystemExit("refusing a batch spanning more than 4 calendar years")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=date.fromisoformat, required=True)
    parser.add_argument("--through", type=date.fromisoformat, required=True)
    parser.add_argument("--workers", type=worker_count, default=MAX_WORKERS)
    args = parser.parse_args()
    validate_batch(args.start, args.through)

    target = ROOT / "data" / "raw" / "xau"
    target.mkdir(parents=True, exist_ok=True)
    expected = [path for day in trading_days(args.start, args.through)
                for path in relative_paths(day)]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for relative, size in pool.map(lambda path: fetch(path, target), expected):
            print(f"{relative} {size}")

    files = [target / path for path in expected]
    metadata = {
        "source": BASE,
        "file_contract": ["BID_candles_min_1.bi5", "ASK_candles_min_1.bi5"],
        "start_utc": args.start.isoformat(),
        "through_utc": args.through.isoformat(),
        "expected_files": len(expected),
        "files_present": sum(path.exists() for path in files),
        "nonempty_files": sum(path.exists() and path.stat().st_size > 0 for path in files),
        "empty_or_not_found_files": sum(path.exists() and path.stat().st_size == 0 for path in files),
        "pacing": {"max_concurrent_requests": MAX_WORKERS,
                   "minimum_request_spacing_ms": int(REQUEST_SPACING_SECONDS * 1000)},
    }
    (target / "ingest_metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
