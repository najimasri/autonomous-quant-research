#!/usr/bin/env python3
"""Reject holdout configuration or boundary references in research code."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED = ROOT / "src" / "validation" / "phase5_holdout_runner.py"
TOKENS = ("holdout.yaml", "2025-07-01", "2024-07-01")


def main() -> int:
    violations: list[str] = []
    for path in (ROOT / "src").rglob("*.py"):
        if path == ALLOWED or path == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in TOKENS):
            violations.append(str(path.relative_to(ROOT)))
    if violations:
        print("Holdout seal violations: " + ", ".join(sorted(violations)))
        return 1
    print("Holdout seal audit: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
