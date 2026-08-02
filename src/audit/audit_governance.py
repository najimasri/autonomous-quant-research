#!/usr/bin/env python3
"""Prove that the immutable mission governance files remain byte-exact."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "ee44588619b3bba8132514a12eb484536bc8162c88af59e9ef3b85b0f270c3a8",
    "4ece447a8125fdf45b5f29bb4a01ac640693ac3674928d38edb0c5fb06f8b1f0",
    "d756f37f8d516e4e11c9efd13a3025db799a01381fe265369fd2f79958137f24",
    "61681018cf7fdc8b60076971e81a9a06cdafc444b10bd35ef42c14cf0e25646a",
    "ebd72b025b8a7aceed8fab1eecc5a98b1f12629e7c3d3a1ec3a3ed457f21ea73",
}


def main() -> int:
    files = sorted((ROOT / "governance").glob("*.yaml"))
    actual = {hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
    if actual != EXPECTED or len(files) != len(EXPECTED):
        raise SystemExit("Governance audit FAIL: immutable contract set changed")
    print(f"Governance audit: PASS ({len(EXPECTED)} byte-exact contracts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
