#!/usr/bin/env python3
"""Run the audits that are valid in a source-only CI checkout."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKS = (
    "audit_holdout_seal.py",
    "audit_governance.py",
    "verify_trials.py",
    "audit_phase2.py",
    "build_manifest.py",
)


def main() -> int:
    for script in CHECKS:
        command = [sys.executable, str(ROOT / "src/audit" / script)]
        if script == "build_manifest.py":
            command.append("--check")
        subprocess.run(command, cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
