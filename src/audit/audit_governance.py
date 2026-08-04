#!/usr/bin/env python3
"""Prove that the immutable mission governance files remain byte-exact."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "ee44588619b3bba8132514a12eb484536bc8162c88af59e9ef3b85b0f270c3a8",
    "4ece447a8125fdf45b5f29bb4a01ac640693ac3674928d38edb0c5fb06f8b1f0",
    # governance/families.yaml: Round 5 operator registration supersedes the
    # original Round 5 pin: F14B is DATA_UNAVAILABLE_STATIC after
    # NO_STATIC_ARCHIVES_FOUND; all other governance pins remain intact.
    "2d19d235280ba5887e97416912348cb36ede2f95bb75b0742df528c7fd129962",
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
