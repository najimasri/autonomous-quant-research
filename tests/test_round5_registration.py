from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_round5_registration_and_round4_retirement():
    registration = yaml.safe_load(
        (ROOT / "governance" / "families.yaml").read_text(encoding="utf-8")
    )

    assert registration["retired_families"]["F13_causal_ml"]["verdict"] == "EMPTY_SET_ROUND4"
    assert set(registration["families"]) == {
        "F14A_funding_extreme_mean_reversion_carry",
        "F14B_liquidation_cascade",
        "F14C_oi_confirmed_breakout",
        "F14D_derivatives_causal_ml",
    }
    for family in registration["families"].values():
        assert family["instruments"] == ["BTC"]
        assert family["decision_timeframes"] == ["1h", "4h"]
        assert family["param_budget_max_combos"] <= 48


def test_operator_registration_is_recorded_verbatim():
    registration = yaml.safe_load(
        (ROOT / "governance" / "families.yaml").read_text(encoding="utf-8")
    )
    directive = registration["operator_authorized_registration_verbatim"]

    assert directive.startswith("Register F14 derivatives-conditioned BTC families")
    assert "cost-to-stop ≤0.15" in directive
    assert "real 200-member re-simulated controls" in directive
    assert "SWING_REQUIRED flags" in directive
