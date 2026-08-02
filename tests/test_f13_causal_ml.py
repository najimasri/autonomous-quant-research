import dataclasses

import numpy as np
import pandas as pd
import pytest

from src.families.f13_causal_ml import (
    OuterPrediction, assert_shift_audit, build_features, execute_outer,
    feature_names, generate_candidates, registered_grid, walk_forward_outer,
)


def tape(n=500, start="2019-01-01", freq="24h"):
    rng = np.random.default_rng(13)
    close = 100 + np.cumsum(rng.normal(.05, 1, n))
    return pd.DataFrame({
        "timestamp": pd.date_range(start, periods=n, freq=freq, tz="UTC"),
        "open": close-rng.normal(0, .2, n), "high": close+1,
        "low": close-1, "close": close, "volume": rng.lognormal(4, .3, n),
    })


def test_registration_is_frozen_and_exactly_48_combinations():
    assert len(registered_grid()) == 48
    assert len(feature_names("BTC")) == len(feature_names("XAU")) + 2


@pytest.mark.parametrize("instrument", ["BTC", "XAU"])
def test_every_registered_feature_passes_current_bar_shift_audit(instrument):
    frame = tape()
    assert_shift_audit(frame, instrument)
    assert tuple(build_features(frame, instrument).columns) == feature_names(instrument)


def test_candidate_generator_scores_both_directions_and_applies_cost_gate():
    frame = tape()
    candidates = generate_candidates(frame, 2.0, 0.0001, .01)
    assert set(candidates.side) == {-1, 1}
    assert candidates.groupby("bar_index").side.nunique().eq(2).all()
    assert generate_candidates(frame, 2.0, 0.0001, 100).empty


def test_walk_forward_emits_only_outer_years_with_fold_model_hashes():
    frame = tape(n=1200)
    features = build_features(frame, "BTC")
    candidates = generate_candidates(frame, 2.0, 0.0001, .01)
    target = frame.close.shift(-3) / frame.close - 1
    predictions = walk_forward_outer(features, candidates, target, frame.timestamp,
                                     registered_grid()[0], "BTC")
    assert predictions
    assert all(p.outer_held_out and p.outer_year > p.train_through_year for p in predictions)
    assert all(len(p.model_sha256) == 64 and len(p.feature_sha256) == 64 for p in predictions)


def test_execution_rejects_non_outer_scores():
    frame = tape()
    candidates = generate_candidates(frame, 2.0, 0.0001, .01)
    prediction = OuterPrediction("x", 2019, 2020, int(candidates.iloc[0].bar_index), 1,
                                 1.0, "a"*64, "b"*64)
    with pytest.raises(ValueError, match="non-outer"):
        execute_outer(frame, [dataclasses.replace(prediction, outer_held_out=False)],
                      registered_grid()[0], candidates, .01, 10)
