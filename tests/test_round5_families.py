import numpy as np
import pandas as pd

from src.families.f14_derivatives import FEATURE_NAMES, assert_derivatives_shift_audit, build_derivatives_features
from src.families.round5_grid import load_round5_features, load_round5_grids


def fixtures():
    rng = np.random.default_rng(14)
    timestamps = pd.date_range("2021-01-01", periods=60*24*8, freq="1min", tz="UTC")
    close = 30000 + np.cumsum(rng.normal(0, 2, len(timestamps)))
    spot = pd.DataFrame({"timestamp": timestamps, "open": close, "high": close+3,
                         "low": close-3, "close": close, "volume": 10})
    hourly = pd.date_range(timestamps[0], timestamps[-1], freq="1h", tz="UTC")
    n = len(hourly); base = np.arange(n)
    derivatives = {
        "fundingRate": pd.DataFrame({"timestamp": hourly, "last_funding_rate": np.sin(base/20)/1000}),
        "perp_klines_1m": pd.DataFrame({"timestamp": hourly, "close": 30005+base}),
        "metrics": pd.DataFrame({"timestamp": hourly, "sum_open_interest": 1e9+base*1e6,
                                  "count_long_short_ratio": 1+np.sin(base/10)/10,
                                  "sum_taker_long_short_vol_ratio": 1+np.cos(base/10)/10}),
        "liquidationSnapshot": pd.DataFrame({"timestamp": hourly, "quantity": 1+(base % 50)}),
    }
    return spot, derivatives


def test_round5_grids_are_frozen_and_within_budget():
    grids = load_round5_grids()
    assert set(grids) == {"F14A", "F14B", "F14C", "F14D"}
    assert all(0 < len(configs) <= 48 for configs in grids.values())
    assert load_round5_features() == FEATURE_NAMES


def test_derivatives_features_have_frozen_order_and_prior_only_shift():
    spot, derivatives = fixtures()
    features = build_derivatives_features(spot, derivatives, "1h")
    assert tuple(features.columns[1:]) == FEATURE_NAMES
    assert features.timestamp.is_monotonic_increasing
    assert_derivatives_shift_audit(spot, derivatives, "1h")
