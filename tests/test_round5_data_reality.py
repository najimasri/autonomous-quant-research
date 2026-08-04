import hashlib
import json
from pathlib import Path

import yaml

from src.validation.round5_gauntlet import EXPECTED_SOURCES, audit_prerequisites

ROOT = Path(__file__).resolve().parents[1]


def test_f14b_retired_and_finding_recorded_verbatim():
    governance = yaml.safe_load((ROOT / "governance/families.yaml").read_text())
    assert governance["operator_authorized_round5_data_reality_verbatim"] == "NO_STATIC_ARCHIVES_FOUND"
    assert governance["retired_families"]["F14B_liquidation_cascade"]["verdict"] == "DATA_UNAVAILABLE_STATIC"
    assert set(governance["families"]) == {
        "F14A_funding_extreme_mean_reversion_carry", "F14C_oi_confirmed_breakout", "F14D_derivatives_causal_ml"
    }


def test_feature_order_refrozen_without_liquidation_features():
    path = ROOT / "src/families/f14_features.json"
    raw = path.read_bytes()
    pin = (ROOT / "src/families/f14_features.sha256").read_text().split()[0]
    assert hashlib.sha256(raw).hexdigest() == pin
    features = json.loads(raw)
    assert tuple(features["source_order"]) == EXPECTED_SOURCES
    assert not any("liquid" in feature.lower() for feature in features["feature_order"])


def test_gauntlet_accepts_only_available_registered_sources():
    audit_prerequisites()
