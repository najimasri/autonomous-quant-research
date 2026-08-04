#!/usr/bin/env python3
"""Round 5 prerequisite guard; evaluation remains fail-closed."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "manifests" / "round5_source_registry.json"
FEATURES = ROOT / "src" / "families" / "f14_features.json"
FEATURE_PIN = ROOT / "src" / "families" / "f14_features.sha256"
EXPECTED_SOURCES = ("fundingRate", "perp_klines", "metrics")


def audit_prerequisites() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    required = tuple(registry["gauntlet_required_sources"])
    if required != EXPECTED_SOURCES:
        raise RuntimeError("Round 5 source prerequisite is not the frozen three-source order")
    if any(registry["sources"].get(name, {}).get("status") != "AVAILABLE" for name in required):
        raise RuntimeError("Round 5 prerequisite unavailable: evaluation forbidden")
    liquidation = registry["sources"].get("liquidationSnapshot", {})
    if liquidation.get("status") != "DATA_UNAVAILABLE_STATIC" or liquidation.get("finding") != "NO_STATIC_ARCHIVES_FOUND" or liquidation.get("proxy_permitted") is not False:
        raise RuntimeError("Liquidation source retirement/no-proxy finding is not pinned")

    raw = FEATURES.read_bytes()
    expected = FEATURE_PIN.read_text(encoding="utf-8").split()[0]
    if hashlib.sha256(raw).hexdigest() != expected:
        raise RuntimeError("Frozen F14 feature-order hash mismatch")
    feature_spec = json.loads(raw)
    if tuple(feature_spec["source_order"]) != required:
        raise RuntimeError("Frozen features do not match available sources")
    if any("liquid" in name.lower() for name in feature_spec["feature_order"]):
        raise RuntimeError("Unavailable liquidation feature remains frozen")


if __name__ == "__main__":
    audit_prerequisites()
    print("Round 5 prerequisites: PASS (fundingRate, perp_klines, metrics; feature pin verified)")
