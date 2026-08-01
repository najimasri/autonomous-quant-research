#!/usr/bin/env python3
"""Verify the append-only trial log's JSON records and SHA-256 chain."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "trials" / "trials.jsonl"
GENESIS = "0" * 64


def canonical(record: dict) -> bytes:
    payload = {key: value for key, value in record.items() if key != "record_sha256"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def main() -> int:
    previous = GENESIS
    records = 0
    for line_number, line in enumerate(LOG.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("previous_sha256") != previous:
            raise ValueError(f"broken previous hash at line {line_number}")
        actual = hashlib.sha256(canonical(record)).hexdigest()
        if record.get("record_sha256") != actual:
            raise ValueError(f"broken record hash at line {line_number}")
        previous, records = actual, records + 1
    print(f"Trial chain audit: PASS ({records} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
