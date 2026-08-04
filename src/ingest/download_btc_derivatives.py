#!/usr/bin/env python3
"""Acquire checksum-verified static BTCUSDT USDT-M derivatives archives."""

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Iterator

import requests

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://data.binance.vision/data/futures/um"
SYMBOL = "BTCUSDT"


@dataclass(frozen=True)
class Source:
    name: str
    cadence: str
    path: str
    first_candidate: date


SOURCES = {
    "fundingRate": Source("fundingRate", "monthly", "monthly/fundingRate/BTCUSDT", date(2020, 1, 1)),
    "perp_klines_1m": Source("perp_klines_1m", "monthly", "monthly/klines/BTCUSDT/1m", date(2020, 1, 1)),
    "metrics": Source("metrics", "daily", "daily/metrics/BTCUSDT", date(2020, 9, 1)),
    "liquidationSnapshot": Source("liquidationSnapshot", "daily", "daily/liquidationSnapshot/BTCUSDT", date(2019, 9, 1)),
}


def periods(source: Source, start: date, through: date) -> Iterator[date]:
    cursor = max(start, source.first_candidate)
    if source.cadence == "monthly":
        cursor = cursor.replace(day=1)
        end = through.replace(day=1) - timedelta(days=1)
        while cursor <= end:
            yield cursor
            cursor = date(cursor.year + (cursor.month == 12), cursor.month % 12 + 1, 1)
    else:
        cursor = max(cursor, source.first_candidate)
        end = through - timedelta(days=1)
        while cursor <= end:
            yield cursor
            cursor += timedelta(days=1)


def archive_name(source: Source, period: date) -> str:
    stamp = period.strftime("%Y-%m" if source.cadence == "monthly" else "%Y-%m-%d")
    if source.name == "perp_klines_1m":
        return f"{SYMBOL}-1m-{stamp}.zip"
    return f"{SYMBOL}-{source.name}-{stamp}.zip"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(session: requests.Session, url: str, destination: Path) -> requests.Response:
    partial = destination.with_suffix(destination.suffix + ".part")
    headers = {"Range": f"bytes={partial.stat().st_size}-"} if partial.exists() else {}
    response = session.get(url, headers=headers, stream=True, timeout=90)
    if response.status_code == 404:
        return response
    response.raise_for_status()
    mode = "ab" if response.status_code == 206 else "wb"
    with partial.open(mode) as handle:
        for chunk in response.iter_content(1024 * 1024):
            if chunk:
                handle.write(chunk)
    partial.replace(destination)
    return response


def acquire(source: Source, start: date, through: date, root: Path) -> dict:
    target = root / source.name
    target.mkdir(parents=True, exist_ok=True)
    records = {}
    with requests.Session() as session:
        for period in periods(source, start, through):
            name = archive_name(source, period)
            archive = target / name
            checksum = target / f"{name}.CHECKSUM"
            url = f"{BASE}/{source.path}/{name}"
            if not archive.exists() and fetch(session, url, archive).status_code == 404:
                continue
            checksum_published = True
            if not checksum.exists() and fetch(session, f"{url}.CHECKSUM", checksum).status_code == 404:
                checksum_published = False
            actual = sha256(archive)
            if checksum_published:
                expected = checksum.read_text(encoding="utf-8").split()[0].lower()
                if actual != expected:
                    archive.unlink(missing_ok=True)
                    raise ValueError(f"checksum mismatch: {name}")
            records[name] = {"sha256": actual, "checksum_published": checksum_published, "period": period.isoformat()}
            print(f"verified {source.name}/{name} {actual}")
    first = min(records) if records else None
    return {
        "source": asdict(source),
        "availability_status": "AVAILABLE" if first else "NO_STATIC_ARCHIVES_FOUND",
        "first_available_archive": first,
        "first_available_date": records[first]["period"] if first else None,
        "archives": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=date.fromisoformat, default=date(2019, 9, 1))
    parser.add_argument("--through", type=date.fromisoformat, default=date.today())
    parser.add_argument("--source", action="append", choices=sorted(SOURCES))
    parser.add_argument("--raw-root", type=Path, default=ROOT / "data/raw/btc_derivatives")
    args = parser.parse_args()
    selected = args.source or list(SOURCES)
    if args.start >= args.through:
        raise SystemExit("--start must precede --through")
    manifest = {name: acquire(SOURCES[name], args.start, args.through, args.raw_root) for name in selected}
    path = args.raw_root / "acquisition_manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
